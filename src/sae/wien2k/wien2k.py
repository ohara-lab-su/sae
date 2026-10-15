# Copyright Kengo NAKADA; SAE class library.
"""WIEN2k owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class WIEN2k:
    """WIEN2k calculation and its structure, results and analysis objects."""

    def __init__(self):
        self.output0 = None
        self.outputt = None
        self.scf = None
        self.dos = None
        self.xspec = None
        self.txspec = None

    def read_output0(self, name):
        """Create ReadWienOutput0; retain it as output0 and return it."""
        from sae.wien2k.output0 import ReadWienOutput0

        value = ReadWienOutput0(name)
        self.output0 = value
        return value

    def read_outputt(self, name):
        """Create ReadWienOutputt; retain it as outputt and return it."""
        from sae.wien2k.outputt import ReadWienOutputt

        value = ReadWienOutputt(name)
        self.outputt = value
        return value

    def read_scf(self, case="case", suffix="scf"):
        """Create ReadWienScf; retain it as scf and return it."""
        from sae.wien2k.scf import ReadWienScf

        value = ReadWienScf(case, suffix)
        self.scf = value
        return value

    def read_dos(self, lists):
        """Create ReadWienDos; retain it as dos and return it."""
        from sae.wien2k.dos import ReadWienDos

        value = ReadWienDos(lists)
        self.dos = value
        return value

    def read_xspec(self, case="case", spin=None, suffix=".xspec"):
        """Create ReadWienXspec; retain it as xspec and return it."""
        from sae.wien2k.xspec import ReadWienXspec

        value = ReadWienXspec(case, spin, suffix)
        self.xspec = value
        return value

    def read_txspec(self, case="case", spin=None, suffix=".txspec"):
        """Create ReadWienTxspec; retain it as txspec and return it."""
        from sae.wien2k.txspec import ReadWienTxspec

        value = ReadWienTxspec(case, spin, suffix)
        self.txspec = value
        return value

    def get_raw_dos(self, atom=1, orbit="total", times=1.0):
        """Apply ReadWienDos.get_raw_dos."""
        return require(self.dos, "dos").get_raw_dos(atom, orbit, times)

    def get_ldos_ion(self, case="case", atom=1, orbit="total"):
        """Apply ReadWienDos.get_ldos_ion."""
        return require(self.dos, "dos").get_ldos_ion(case, atom, orbit)

    def get_eng(self):
        """Apply ReadWienDos.get_eng."""
        return require(self.dos, "dos").get_eng()

    def write_epl(self, ion=None):
        """Apply ReadWienScf.write_epl."""
        return require(self.scf, "scf").write_epl(ion)

    def write_eph(self, ion=None):
        """Apply ReadWienScf.write_eph."""
        return require(self.scf, "scf").write_eph(ion)

    def write_epar(self, ion=None, par=None, l=None):
        """Apply ReadWienScf.write_epar."""
        return require(self.scf, "scf").write_epar(ion, par, l)

    def get_xas(self):
        """Apply ReadWienXspec.get_xas."""
        return require(self.xspec, "xspec").get_xas()
