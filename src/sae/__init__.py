# Copyright Kengo NAKADA; SAE class library.
"""Code classes built on the original SAE algorithms."""

from importlib import import_module

_CLASSES = {
    "VASP": "sae.vasp",
    "OpenMX": "sae.openmx",
    "FDMNES": "sae.fdmnes",
    "HiLAPW": "sae.hilapw",
    "PWscf": "sae.pwscf",
    "WIEN2k": "sae.wien2k",
    "RMC_POT": "sae.rmcpot",
    "LOBSTER": "sae.lobster",
    "Bader": "sae.bader",
    "Athena": "sae.athena",
    "PF": "sae.pf",
}
__all__ = list(_CLASSES)


def __getattr__(name):
    if name not in _CLASSES:
        raise AttributeError(name)
    value = getattr(import_module(_CLASSES[name]), name)
    globals()[name] = value
    return value


__version__ = "0.1.0"
