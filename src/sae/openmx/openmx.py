# Copyright Kengo NAKADA; SAE class library.
"""OpenMX owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class OpenMX:
    """OpenMX calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        self.output = None
        self.scf = None
        self.trajectory = None
        self.tdos = None
        self.pdos = None
        self.vps = None
        self.vps_list = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(self, datname, suffix=".dat", sort=True, atoms_index=None):
        """Create ReadMxDat; retain it as structure and return it."""
        from sae.openmx.dat import ReadMxDat

        value = ReadMxDat(datname, suffix, sort, atoms_index)
        self.structure = value
        return value

    def read_output(self, cname):
        """Create ReadMxOut; retain it as output and return it."""
        from sae.openmx.out import ReadMxOut

        value = ReadMxOut(cname)
        self.output = value
        return value

    def read_scf(self, cname):
        """Create ReadMxDftscf; retain it as scf and return it."""
        from sae.openmx.dftscf import ReadMxDftscf

        value = ReadMxDftscf(cname)
        self.scf = value
        return value

    def read_trajectory(self, cname):
        """Create ReadMd; retain it as trajectory and return it."""
        from sae.openmx.md import ReadMd

        value = ReadMd(cname)
        self.trajectory = value
        return value

    def read_tdos(self, name, suffix):
        """Create ReadMxTdos; retain it as tdos and return it."""
        from sae.openmx.tdos import ReadMxTdos

        value = ReadMxTdos(name, suffix)
        self.tdos = value
        return value

    def read_pdos(self, name, suffix):
        """Create ReadMxPdos; retain it as pdos and return it."""
        from sae.openmx.pdos import ReadMxPdos

        value = ReadMxPdos(name, suffix)
        self.pdos = value
        return value

    def read_vps(self, fullname):
        """Create ReadMxVps; retain it as vps and return it."""
        from sae.openmx.vps import ReadMxVps

        value = ReadMxVps(fullname)
        self.vps = value
        return value

    def read_vps_list(self, name):
        """Create ReadMxVpsList; retain it as vps_list and return it."""
        from sae.openmx.vps_list import ReadMxVpsList

        value = ReadMxVpsList(name)
        self.vps_list = value
        return value

    def get_utot(self):
        """Apply ReadMxOut.get_utot."""
        return require(self.output, "output").get_utot()

    def get_n_ion_loop(self):
        """Apply ReadMxOut.get_n_ion_loop."""
        return require(self.output, "output").get_n_ion_loop()

    def get_max_n_scf(self):
        """Apply ReadMxOut.get_max_n_scf."""
        return require(self.output, "output").get_max_n_scf()

    def get_uele(self):
        """Apply ReadMxOut.get_uele."""
        return require(self.output, "output").get_uele()

    def get_tdos(self, spin=0):
        """Apply ReadMxTdos.get_tdos."""
        return require(self.tdos, "tdos").get_tdos(spin)

    def get_inttdos(self, spin=0):
        """Apply ReadMxTdos.get_inttdos."""
        return require(self.tdos, "tdos").get_inttdos(spin)

    def get_pdos(self, lm=0, atom=0, spin=0):
        """Apply ReadMxPdos.get_pdos."""
        return require(self.pdos, "pdos").get_pdos(lm, atom, spin)

    def get_ldos(self, l=0, atom=0, spin=0):
        """Apply ReadMxPdos.get_ldos."""
        return require(self.pdos, "pdos").get_ldos(l, atom, spin)

    def get_tdos_spd(self, l=0, spin=0):
        """Apply ReadMxPdos.get_tdos_spd."""
        return require(self.pdos, "pdos").get_tdos_spd(l, spin)

    def get_ldos_ion(self, l=0, ion=0, spin=0):
        """Apply ReadMxPdos.get_ldos_ion."""
        return require(self.pdos, "pdos").get_ldos_ion(l, ion, spin)

    def get_title(self):
        """Apply ReadMxDat.get_title."""
        return require(self.structure, "structure").get_title()

    def get_system(self):
        """Apply ReadMxDat.get_system."""
        return require(self.structure, "structure").get_system()

    def get_scale(self):
        """Apply ReadMxDat.get_scale."""
        return require(self.structure, "structure").get_scale()

    def get_t(self):
        """Apply ReadMxDat.get_t."""
        return require(self.structure, "structure").get_t()

    def get_vasp_version(self):
        """Apply ReadMxDat.get_vasp_version."""
        return require(self.structure, "structure").get_vasp_version()

    def get_atoms(self):
        """Apply ReadMxDat.get_atoms."""
        return require(self.structure, "structure").get_atoms()

    def get_atoms_j(self):
        """Apply ReadMxDat.get_atoms_j."""
        return require(self.structure, "structure").get_atoms_j()

    def get_atoms_index(self):
        """Apply ReadMxDat.get_atoms_index."""
        return require(self.structure, "structure").get_atoms_index()

    def get_atoms_number(self):
        """Apply ReadMxDat.get_atoms_number."""
        return require(self.structure, "structure").get_atoms_number()

    def get_atoms_index_j(self):
        """Apply ReadMxDat.get_atoms_index_j."""
        return require(self.structure, "structure").get_atoms_index_j()

    def get_atoms_number_j(self):
        """Apply ReadMxDat.get_atoms_number_j."""
        return require(self.structure, "structure").get_atoms_number_j()

    def get_nion(self):
        """Apply ReadMxDat.get_nion."""
        return require(self.structure, "structure").get_nion()

    def get_natom(self):
        """Apply ReadMxDat.get_natom."""
        return require(self.structure, "structure").get_natom()

    def get_ion(self):
        """Apply ReadMxDat.get_ion."""
        return require(self.structure, "structure").get_ion()

    def get_ion_local(self):
        """Apply ReadMxDat.get_ion_local."""
        return require(self.structure, "structure").get_ion_local()

    def get_selective(self):
        """Apply ReadMxDat.get_selective."""
        return require(self.structure, "structure").get_selective()

    def get_direct(self):
        """Apply ReadMxDat.get_direct."""
        return require(self.structure, "structure").get_direct()

    def get_position(self):
        """Apply ReadMxDat.get_position."""
        return require(self.structure, "structure").get_position()

    def get_fix(self):
        """Apply ReadMxDat.get_fix."""
        return require(self.structure, "structure").get_fix()

    def get_ispin(self):
        """Apply ReadMxDat.get_ispin."""
        return require(self.structure, "structure").get_ispin()

    def write(
        self,
        outname=None,
        suffix=None,
        code="OPENMX",
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
