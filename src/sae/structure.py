"""Geometry shared across codes. Cell vectors are rows; lengths are angstrom."""

from itertools import product
from typing import Sequence
import numpy as np


class Structure:
    """Atomic geometry with validated state and coordinate operations.

    Code-specific settings belong to their input/result object, not this class.
    Cartesian positions and row cell vectors are stored in angstrom.
    """

    def __init__(self, symbols: Sequence[str], positions, cell, fractional=False):
        self._symbols = tuple(str(s) for s in symbols)
        if any(not s or any(c.isspace() for c in s) for s in self._symbols):
            raise ValueError("Each site requires a nonempty species label")
        self._cell = self._validated_cell(cell)
        positions = np.asarray(positions, dtype=float)
        if (
            positions.shape != (len(self._symbols), 3)
            or not np.isfinite(positions).all()
        ):
            raise ValueError("positions must be a finite (number of sites, 3) array")
        self._positions = positions.dot(self._cell) if fractional else positions.copy()

    @staticmethod
    def _validated_cell(cell):
        value = np.array(cell, dtype=float, copy=True)
        if value.shape != (3, 3) or not np.isfinite(value).all():
            raise ValueError("cell must be a finite 3 x 3 matrix of row vectors")
        if np.linalg.matrix_rank(value) != 3:
            raise ValueError("cell vectors must be linearly independent")
        return value

    def __len__(self):
        return len(self._symbols)

    @property
    def symbols(self):
        return self._symbols

    @property
    def cell(self):
        return self._cell.copy()

    @property
    def positions(self):
        return self._positions.copy()

    @property
    def fractional_positions(self):
        return np.linalg.solve(self._cell.T, self._positions.T).T

    @property
    def volume(self):
        return float(abs(np.linalg.det(self._cell)))

    def copy(self):
        return type(self)(self.symbols, self.positions, self.cell)

    def translate(self, vector, fractional=False):
        vector = np.asarray(vector, dtype=float)
        if vector.shape != (3,) or not np.isfinite(vector).all():
            raise ValueError("translation must contain three finite values")
        self._positions += vector.dot(self._cell) if fractional else vector
        return self

    def wrap(self):
        self._positions = (self.fractional_positions % 1.0).dot(self._cell)
        return self

    def set_cell(self, cell, scale_positions=False):
        cell = self._validated_cell(cell)
        positions = (
            self.fractional_positions.dot(cell) if scale_positions else self.positions
        )
        self._cell, self._positions = cell, positions
        return self

    def repeat(self, repetitions):
        repeats = np.asarray(repetitions)
        if (
            repeats.shape != (3,)
            or not np.issubdtype(repeats.dtype, np.integer)
            or (repeats < 1).any()
        ):
            raise ValueError("repetitions must be three positive integers")
        offsets = np.asarray(list(product(*(range(int(n)) for n in repeats))))
        positions = self._positions[None, :, :] + offsets.dot(self._cell)[:, None, :]
        return type(self)(
            self.symbols * len(offsets),
            positions.reshape(-1, 3),
            self._cell * repeats[:, None],
        )

    def select(self, indices):
        indices = list(indices)
        return type(self)(
            [self.symbols[i] for i in indices], self.positions[indices], self.cell
        )

    def to_ase(self):
        from ase import Atoms

        return Atoms(
            symbols=self.symbols, positions=self.positions, cell=self.cell, pbc=True
        )

    @classmethod
    def from_ase(cls, atoms):
        if not all(atoms.pbc):
            raise ValueError("Structure currently represents fully periodic cells")
        return cls(atoms.get_chemical_symbols(), atoms.positions, atoms.cell)


def cell_from_parameters(parameters):
    """Build row cell vectors from a, b, c, alpha, beta, gamma (degrees)."""
    p = np.asarray(parameters, dtype=float)
    if p.shape != (6,) or not np.isfinite(p).all() or (p[:3] <= 0).any():
        raise ValueError("Expected positive lengths and three finite angles")
    if (p[3:] <= 0).any() or (p[3:] >= 180).any():
        raise ValueError("Cell angles must lie strictly between 0 and 180 degrees")
    a, b, c = p[:3]
    alpha, beta, gamma = np.deg2rad(p[3:])
    cx = c * np.cos(beta)
    cy = c * (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
    cz2 = c * c - cx * cx - cy * cy
    if cz2 <= 0:
        raise ValueError("Cell angles do not define a nondegenerate cell")
    return np.array(
        [[a, 0, 0], [b * np.cos(gamma), b * np.sin(gamma), 0], [cx, cy, np.sqrt(cz2)]]
    )
