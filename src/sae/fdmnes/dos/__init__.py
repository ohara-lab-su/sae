"""sae.fdmnes.dos classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "DensityOfStates": ("sae.fdmnes.dos.dispatch", "DensityOfStates"),
    "DensityOfStates2016": ("sae.fdmnes.dos.v2016", "DensityOfStates2016"),
    "DensityOfStates2020": ("sae.fdmnes.dos.v2020", "DensityOfStates2020"),
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
