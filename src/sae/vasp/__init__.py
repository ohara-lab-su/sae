"""sae.vasp classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "LegacyPoscar": ("sae.vasp.structure_legacy", "LegacyPoscar"),
    "Incar": ("sae.vasp.parameters", "Incar"),
    "Kpoints": ("sae.vasp.kpoints", "Kpoints"),
    "Potcar": ("sae.vasp.pseudopotential", "Potcar"),
    "Outcar": ("sae.vasp.output.outcar", "Outcar"),
    "Oszicar": ("sae.vasp.output.oszicar", "Oszicar"),
    "Vasprun": ("sae.vasp.output.vasprun", "Vasprun"),
    "Eigenvalues": ("sae.vasp.bands.eigenval", "Eigenvalues"),
    "Projections": ("sae.vasp.bands.procar", "Projections"),
    "DensityOfStates": ("sae.vasp.dos", "DensityOfStates"),
    "Trajectory": ("sae.vasp.trajectory", "Trajectory"),
    "Symmetry": ("sae.vasp.symmetry", "Symmetry"),
    "Charges": ("sae.vasp.charges", "Charges"),
    "ChargeDensity": ("sae.vasp.charge_density.reader", "ChargeDensity"),
    "Header": ("sae.vasp.charge_density.header", "Header"),
    "Footer": ("sae.vasp.charge_density.footer", "Footer"),
    "Writer": ("sae.vasp.charge_density.writer", "Writer"),
    "SumChargeDensity": ("sae.vasp.charge_density.operations", "SumChargeDensity"),
    "Poscar": ("sae.vasp.structure", "Poscar"),
}
__all__ = list(_EXPORTS)


def __getattr__(name):
    if name not in _EXPORTS:
        raise AttributeError("{} has no attribute {!r}".format(__name__, name))
    module, attribute = _EXPORTS[name]
    value = getattr(_import_module(module), attribute)
    globals()[name] = value
    return value


def __dir__():
    return sorted(set(globals()) | set(__all__))
