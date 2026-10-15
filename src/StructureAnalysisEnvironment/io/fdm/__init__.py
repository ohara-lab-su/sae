"""Historical API. New code should import from sae.<calculation_code>."""
from importlib import import_module as _import_module

_EXPORTS = {'ReadFdmTxt': ('sae.fdmnes.spectra.absorption', 'AbsorptionSpectrum'), 'plot_fdm_xas': ('sae.fdmnes.spectra.convolution', 'plot_fdm_xas'), 'options': ('sae.fdmnes.writer', 'options'), 'ReadFdmConv': ('sae.fdmnes.spectra.convolution', 'ConvolvedSpectrum'), 'ReadFdmInp': ('sae.fdmnes.input', 'Input'), 'ReadFdmBav': ('sae.fdmnes.output.dispatch', 'Output'), 'ReadFdmBav2016': ('sae.fdmnes.output.v2016', 'Output2016'), 'ReadFdmBav2020': ('sae.fdmnes.output.v2020', 'Output2020'), 'ReadFdmSd': ('sae.fdmnes.dos.dispatch', 'DensityOfStates'), 'ReadFdmSd2016': ('sae.fdmnes.dos.v2016', 'DensityOfStates2016'), 'ReadFdmSd2020': ('sae.fdmnes.dos.v2020', 'DensityOfStates2020'), 'ReadFdmFdmfile': ('sae.fdmnes.batch', 'BatchInput'), 'WriteFdmInp': ('sae.fdmnes.writer', 'InputWriter'), 'WriteFdmfile': ('sae.fdmnes.batch_writer', 'BatchWriter')}
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
