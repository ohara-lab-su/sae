"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'write_fdmnes': ('StructureAnalysisEnvironment.io.ase_support.fdmnes', 'write_fdmnes'), 'write_fdmnes_inp': ('StructureAnalysisEnvironment.io.ase_support.fdmnes', 'write_fdmnes_inp'), 'options': ('StructureAnalysisEnvironment.io.ase_support.fdmnes', 'options')}
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
