"""sae.vasp.charge_density classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "ChargeDensity": ("sae.vasp.charge_density.reader", "ChargeDensity"),
    "Header": ("sae.vasp.charge_density.header", "Header"),
    "Footer": ("sae.vasp.charge_density.footer", "Footer"),
    "Writer": ("sae.vasp.charge_density.writer", "Writer"),
    "SumChargeDensity": ("sae.vasp.charge_density.operations", "SumChargeDensity"),
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
