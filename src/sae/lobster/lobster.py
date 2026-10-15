# Copyright Kengo NAKADA; SAE class library.
"""LOBSTER owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class LOBSTER:
    """LOBSTER calculation and its structure, results and analysis objects."""

    def __init__(self):
        self.output = None
        self.dos = None
        self.cohp = None

    def read_output(self, name="lobsterout"):
        """Create ReadLobOut; retain it as output and return it."""
        from sae.lobster.out import ReadLobOut

        value = ReadLobOut(name)
        self.output = value
        return value

    def read_dos(self, name="DOSCAR.lobster"):
        """Create ReadLobDos; retain it as dos and return it."""
        from sae.lobster.doscar import ReadLobDos

        value = ReadLobDos(name)
        self.dos = value
        return value

    def read_cohp(self, name="COHPCAR.lobster"):
        """Create ReadLobCohp; retain it as cohp and return it."""
        from sae.lobster.cohpcar import ReadLobCohp

        value = ReadLobCohp(name)
        self.cohp = value
        return value

    def get_tdos(self, spin=0):
        """Apply ReadLobDos.get_tdos."""
        return require(self.dos, "dos").get_tdos(spin)

    def get_ldos(self, l=0, atom=0, spin=0):
        """Apply ReadLobDos.get_ldos."""
        return require(self.dos, "dos").get_ldos(l, atom, spin)

    def get_pdos(self, lm=0, atom=0, spin=0):
        """Apply ReadLobDos.get_pdos."""
        return require(self.dos, "dos").get_pdos(lm, atom, spin)

    def get_pdos_sum(self, start, end, atom=0, spin=0):
        """Apply ReadLobDos.get_pdos_sum."""
        return require(self.dos, "dos").get_pdos_sum(start, end, atom, spin)

    def get_cohp(self, bond=0, spin=0):
        """Apply ReadLobCohp.get_cohp."""
        return require(self.cohp, "cohp").get_cohp(bond, spin)

    def get_icohp(self, bond=0, spin=0):
        """Apply ReadLobCohp.get_icohp."""
        return require(self.cohp, "cohp").get_icohp(bond, spin)

    def get_bond_leng(self):
        """Apply ReadLobCohp.get_bond_leng."""
        return require(self.cohp, "cohp").get_bond_leng()
