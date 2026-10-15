"""sae.rmcpot classes."""

from importlib import import_module as _import_module

_EXPORTS = {"Configuration": ("sae.rmcpot.configuration", "Configuration")}
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
