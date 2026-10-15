"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'Logger': ('StructureAnalysisEnvironment.util.logger', 'Logger'), 'get_loglevel_object': ('StructureAnalysisEnvironment.util.logger_support', 'get_loglevel_object'), 'init_logger': ('StructureAnalysisEnvironment.util.logger_support', 'init_logger')}
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
