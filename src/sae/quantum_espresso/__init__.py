"""sae.quantum_espresso classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "Input": ("sae.quantum_espresso.input", "Input"),
    "Output": ("sae.quantum_espresso.output", "Output"),
    "TotalDOS": ("sae.quantum_espresso.dos.total", "TotalDOS"),
    "ProjectedDOS": ("sae.quantum_espresso.dos.projected", "ProjectedDOS"),
    "XANES": ("sae.quantum_espresso.spectra", "XANES"),
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
