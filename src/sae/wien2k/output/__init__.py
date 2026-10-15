"""sae.wien2k.output classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "PotentialOutput": ("sae.wien2k.output.potential", "PotentialOutput"),
    "BandOutput": ("sae.wien2k.output.bands", "BandOutput"),
    "SCFHistory": ("sae.wien2k.output.scf", "SCFHistory"),
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
