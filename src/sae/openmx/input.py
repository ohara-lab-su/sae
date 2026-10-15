"""OpenMX input documents: parameters, blocks, geometry, and constraints."""

from pathlib import Path
import re
import numpy as np
from sae._text import read_text, write_text
from sae.errors import ParseError
from sae.structure import Structure

BOHR = 0.529177210903


class Input:
    """An editable OpenMX .dat document retaining unknown settings and blocks.

    Species labels (including distinct basis sets for the same element) and
    per-site spin/occupation columns remain in their original site order.
    """

    def __init__(self, text):
        self._lines = str(text).splitlines()
        self._scan()

    @classmethod
    def read(cls, path):
        return cls(read_text(path))

    def _scan(self):
        self._parameters, self._blocks = {}, {}
        active = None
        for i, line in enumerate(self._lines):
            data = line.split("#", 1)[0].strip()
            if not data:
                continue
            if data.startswith("<"):
                if active is not None:
                    raise ParseError("Nested OpenMX blocks at line {}".format(i + 1))
                active = (data[1:].strip().lower(), i)
            elif data.endswith(">"):
                if active is None or data[:-1].strip().lower() != active[0]:
                    raise ParseError(
                        "Unmatched block terminator at line {}".format(i + 1)
                    )
                if active[0] in self._blocks:
                    raise ParseError("Duplicate OpenMX block: " + active[0])
                self._blocks[active[0]] = (active[1], i)
                active = None
            elif active is None:
                parts = data.split(None, 1)
                if len(parts) == 2:
                    if parts[0].lower() in self._parameters:
                        raise ParseError("Duplicate OpenMX parameter: " + parts[0])
                    self._parameters[parts[0].lower()] = (i, parts[1])
        if active is not None:
            raise ParseError("Unclosed OpenMX block: " + active[0])

    def get_parameter(self, name, default=None):
        entry = self._parameters.get(name.lower())
        return default if entry is None else entry[1]

    def set_parameter(self, name, value):
        if not name or any(c.isspace() for c in name) or any(c in name for c in "<>#"):
            raise ValueError("Invalid parameter name")
        value = str(value)
        if "\n" in value or "\r" in value:
            raise ValueError("Parameter values must occupy one line")
        entry = self._parameters.get(name.lower())
        line = "{}  {}".format(name, value)
        if entry is None:
            self._lines.append(line)
        else:
            original = self._lines[entry[0]]
            if "#" in original:
                line += "  #" + original.split("#", 1)[1]
            self._lines[entry[0]] = line
        self._scan()
        return self

    def get_block(self, name):
        try:
            start, stop = self._blocks[name.lower()]
        except KeyError:
            raise ParseError("Missing OpenMX block: " + name)
        return [
            line.split("#", 1)[0].split()
            for line in self._lines[start + 1 : stop]
            if line.split("#", 1)[0].strip()
        ]

    def set_block(self, name, rows):
        if not re.match(r"^[A-Za-z][A-Za-z0-9_.]*$", name):
            raise ValueError("Invalid block name")
        rendered = [" ".join(str(item) for item in row) for row in rows]
        if any("\n" in line or "\r" in line for line in rendered):
            raise ValueError("Block rows must occupy one line")
        if name.lower() in self._blocks:
            start, stop = self._blocks[name.lower()]
            self._lines[start + 1 : stop] = rendered
        else:
            self._lines += ["<" + name] + rendered + [name + ">"]
        self._scan()
        return self

    @staticmethod
    def _unit(value, fractional=False):
        unit = value.lower()
        if unit == "ang":
            return 1.0
        if unit == "au":
            return BOHR
        if fractional and unit == "frac":
            return None
        raise ParseError("Unsupported OpenMX coordinate unit: " + value)

    @property
    def species(self):
        """Basis and pseudopotential definitions keyed by OpenMX species label."""
        rows = self.get_block("Definition.of.Atomic.Species")
        if any(len(row) != 3 for row in rows):
            raise ParseError(
                "Species definitions require label, basis and pseudopotential"
            )
        result = {r[0]: (r[1], r[2]) for r in rows}
        if len(result) != len(rows) or len(rows) != int(
            self.get_parameter("Species.Number", -1)
        ):
            raise ParseError("Species.Number does not match unique species definitions")
        return result

    def _site_rows(self):
        rows = self.get_block("Atoms.SpeciesAndCoordinates")
        if len(rows) != int(self.get_parameter("Atoms.Number", -1)):
            raise ParseError("Atoms.Number does not match coordinate rows")
        if any(len(row) < 5 for row in rows):
            raise ParseError("Coordinate rows require index, species and x/y/z")
        ids = [int(row[0]) for row in rows]
        if ids != list(range(1, len(rows) + 1)):
            raise ParseError("OpenMX site indices must be sequential, starting at 1")
        species = self.species
        if any(row[1] not in species for row in rows):
            raise ParseError("Coordinate row references an undefined species")
        return rows

    @property
    def structure(self):
        rows = self._site_rows()
        cell = np.asarray(self.get_block("Atoms.UnitVectors"), dtype=float)
        cell *= self._unit(self.get_parameter("Atoms.UnitVectors.Unit", "AU"))
        factor = self._unit(
            self.get_parameter("Atoms.SpeciesAndCoordinates.Unit", "AU"), True
        )
        positions = np.asarray([r[2:5] for r in rows], dtype=float)
        return Structure(
            [r[1] for r in rows],
            positions if factor is None else positions * factor,
            cell,
            fractional=factor is None,
        )

    def set_structure(self, structure):
        rows = self._site_rows()
        if structure.symbols != tuple(row[1] for row in rows):
            raise ValueError(
                "Site count/order/species must match to preserve spin and constraint columns"
            )
        for row, xyz in zip(rows, structure.positions):
            row[2:5] = ["{:.16g}".format(x) for x in xyz]
        self.set_block("Atoms.SpeciesAndCoordinates", rows)
        self.set_block(
            "Atoms.UnitVectors",
            [["{:.16g}".format(x) for x in row] for row in structure.cell],
        )
        self.set_parameter("Atoms.SpeciesAndCoordinates.Unit", "Ang")
        self.set_parameter("Atoms.UnitVectors.Unit", "Ang")
        return self

    @property
    def fixed(self):
        rows = self._site_rows()
        result = np.zeros((len(rows), 3), dtype=bool)
        if "md.fixed.xyz" not in self._blocks:
            return result
        seen = set()
        for row in self.get_block("MD.Fixed.XYZ"):
            if len(row) != 4 or any(flag not in ("0", "1") for flag in row[1:]):
                raise ParseError("MD.Fixed.XYZ requires index and three 0/1 flags")
            i = int(row[0]) - 1
            if i < 0 or i >= len(rows) or i in seen:
                raise ParseError("Invalid or duplicate fixed-site index")
            seen.add(i)
            result[i] = [flag == "1" for flag in row[1:]]
        return result

    def set_fixed(self, fixed):
        flags = np.asarray(fixed)
        if (
            flags.shape != (len(self._site_rows()), 3)
            or not np.isin(flags, [0, 1]).all()
        ):
            raise ValueError("fixed must be an (natom, 3) array of boolean flags")
        return self.set_block(
            "MD.Fixed.XYZ",
            [[i + 1] + row.astype(int).tolist() for i, row in enumerate(flags)],
        )

    def to_string(self):
        return "\n".join(self._lines) + "\n"

    def write(self, path, overwrite=False):
        # Validate geometry and constraints before writing a modified input.
        self.structure
        self.fixed
        write_text(path, self.to_string(), overwrite=overwrite)
