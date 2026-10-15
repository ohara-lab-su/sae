"""sae.fdmnes classes."""

from importlib import import_module as _import_module

_EXPORTS = {
    "Input": ("sae.fdmnes.input", "Input"),
    "InputWriter": ("sae.fdmnes.writer", "InputWriter"),
    "BatchInput": ("sae.fdmnes.batch", "BatchInput"),
    "BatchWriter": ("sae.fdmnes.batch_writer", "BatchWriter"),
    "AbsorptionSpectrum": ("sae.fdmnes.spectra.absorption", "AbsorptionSpectrum"),
    "ConvolvedSpectrum": ("sae.fdmnes.spectra.convolution", "ConvolvedSpectrum"),
    "Output": ("sae.fdmnes.output.dispatch", "Output"),
    "Output2016": ("sae.fdmnes.output.v2016", "Output2016"),
    "Output2020": ("sae.fdmnes.output.v2020", "Output2020"),
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
