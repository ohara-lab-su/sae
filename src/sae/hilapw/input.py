"""HiLAPW sets.in: symmetry sites, lattice parameters, spin and k mesh."""

import numpy as np
from sae._text import read_text, write_text
from sae.errors import ParseError
from sae.structure import Structure, cell_from_parameters


class Input:
    """HiLAPW input with native lattice units and symmetry-site ordering.

    The space-group specification is retained verbatim. Sites are NOT expanded
    by symmetry. Explicit length units are required when exporting geometry.
    """

    def __init__(
        self,
        title,
        nspin,
        space_group,
        lattice_parameters,
        species,
        counts,
        sites,
        kinfo,
        kpoints,
        trailing_lines=(),
    ):
        self.title = str(title)
        self.nspin = int(nspin)
        self.space_group = str(space_group)
        self.lattice_parameters = np.asarray(lattice_parameters, dtype=float).copy()
        self.species = tuple(species)
        counts_array = np.asarray(counts)
        mesh = np.asarray(kpoints)
        if not np.issubdtype(counts_array.dtype, np.integer) or not np.issubdtype(
            mesh.dtype, np.integer
        ):
            raise ValueError("Site counts and k mesh must contain integers")
        self.counts = tuple(int(n) for n in counts_array)
        self.sites = np.asarray(sites, dtype=float).copy()
        self.kinfo = int(kinfo)
        self.kpoints = mesh.copy()
        self.trailing_lines = tuple(trailing_lines)
        self.validate()

    def validate(self):
        cell_from_parameters(self.lattice_parameters)
        if (
            not self.species
            or len(self.species) != len(self.counts)
            or any(n < 1 for n in self.counts)
        ):
            raise ValueError("Each species needs a positive symmetry-site count")
        if any(not s or any(c.isspace() for c in s) for s in self.species):
            raise ValueError("Invalid species label")
        if (
            self.sites.shape != (sum(self.counts), 3)
            or not np.isfinite(self.sites).all()
        ):
            raise ValueError(
                "sites must match species counts and contain finite coordinates"
            )
        if self.kpoints.shape != (3,) or (self.kpoints < 1).any():
            raise ValueError("kpoints must contain three positive integers")
        if "\n" in self.title or "\n" in self.space_group:
            raise ValueError("Title and space group must each occupy one line")
        return self

    @classmethod
    def read(cls, path):
        return cls.from_string(read_text(path))

    @classmethod
    def from_string(cls, text):
        lines = text.splitlines()
        try:
            title, nspin, space_group = lines[0], int(lines[2]), lines[4]
            parameters = [float(x) for x in (lines[5] + " " + lines[6]).split()]
            ngroups = int(lines[8])
            species, counts, sites = [], [], []
            cursor = 9
            for _ in range(ngroups):
                label, count = lines[cursor].split()
                count = int(count)
                species.append(label)
                counts.append(count)
                cursor += 1
                for _ in range(count):
                    sites.append([float(x) for x in lines[cursor].split()])
                    cursor += 1
            kinfo = int(lines[cursor + 1])
            kpoints = [int(x) for x in lines[cursor + 2].split()]
            return cls(
                title,
                nspin,
                space_group,
                parameters,
                species,
                counts,
                sites,
                kinfo,
                kpoints,
                lines[cursor + 3 :],
            )
        except (IndexError, ValueError) as error:
            raise ParseError("Invalid HiLAPW sets.in: {}".format(error)) from error

    def to_structure(self, length_unit):
        """Export listed sites only; caller explicitly specifies native units."""
        factors = {"angstrom": 1.0, "bohr": 0.529177210903}
        if length_unit not in factors:
            raise ValueError("length_unit must be angstrom or bohr")
        symbols = [
            symbol
            for symbol, count in zip(self.species, self.counts)
            for _ in range(count)
        ]
        return Structure(
            symbols,
            self.sites,
            cell_from_parameters(self.lattice_parameters) * factors[length_unit],
            fractional=True,
        )

    def set_kpoints(self, kpoints, kinfo=None):
        value = np.asarray(kpoints)
        if (
            value.shape != (3,)
            or not np.issubdtype(value.dtype, np.integer)
            or (value < 1).any()
        ):
            raise ValueError("kpoints must contain three positive integers")
        self.kpoints = value.copy()
        if kinfo is not None:
            self.kinfo = int(kinfo)
        return self

    def to_string(self):
        self.validate()
        lines = [
            self.title,
            "-----nspin",
            str(self.nspin),
            "-----space group",
            self.space_group,
            " ".join("{:.16g}".format(x) for x in self.lattice_parameters[:3]),
            " ".join("{:.16g}".format(x) for x in self.lattice_parameters[3:]),
            "-----atoms",
            str(len(self.species)),
        ]
        cursor = 0
        for symbol, count in zip(self.species, self.counts):
            lines.append("{} {}".format(symbol, count))
            lines.extend(
                " ".join("{:.16g}".format(x) for x in row)
                for row in self.sites[cursor : cursor + count]
            )
            cursor += count
        lines += [
            "-----k points",
            str(self.kinfo),
            " ".join(str(x) for x in self.kpoints),
        ]
        lines += list(self.trailing_lines)
        return "\n".join(lines) + "\n"

    def write(self, path, overwrite=False):
        write_text(path, self.to_string(), overwrite=overwrite)
