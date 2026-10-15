# Copyright Kengo NAKADA; SAE class library.
"""VASP owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class VASP:
    """VASP calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        self.incar = None
        self.kpoints = None
        self.potcar = None
        self.output = None
        self.oszicar = None
        self.vasprun = None
        self.trajectory = None
        self.dos = None
        self.eigenval = None
        self.procar = None
        self.symmetry = None
        self.charges = None
        self.charge_density = None
        self.charge_header = None
        self.charge_footer = None
        self.charge_writer = None
        self.charge_sum = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(
        self,
        POSCAR="POSCAR",
        suffix=".vasp",
        sort=False,
        atoms_index=None,
        code=None,
        logger=None,
    ):
        """Create ReadVaspPoscar; retain it as structure and return it."""
        from sae.vasp.poscar import ReadVaspPoscar

        value = ReadVaspPoscar(POSCAR, suffix, sort, atoms_index, code, logger)
        self.structure = value
        return value

    def read_incar(self, INCAR="INCAR", logger=None):
        """Create ReadVaspIncar; retain it as incar and return it."""
        from sae.vasp.incar import ReadVaspIncar

        value = ReadVaspIncar(INCAR, logger)
        self.incar = value
        return value

    def read_kpoints(self, KPOINTS="KPOINTS"):
        """Create ReadVaspKpoints; retain it as kpoints and return it."""
        from sae.vasp.kpoints import ReadVaspKpoints

        value = ReadVaspKpoints(KPOINTS)
        self.kpoints = value
        return value

    def read_potcar(self, POTCAR="POTCAR", logger=None):
        """Create ReadVaspPotcar; retain it as potcar and return it."""
        from sae.vasp.potcar import ReadVaspPotcar

        value = ReadVaspPotcar(POTCAR, logger)
        self.potcar = value
        return value

    def read_output(self, cname):
        """Create ReadVaspOutcar; retain it as output and return it."""
        from sae.vasp.outcar import ReadVaspOutcar

        value = ReadVaspOutcar(cname)
        self.output = value
        return value

    def read_oszicar(self, cname):
        """Create ReadVaspOszicar; retain it as oszicar and return it."""
        from sae.vasp.oszicar import ReadVaspOszicar

        value = ReadVaspOszicar(cname)
        self.oszicar = value
        return value

    def read_vasprun(self, name="vasprun.xml"):
        """Create ReadVaspVasprun; retain it as vasprun and return it."""
        from sae.vasp.vasprun import ReadVaspVasprun

        value = ReadVaspVasprun(name)
        self.vasprun = value
        return value

    def read_trajectory(self, name):
        """Create ReadVaspXdat; retain it as trajectory and return it."""
        from sae.vasp.xdatcar import ReadVaspXdat

        value = ReadVaspXdat(name)
        self.trajectory = value
        return value

    def read_dos(self, name="DOSCAR"):
        """Create ReadVaspDoscar; retain it as dos and return it."""
        from sae.vasp.doscar import ReadVaspDoscar

        value = ReadVaspDoscar(name)
        self.dos = value
        return value

    def read_eigenval(self, name):
        """Create ReadVaspEigenval; retain it as eigenval and return it."""
        from sae.vasp.eigenval import ReadVaspEigenval

        value = ReadVaspEigenval(name)
        self.eigenval = value
        return value

    def read_procar(self, name):
        """Create ReadProcar; retain it as procar and return it."""
        from sae.vasp.procar import ReadProcar

        value = ReadProcar(name)
        self.procar = value
        return value

    def read_symmetry(self, name):
        """Create ReadVaspSymdat; retain it as symmetry and return it."""
        from sae.vasp.symdat import ReadVaspSymdat

        value = ReadVaspSymdat(name)
        self.symmetry = value
        return value

    def read_charges(self, poscar=None, potcar=None, acf="ACF.dat"):
        """Create ReadVaspAcf; retain it as charges and return it."""
        from sae.vasp.acf import ReadVaspAcf

        value = ReadVaspAcf(poscar, potcar, acf)
        self.charges = value
        return value

    def read_charge_density(
        self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None, logger=None
    ):
        """Create ReadVaspChgcar; retain it as charge_density and return it."""
        from sae.vasp.chgcar import ReadVaspChgcar

        value = ReadVaspChgcar(CHGCAR, suffix, sort, atoms_index, logger)
        self.charge_density = value
        return value

    def read_charge_header(
        self, CHGCAR="CHGCAR", suffix=".vasp", sort=False, atoms_index=None, logger=None
    ):
        """Create ReadVaspChgcarHeader; retain it as charge_header and return it."""
        from sae.vasp.chgcar_header import ReadVaspChgcarHeader

        value = ReadVaspChgcarHeader(CHGCAR, suffix, sort, atoms_index, logger)
        self.charge_header = value
        return value

    def read_charge_footer(
        self,
        CHGCAR,
        header_data,
        suffix=".vasp",
        sort=False,
        atoms_index=None,
        logger=None,
    ):
        """Create ReadVaspChgcarFooter; retain it as charge_footer and return it."""
        from sae.vasp.chgcar_footer import ReadVaspChgcarFooter

        value = ReadVaspChgcarFooter(
            CHGCAR, header_data, suffix, sort, atoms_index, logger
        )
        self.charge_footer = value
        return value

    def prepare_charge_writer(
        self,
        outname=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        logger=None,
    ):
        """Create WriteVaspChgcar; retain it as charge_writer and return it."""
        from sae.vasp.chgcar_writer import WriteVaspChgcar

        value = WriteVaspChgcar(outname, poscar_info, ngx_max, ngy_max, ngz_max, logger)
        self.charge_writer = value
        return value

    def prepare_charge_sum(self, logger=None):
        """Create SumChgcar; retain it as charge_sum and return it."""
        from sae.vasp.chgcar_sum import SumChgcar

        value = SumChgcar(logger)
        self.charge_sum = value
        return value

    def conv_rot_euler(self, alpha, beta, gamma):
        """Apply ReadVaspPoscar.conv_rot_euler."""
        return require(self.structure, "structure").conv_rot_euler(alpha, beta, gamma)

    def conv_direct2car(self, ABS=None):
        """Apply ReadVaspPoscar.conv_direct2car."""
        return require(self.structure, "structure").conv_direct2car(ABS)

    def conv_scale21(self):
        """Apply ReadVaspPoscar.conv_scale21."""
        return require(self.structure, "structure").conv_scale21()

    def print_poscar(self, outname="POSCAR", STD=True):
        """Apply ReadVaspPoscar.print_poscar."""
        return require(self.structure, "structure").print_poscar(outname, STD)

    def conv_supercell(self, times=(1, 1, 1)):
        """Apply ReadVaspPoscar.conv_supercell."""
        return require(self.structure, "structure").conv_supercell(times)

    def get_title(self):
        """Apply ReadVaspPoscar.get_title."""
        return require(self.structure, "structure").get_title()

    def get_system(self):
        """Apply ReadVaspPoscar.get_system."""
        return require(self.structure, "structure").get_system()

    def get_scale(self):
        """Apply ReadVaspPoscar.get_scale."""
        return require(self.structure, "structure").get_scale()

    def get_t(self):
        """Apply ReadVaspPoscar.get_t."""
        return require(self.structure, "structure").get_t()

    def get_vasp_version(self):
        """Apply ReadVaspPoscar.get_vasp_version."""
        return require(self.structure, "structure").get_vasp_version()

    def get_atoms(self):
        """Apply ReadVaspPoscar.get_atoms."""
        return require(self.structure, "structure").get_atoms()

    def get_atoms_j(self):
        """Apply ReadVaspPoscar.get_atoms_j."""
        return require(self.structure, "structure").get_atoms_j()

    def get_atoms_index(self):
        """Apply ReadVaspPoscar.get_atoms_index."""
        return require(self.structure, "structure").get_atoms_index()

    def get_atoms_number(self):
        """Apply ReadVaspPoscar.get_atoms_number."""
        return require(self.structure, "structure").get_atoms_number()

    def get_atoms_index_j(self):
        """Apply ReadVaspPoscar.get_atoms_index_j."""
        return require(self.structure, "structure").get_atoms_index_j()

    def get_atoms_number_j(self):
        """Apply ReadVaspPoscar.get_atoms_number_j."""
        return require(self.structure, "structure").get_atoms_number_j()

    def get_nion(self):
        """Apply ReadVaspPoscar.get_nion."""
        return require(self.structure, "structure").get_nion()

    def get_natom(self):
        """Apply ReadVaspPoscar.get_natom."""
        return require(self.structure, "structure").get_natom()

    def get_ion(self):
        """Apply ReadVaspPoscar.get_ion."""
        return require(self.structure, "structure").get_ion()

    def get_ion_local(self):
        """Apply ReadVaspPoscar.get_ion_local."""
        return require(self.structure, "structure").get_ion_local()

    def get_selective(self):
        """Apply ReadVaspPoscar.get_selective."""
        return require(self.structure, "structure").get_selective()

    def get_direct(self):
        """Apply ReadVaspPoscar.get_direct."""
        return require(self.structure, "structure").get_direct()

    def get_position(self):
        """Apply ReadVaspPoscar.get_position."""
        return require(self.structure, "structure").get_position()

    def get_fix(self):
        """Apply ReadVaspPoscar.get_fix."""
        return require(self.structure, "structure").get_fix()

    def get_toten(self):
        """Apply ReadVaspOutcar.get_toten."""
        return require(self.output, "output").get_toten()

    def get_efermi(self):
        """Apply ReadVaspOutcar.get_efermi."""
        return require(self.output, "output").get_efermi()

    def get_tdos(self, spin=0):
        """Apply ReadVaspDoscar.get_tdos."""
        return require(self.dos, "dos").get_tdos(spin)

    def get_inttdos(self, spin=0):
        """Apply ReadVaspDoscar.get_inttdos."""
        return require(self.dos, "dos").get_inttdos(spin)

    def get_ldos(self, l=0, atom=0, spin=0):
        """Apply ReadVaspDoscar.get_ldos."""
        return require(self.dos, "dos").get_ldos(l, atom, spin)

    def get_pdos(self, lm=0, atom=0, spin=0):
        """Apply ReadVaspDoscar.get_pdos."""
        return require(self.dos, "dos").get_pdos(lm, atom, spin)

    def get_tdos_spd(self, l=0, spin=0):
        """Apply ReadVaspDoscar.get_tdos_spd."""
        return require(self.dos, "dos").get_tdos_spd(l, spin)

    def get_ldos_ion(self, l=0, ion=0, spin=0):
        """Apply ReadVaspDoscar.get_ldos_ion."""
        return require(self.dos, "dos").get_ldos_ion(l, ion, spin)

    def write(
        self,
        outname=None,
        suffix=None,
        code="VASP",
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
