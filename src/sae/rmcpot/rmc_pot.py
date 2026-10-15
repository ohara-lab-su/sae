# Copyright Kengo NAKADA; SAE class library.
"""RMC_POT owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class RMC_POT:
    """RMC_POT calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(
        self, cname="POSCAR.cfg", suffix=".cfg", sort=False, atoms_index=None
    ):
        """Create ReadRmcpotCfg; retain it as structure and return it."""
        from sae.rmcpot.cfg import ReadRmcpotCfg

        value = ReadRmcpotCfg(cname, suffix, sort, atoms_index)
        self.structure = value
        return value

    def get_comment(self):
        """Apply ReadRmcpotCfg.get_comment."""
        return require(self.structure, "structure").get_comment()

    def conv_cfg2vasp(self):
        """Apply ReadRmcpotCfg.conv_cfg2vasp."""
        return require(self.structure, "structure").conv_cfg2vasp()

    def get_title(self):
        """Apply ReadRmcpotCfg.get_title."""
        return require(self.structure, "structure").get_title()

    def get_system(self):
        """Apply ReadRmcpotCfg.get_system."""
        return require(self.structure, "structure").get_system()

    def get_scale(self):
        """Apply ReadRmcpotCfg.get_scale."""
        return require(self.structure, "structure").get_scale()

    def get_t(self):
        """Apply ReadRmcpotCfg.get_t."""
        return require(self.structure, "structure").get_t()

    def get_vasp_version(self):
        """Apply ReadRmcpotCfg.get_vasp_version."""
        return require(self.structure, "structure").get_vasp_version()

    def get_atoms(self):
        """Apply ReadRmcpotCfg.get_atoms."""
        return require(self.structure, "structure").get_atoms()

    def get_atoms_j(self):
        """Apply ReadRmcpotCfg.get_atoms_j."""
        return require(self.structure, "structure").get_atoms_j()

    def get_atoms_index(self):
        """Apply ReadRmcpotCfg.get_atoms_index."""
        return require(self.structure, "structure").get_atoms_index()

    def get_atoms_number(self):
        """Apply ReadRmcpotCfg.get_atoms_number."""
        return require(self.structure, "structure").get_atoms_number()

    def get_atoms_index_j(self):
        """Apply ReadRmcpotCfg.get_atoms_index_j."""
        return require(self.structure, "structure").get_atoms_index_j()

    def get_atoms_number_j(self):
        """Apply ReadRmcpotCfg.get_atoms_number_j."""
        return require(self.structure, "structure").get_atoms_number_j()

    def get_nion(self):
        """Apply ReadRmcpotCfg.get_nion."""
        return require(self.structure, "structure").get_nion()

    def get_natom(self):
        """Apply ReadRmcpotCfg.get_natom."""
        return require(self.structure, "structure").get_natom()

    def get_ion(self):
        """Apply ReadRmcpotCfg.get_ion."""
        return require(self.structure, "structure").get_ion()

    def get_ion_local(self):
        """Apply ReadRmcpotCfg.get_ion_local."""
        return require(self.structure, "structure").get_ion_local()

    def get_selective(self):
        """Apply ReadRmcpotCfg.get_selective."""
        return require(self.structure, "structure").get_selective()

    def get_direct(self):
        """Apply ReadRmcpotCfg.get_direct."""
        return require(self.structure, "structure").get_direct()

    def get_position(self):
        """Apply ReadRmcpotCfg.get_position."""
        return require(self.structure, "structure").get_position()

    def get_fix(self):
        """Apply ReadRmcpotCfg.get_fix."""
        return require(self.structure, "structure").get_fix()

    def write(
        self,
        outname=None,
        suffix=None,
        code="RMC_POT",
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
