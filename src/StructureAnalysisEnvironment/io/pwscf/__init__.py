"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'ReadPwIn': ('sae.quantum_espresso.input', 'Input'), 'options': ('sae.quantum_espresso.spectra', 'options'), 'ReadPwOut': ('sae.quantum_espresso.output', 'Output'), 'ReadPwTdos': ('sae.quantum_espresso.dos.total', 'TotalDOS'), 'ReadPwPdos': ('sae.quantum_espresso.dos.projected', 'ProjectedDOS'), 'ReadPwXanes': ('sae.quantum_espresso.spectra', 'XANES')}
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
