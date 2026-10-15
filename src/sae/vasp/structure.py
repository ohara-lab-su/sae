"""POSCAR geometry and selective-dynamics flags, without global VASP state."""

from itertools import groupby
import numpy as np
from sae.structure import Structure
from sae._text import read_text, write_text
from sae.errors import ParseError


class Poscar:
    """POSCAR document with Cartesian geometry and VASP movement flags.

    ``movable`` is True for VASP T, False for F. Extra trailing sections are
    retained verbatim; changing site count with those sections is forbidden.
    """

    def __init__(self, structure, title="SAE structure", movable=None, tail=()):
        self.structure = structure.copy()
        self.title = str(title)
        if "\n" in self.title or "\r" in self.title:
            raise ValueError("Title must occupy one line")
        self.movable = (
            None if movable is None else np.asarray(movable, dtype=bool).copy()
        )
        self.tail = tuple(tail)
        self._original_count = len(structure)
        self._validate()

    def _validate(self):
        if self.movable is not None and self.movable.shape != (len(self.structure), 3):
            raise ValueError("movable must be an (natom, 3) boolean array")
        if (
            any(line.strip() for line in self.tail)
            and len(self.structure) != self._original_count
        ):
            raise ValueError(
                "Cannot change site count while retaining trailing POSCAR sections"
            )

    @classmethod
    def read(cls, path, species=None):
        return cls.from_string(read_text(path), species=species)

    @classmethod
    def from_string(cls, text, species=None):
        lines = text.splitlines()
        try:
            scale = np.asarray(lines[1].split(), dtype=float)
            cell = np.asarray([line.split()[:3] for line in lines[2:5]], dtype=float)
            if scale.size == 1:
                value = scale[0]
                if value == 0:
                    raise ValueError("POSCAR scale cannot be zero")
                if value < 0:
                    value = (abs(value) / abs(np.linalg.det(cell))) ** (1.0 / 3.0)
                factor = np.full(3, value)
            elif scale.size == 3 and (scale > 0).all():
                factor = scale
            else:
                raise ValueError("Expected one nonzero scale or three positive scales")
            cell = cell * factor
            tokens = lines[5].split()
            cursor = 6
            try:
                counts = [int(x) for x in tokens]
            except ValueError:
                labels = tokens
                counts = [int(x) for x in lines[cursor].split()]
                cursor += 1
            else:
                if species is None:
                    raise ValueError("VASP 4 POSCAR requires explicit species labels")
                labels = list(species)
            if (
                len(labels) != len(counts)
                or any(n < 0 for n in counts)
                or sum(counts) < 1
            ):
                raise ValueError("Invalid species counts")
            selective = lines[cursor].strip().lower().startswith("s")
            cursor += int(selective)
            mode = lines[cursor].strip().lower()
            if not mode or mode[0] not in "dck":
                raise ValueError("Expected Direct or Cartesian coordinate mode")
            fractional = mode.startswith("d")
            cursor += 1
            symbols = [s for s, n in zip(labels, counts) for _ in range(n)]
            rows = [lines[cursor + i].split() for i in range(sum(counts))]
            positions = np.asarray([r[:3] for r in rows], dtype=float)
            movable = None
            if selective:
                if any(
                    len(r) < 6 or any(flag.upper() not in ("T", "F") for flag in r[3:6])
                    for r in rows
                ):
                    raise ValueError(
                        "Selective dynamics requires three T/F flags per site"
                    )
                movable = [[flag.upper() == "T" for flag in r[3:6]] for r in rows]
            structure = Structure(
                symbols,
                positions if fractional else positions * factor,
                cell,
                fractional=fractional,
            )
            return cls(structure, lines[0], movable, lines[cursor + sum(counts) :])
        except (IndexError, ValueError, ZeroDivisionError) as error:
            raise ParseError("Invalid POSCAR: {}".format(error)) from error

    def to_string(self, direct=True):
        self._validate()
        # Consecutive groups preserve original atom ordering and flag alignment.
        groups = [
            (symbol, len(list(items)))
            for symbol, items in groupby(self.structure.symbols)
        ]
        lines = [self.title, "1.0"]
        lines.extend(
            " ".join("{:.16g}".format(v) for v in row) for row in self.structure.cell
        )
        lines += [" ".join(s for s, _ in groups), " ".join(str(n) for _, n in groups)]
        if self.movable is not None:
            lines.append("Selective dynamics")
        lines.append("Direct" if direct else "Cartesian")
        positions = (
            self.structure.fractional_positions if direct else self.structure.positions
        )
        for i, row in enumerate(positions):
            line = " ".join("{:.16g}".format(v) for v in row)
            if self.movable is not None:
                line += "  " + " ".join(
                    "T" if flag else "F" for flag in self.movable[i]
                )
            lines.append(line)
        lines.extend(self.tail)
        return "\n".join(lines) + "\n"

    def write(self, path, direct=True, overwrite=False):
        write_text(path, self.to_string(direct=direct), overwrite=overwrite)
