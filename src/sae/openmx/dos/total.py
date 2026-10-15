"""OpenMX total DOS with explicit spin channels and integrated DOS."""

import io
import numpy as np
from sae._text import read_text
from sae.errors import ParseError


class TotalDOS:
    """Total DOS in OpenMX's three-column or five-column text format.

    ``density`` uses nonnegative down-spin values as in the historical SAE API;
    ``raw_density`` retains OpenMX's signed plotting convention. Integrated DOS
    is retained with its file sign and is never silently made absolute.
    """

    def __init__(self, energy, density, integrated):
        self.energy = np.asarray(energy, dtype=float).copy()
        self.raw_density = np.asarray(density, dtype=float).copy()
        self.integrated = np.asarray(integrated, dtype=float).copy()
        if (
            self.energy.ndim != 1
            or len(self.energy) < 1
            or self.raw_density.ndim != 2
            or self.raw_density.shape != self.integrated.shape
            or self.raw_density.shape[0] != len(self.energy)
            or self.raw_density.shape[1] not in (1, 2)
        ):
            raise ValueError("Expected energy (n,) and density/integrated (n, 1 or 2)")
        if not all(
            np.isfinite(a).all()
            for a in (self.energy, self.raw_density, self.integrated)
        ):
            raise ValueError("DOS arrays must be finite")
        if (np.diff(self.energy) <= 0).any():
            raise ValueError("DOS energy grid must be strictly increasing")

    @classmethod
    def read(cls, path):
        try:
            data = np.loadtxt(io.StringIO(read_text(path)), ndmin=2)
            if data.shape[1] not in (3, 5):
                raise ValueError("OpenMX total DOS needs 3 or 5 columns")
            nspin = (data.shape[1] - 1) // 2
            return cls(data[:, 0], data[:, 1 : 1 + nspin], data[:, 1 + nspin :])
        except ValueError as error:
            raise ParseError("Invalid OpenMX total DOS: {}".format(error)) from error

    @property
    def nspin(self):
        return self.raw_density.shape[1]

    @property
    def density(self):
        return np.abs(self.raw_density)

    def shifted(self, energy_reference):
        return type(self)(
            self.energy - float(energy_reference), self.raw_density, self.integrated
        )

    def integrate(self, emin=None, emax=None, spin=None):
        """Integrate density, interpolating requested endpoints within the grid."""
        lo = self.energy[0] if emin is None else float(emin)
        hi = self.energy[-1] if emax is None else float(emax)
        if not self.energy[0] <= lo < hi <= self.energy[-1]:
            raise ValueError("Integration bounds must lie inside the energy grid")
        if spin is not None and spin not in range(self.nspin):
            raise ValueError("Invalid spin channel")
        grid = np.r_[lo, self.energy[(self.energy > lo) & (self.energy < hi)], hi]
        values = np.column_stack(
            [np.interp(grid, self.energy, d) for d in self.density.T]
        )
        result = np.sum(
            (values[1:] + values[:-1]) * np.diff(grid)[:, None] / 2.0, axis=0
        )
        return result if spin is None else float(result[spin])
