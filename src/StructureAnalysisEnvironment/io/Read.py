"""Compatibility dispatcher. Code-specific readers are the primary API."""
from importlib import import_module


class Read:
    _READERS = {
        'VASP': ('sae.vasp.structure_legacy', 'LegacyPoscar', 'POSCAR'),
        'OPENMX': ('sae.openmx.input_legacy', 'LegacyInput', 'openmx.dat'),
        'FDMNES': ('sae.fdmnes.input', 'Input', 'read_pdb.inp'),
        'RMC_POT': ('sae.rmcpot.configuration', 'Configuration', 'rmcpot.cfg'),
        'PWSCF': ('sae.quantum_espresso.input', 'Input', 'scf.in'),
        'HILAPW': ('sae.hilapw.input_legacy', 'LegacyInput', 'sets.in'),
    }
    _ALIASES = {'MX': 'OPENMX', 'FDM': 'FDMNES', 'RMC': 'RMC_POT',
                'QE': 'PWSCF', 'QUANTUMESPRESSO': 'PWSCF', 'HI': 'HILAPW'}

    def __init__(self, filename=None, suffix=None, code='VASP', sort=False, atoms_index=None):
        self.code = self._ALIASES.get(code.upper(), code.upper())
        if self.code not in self._READERS:
            raise ValueError('No structure reader registered for ' + code)
        module, name, default = self._READERS[self.code]
        reader = getattr(import_module(module), name)
        kwargs = {} if self.code == 'HILAPW' else {'sort': sort, 'atoms_index': atoms_index}
        if suffix is not None and self.code != 'HILAPW':
            kwargs['suffix'] = suffix
        self.cell = reader(str(filename) if filename is not None else default, **kwargs)
        self.suffix = suffix

    def __getattr__(self, name):
        return getattr(self.cell, name)
