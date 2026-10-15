# Copyright Kengo NAKADA; SAE class library.
"""PWscf owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class PWscf:
    """PWscf calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        self.output = None
        self.tdos = None
        self.pdos = None
        self.xanes = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(self, cname, suffix=".in", sort=False, atoms_index=None):
        """Create ReadPwIn; retain it as structure and return it."""
        from sae.pwscf.inp import ReadPwIn

        value = ReadPwIn(cname, suffix, sort, atoms_index)
        self.structure = value
        return value

    def read_output(self, cname):
        """Create ReadPwOut; retain it as output and return it."""
        from sae.pwscf.out import ReadPwOut

        value = ReadPwOut(cname)
        self.output = value
        return value

    def read_tdos(self, cname="input.dos"):
        """Create ReadPwTdos; retain it as tdos and return it."""
        from sae.pwscf.tdos import ReadPwTdos

        value = ReadPwTdos(cname)
        self.tdos = value
        return value

    def read_pdos(self, prefix):
        """Create ReadPwPdos; retain it as pdos and return it."""
        from sae.pwscf.pdos import ReadPwPdos

        value = ReadPwPdos(prefix)
        self.pdos = value
        return value

    def read_xanes(self, cname="xanes.dat"):
        """Create ReadPwXanes; retain it as xanes and return it."""
        from sae.pwscf.xanes import ReadPwXanes

        value = ReadPwXanes(cname)
        self.xanes = value
        return value

    def get_toten_ion(self):
        """Apply ReadPwOut.get_toten_ion."""
        return require(self.output, "output").get_toten_ion()

    def get_energy_loop(self):
        """Apply ReadPwOut.get_energy_loop."""
        return require(self.output, "output").get_energy_loop()

    def get_force_loop(self):
        """Apply ReadPwOut.get_force_loop."""
        return require(self.output, "output").get_force_loop()

    def get_tdos(self, spin=0):
        """Apply ReadPwTdos.get_tdos."""
        return require(self.tdos, "tdos").get_tdos(spin)

    def get_inttdos(self, spin=0):
        """Apply ReadPwTdos.get_inttdos."""
        return require(self.tdos, "tdos").get_inttdos(spin)

    def get_ldos(self, l=0, atom=0, spin=0):
        """Apply ReadPwPdos.get_ldos."""
        return require(self.pdos, "pdos").get_ldos(l, atom, spin)

    def get_pdos(self, l=0, lm=0, atom=0, spin=0):
        """Apply ReadPwPdos.get_pdos."""
        return require(self.pdos, "pdos").get_pdos(l, lm, atom, spin)

    def get_xas(self):
        """Apply ReadPwXanes.get_xas."""
        return require(self.xanes, "xanes").get_xas()

    def get_title(self):
        """Apply ReadPwIn.get_title."""
        return require(self.structure, "structure").get_title()

    def get_system(self):
        """Apply ReadPwIn.get_system."""
        return require(self.structure, "structure").get_system()

    def get_scale(self):
        """Apply ReadPwIn.get_scale."""
        return require(self.structure, "structure").get_scale()

    def get_t(self):
        """Apply ReadPwIn.get_t."""
        return require(self.structure, "structure").get_t()

    def get_vasp_version(self):
        """Apply ReadPwIn.get_vasp_version."""
        return require(self.structure, "structure").get_vasp_version()

    def get_atoms(self):
        """Apply ReadPwIn.get_atoms."""
        return require(self.structure, "structure").get_atoms()

    def get_atoms_j(self):
        """Apply ReadPwIn.get_atoms_j."""
        return require(self.structure, "structure").get_atoms_j()

    def get_atoms_index(self):
        """Apply ReadPwIn.get_atoms_index."""
        return require(self.structure, "structure").get_atoms_index()

    def get_atoms_number(self):
        """Apply ReadPwIn.get_atoms_number."""
        return require(self.structure, "structure").get_atoms_number()

    def get_atoms_index_j(self):
        """Apply ReadPwIn.get_atoms_index_j."""
        return require(self.structure, "structure").get_atoms_index_j()

    def get_atoms_number_j(self):
        """Apply ReadPwIn.get_atoms_number_j."""
        return require(self.structure, "structure").get_atoms_number_j()

    def get_nion(self):
        """Apply ReadPwIn.get_nion."""
        return require(self.structure, "structure").get_nion()

    def get_natom(self):
        """Apply ReadPwIn.get_natom."""
        return require(self.structure, "structure").get_natom()

    def get_ion(self):
        """Apply ReadPwIn.get_ion."""
        return require(self.structure, "structure").get_ion()

    def get_ion_local(self):
        """Apply ReadPwIn.get_ion_local."""
        return require(self.structure, "structure").get_ion_local()

    def get_selective(self):
        """Apply ReadPwIn.get_selective."""
        return require(self.structure, "structure").get_selective()

    def get_direct(self):
        """Apply ReadPwIn.get_direct."""
        return require(self.structure, "structure").get_direct()

    def get_position(self):
        """Apply ReadPwIn.get_position."""
        return require(self.structure, "structure").get_position()

    def get_fix(self):
        """Apply ReadPwIn.get_fix."""
        return require(self.structure, "structure").get_fix()

    def get_ispin(self):
        """Apply ReadPwIn.get_ispin."""
        return require(self.structure, "structure").get_ispin()

    def get_ibrav(self):
        """Apply ReadPwIn.get_ibrav."""
        return require(self.structure, "structure").get_ibrav()

    def write(
        self,
        outname=None,
        suffix=None,
        code="PWSCF",
        calinfo=None,
        sort=False,
        STD=False,
        MOL=False,
        FRAC=True,
    ):
        """Use the original write dispatcher and its original conversion routines."""
        from sae.structure.writer import StructureWriter

        write = StructureWriter().write
        return StructureWriter().write(
            require(self.structure, "structure"),
            outname=outname,
            suffix=suffix,
            code=code,
            calinfo=calinfo,
            sort=sort,
            STD=STD,
            MOL=MOL,
            FRAC=FRAC,
        )
