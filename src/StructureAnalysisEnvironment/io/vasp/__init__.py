"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'ReadVaspOutcar': ('sae.vasp.output.outcar', 'Outcar'), 'ReadVaspDoscar': ('sae.vasp.dos', 'DensityOfStates'), 'ReadVaspXdat': ('sae.vasp.trajectory', 'Trajectory'), 'ReadVaspVasprun': ('sae.vasp.output.vasprun', 'Vasprun'), 'ReadVaspOszicar': ('sae.vasp.output.oszicar', 'Oszicar'), 'ReadVaspEigenval': ('sae.vasp.bands.eigenval', 'Eigenvalues'), 'ReadVaspKpoints': ('sae.vasp.kpoints', 'Kpoints'), 'ReadVaspSymdat': ('sae.vasp.symmetry', 'Symmetry'), 'ReadProcar': ('sae.vasp.bands.procar', 'Projections'), 'ReadVaspPoscar': ('sae.vasp.structure_legacy', 'LegacyPoscar'), 'ReadVaspIncar': ('sae.vasp.parameters', 'Incar'), 'ReadVaspAcf': ('sae.vasp.charges', 'Charges'), 'options': ('sae.vasp.pseudopotential', 'options'), 'ReadVaspPotcar': ('sae.vasp.pseudopotential', 'Potcar'), 'ReadVaspChgcar': ('sae.vasp.charge_density.reader', 'ChargeDensity'), 'WriteVaspChgcar': ('sae.vasp.charge_density.writer', 'Writer'), 'SumChgcar': ('sae.vasp.charge_density.operations', 'SumChargeDensity'), 'ReadVaspChgcarHeader': ('sae.vasp.charge_density.header', 'Header'), 'ReadVaspChgcarFooter': ('sae.vasp.charge_density.footer', 'Footer')}
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
