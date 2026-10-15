"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'ReadMd': ('sae.openmx.trajectory', 'Trajectory'), 'ReadMxVps': ('sae.openmx.pseudopotential.file', 'Pseudopotential'), 'ReadMxVpsList': ('sae.openmx.pseudopotential.catalog', 'PseudopotentialCatalog'), 'ReadMxDatMethod': ('sae.openmx._structure', 'StructureMethods'), 'ReadMxDat': ('sae.openmx.input_legacy', 'LegacyInput'), 'options': ('sae.openmx.input_legacy', 'options'), 'ReadMxOut': ('sae.openmx.output', 'Output'), 'ReadMxDftscf': ('sae.openmx.scf', 'SCFHistory'), 'ReadMxDosMethod': ('sae.openmx.dos._base', 'DOSMethods'), 'ReadMxTdos': ('sae.openmx.dos.total_legacy', 'LegacyTotalDOS'), 'ReadMxPdos': ('sae.openmx.dos.projected', 'ProjectedDOS')}
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
