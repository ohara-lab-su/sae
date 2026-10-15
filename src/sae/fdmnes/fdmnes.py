# Copyright Kengo NAKADA; SAE class library.
"""FDMNES owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class FDMNES:
    """FDMNES calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        self.output = None
        self.output_2016 = None
        self.output_2020 = None
        self.sd = None
        self.sd_2016 = None
        self.sd_2020 = None
        self.xas = None
        self.convolution = None
        self.batch = None
        self.writer = None
        self.batch_writer = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(self, inpname, suffix=".inp", sort=True, atoms_index=None):
        """Create ReadFdmInp; retain it as structure and return it."""
        from sae.fdmnes.inp import ReadFdmInp

        value = ReadFdmInp(inpname, suffix, sort, atoms_index)
        self.structure = value
        return value

    def read_output(self, cname, suffix="_bav.txt"):
        """Create ReadFdmBav; retain it as output and return it."""
        from sae.fdmnes.bav import ReadFdmBav

        value = ReadFdmBav(cname, suffix)
        self.output = value
        return value

    def read_output_2016(self, cname, suffix="_bav.txt", datline=None, num=None):
        """Create ReadFdmBav2016; retain it as output_2016 and return it."""
        from sae.fdmnes.bav_2016 import ReadFdmBav2016

        value = ReadFdmBav2016(cname, suffix, datline, num)
        self.output_2016 = value
        return value

    def read_output_2020(self, cname, suffix="_bav.txt", datline=None, num=None):
        """Create ReadFdmBav2020; retain it as output_2020 and return it."""
        from sae.fdmnes.bav_2020 import ReadFdmBav2020

        value = ReadFdmBav2020(cname, suffix, datline, num)
        self.output_2020 = value
        return value

    def read_sd(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
        bav=None,
    ):
        """Create ReadFdmSd; retain it as sd and return it."""
        from sae.fdmnes.sd import ReadFdmSd

        value = ReadFdmSd(sdname, suffix, inpname, bavname, absorber, weight, bav)
        self.sd = value
        return value

    def read_sd_2016(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
    ):
        """Create ReadFdmSd2016; retain it as sd_2016 and return it."""
        from sae.fdmnes.sd_2016 import ReadFdmSd2016

        value = ReadFdmSd2016(sdname, suffix, inpname, bavname, absorber, weight)
        self.sd_2016 = value
        return value

    def read_sd_2020(
        self,
        sdname,
        suffix="_sd0.txt",
        inpname=None,
        bavname=None,
        absorber=None,
        weight=None,
    ):
        """Create ReadFdmSd2020; retain it as sd_2020 and return it."""
        from sae.fdmnes.sd_2020 import ReadFdmSd2020

        value = ReadFdmSd2020(sdname, suffix, inpname, bavname, absorber, weight)
        self.sd_2020 = value
        return value

    def read_xas(self, cname, suffix=".txt", edge="K", weight=None):
        """Create ReadFdmTxt; retain it as xas and return it."""
        from sae.fdmnes.txt import ReadFdmTxt

        value = ReadFdmTxt(cname, suffix, edge, weight)
        self.xas = value
        return value

    def read_convolution(self, cname, suffix="_conv.txt", weight=None):
        """Create ReadFdmConv; retain it as convolution and return it."""
        from sae.fdmnes.conv import ReadFdmConv

        value = ReadFdmConv(cname, suffix, weight)
        self.convolution = value
        return value

    def read_batch(self, cname="fdmfile", suffix=".txt"):
        """Create ReadFdmFdmfile; retain it as batch and return it."""
        from sae.fdmnes.fdmfile import ReadFdmFdmfile

        value = ReadFdmFdmfile(cname, suffix)
        self.batch = value
        return value

    def prepare_writer(self, atoms=None):
        """Create WriteFdmInp; retain it as writer and return it."""
        from sae.fdmnes.inp_writer import WriteFdmInp

        value = WriteFdmInp(atoms)
        self.writer = value
        return value

    def prepare_batch_writer(self, inpname="read_pdb.inp"):
        """Create WriteFdmfile; retain it as batch_writer and return it."""
        from sae.fdmnes.fdmfile_writer import WriteFdmfile

        value = WriteFdmfile(inpname)
        self.batch_writer = value
        return value

    def get_absorber(self):
        """Apply WriteFdmInp.get_absorber."""
        return require(self.writer, "writer").get_absorber()

    def set_absorber(self, val):
        """Apply WriteFdmInp.set_absorber."""
        return require(self.writer, "writer").set_absorber(val)

    def get_fileout(self):
        """Apply WriteFdmInp.get_fileout."""
        return require(self.writer, "writer").get_fileout()

    def set_fileout(self, val):
        """Apply WriteFdmInp.set_fileout."""
        return require(self.writer, "writer").set_fileout(val)

    def get_e_range(self):
        """Apply WriteFdmInp.get_e_range."""
        return require(self.writer, "writer").get_e_range()

    def set_e_range(self, val):
        """Apply WriteFdmInp.set_e_range."""
        return require(self.writer, "writer").set_e_range(val)

    def get_edge(self):
        """Apply WriteFdmInp.get_edge."""
        return require(self.writer, "writer").get_edge()

    def set_edge(self, val):
        """Apply WriteFdmInp.set_edge."""
        return require(self.writer, "writer").set_edge(val)

    def get_radius(self):
        """Apply WriteFdmInp.get_radius."""
        return require(self.writer, "writer").get_radius()

    def set_radius(self, val):
        """Apply WriteFdmInp.set_radius."""
        return require(self.writer, "writer").set_radius(val)

    def get_rmt(self):
        """Apply WriteFdmInp.get_rmt."""
        return require(self.writer, "writer").get_rmt()

    def set_rmt(self, val):
        """Apply WriteFdmInp.set_rmt."""
        return require(self.writer, "writer").set_rmt(val)

    def get_energpho(self):
        """Apply WriteFdmInp.get_energpho."""
        return require(self.writer, "writer").get_energpho()

    def set_energpho(self, val_):
        """Apply WriteFdmInp.set_energpho."""
        return require(self.writer, "writer").set_energpho(val_)

    def get_MOL(self):
        """Apply WriteFdmInp.get_MOL."""
        return require(self.writer, "writer").get_MOL()

    def set_MOL(self, val_):
        """Apply WriteFdmInp.set_MOL."""
        return require(self.writer, "writer").set_MOL(val_)

    def write_inp(
        self,
        atoms=None,
        name="read_pdb.inp",
        absorber=None,
        fileout=None,
        e_range=None,
        edge=None,
        radius=None,
        rmt=None,
        MOL=False,
    ):
        """Apply WriteFdmInp.write_inp."""
        return require(self.writer, "writer").write_inp(
            atoms, name, absorber, fileout, e_range, edge, radius, rmt, MOL
        )

    def write_fdmnes_inp(
        self,
        atoms=None,
        name="read_pdb.inp",
        absorber=None,
        fileout=None,
        e_range=None,
        edge=None,
        radius=None,
        R=None,
        rmt=None,
        green=False,
        energpho=False,
        conv_out=None,
        ecent=None,
        elarg=None,
        gamma_hole=None,
        gamma_max=None,
        MOL=False,
    ):
        """Apply WriteFdmInp.write_fdmnes_inp."""
        return require(self.writer, "writer").write_fdmnes_inp(
            atoms,
            name,
            absorber,
            fileout,
            e_range,
            edge,
            radius,
            R,
            rmt,
            green,
            energpho,
            conv_out,
            ecent,
            elarg,
            gamma_hole,
            gamma_max,
            MOL,
        )

    def write_fdmnes(
        self, atoms=None, prefix_name="POSCAR", name=None, STD=True, MOL=False
    ):
        """Apply WriteFdmInp.write_fdmnes."""
        return require(self.writer, "writer").write_fdmnes(
            atoms, prefix_name, name, STD, MOL
        )

    def write_structure_inp(self, out, atoms=None, MOL=False):
        """Apply WriteFdmInp.write_structure_inp."""
        return require(self.writer, "writer").write_structure_inp(out, atoms, MOL)

    def write_conv_inp(
        self,
        out,
        conv_out=None,
        ecent=None,
        elarg=None,
        gamma_hole=None,
        gamma_max=None,
    ):
        """Apply WriteFdmInp.write_conv_inp."""
        return require(self.writer, "writer").write_conv_inp(
            out, conv_out, ecent, elarg, gamma_hole, gamma_max
        )

    def write_fdmfile(self, prefix=None, inpname=None):
        """Apply WriteFdmfile.write_fdmfile."""
        return require(self.batch_writer, "batch_writer").write_fdmfile(prefix, inpname)

    def get_pdos(self, l=0, m=0, lm=None, spin=0):
        """Apply ReadFdmSd.get_pdos."""
        return require(self.sd, "sd").get_pdos(l, m, lm, spin)

    def get_ldos(self, l=0, spin=0):
        """Apply ReadFdmSd.get_ldos."""
        return require(self.sd, "sd").get_ldos(l, spin)

    def get_tdos(self, spin=0):
        """Apply ReadFdmSd.get_tdos."""
        return require(self.sd, "sd").get_tdos(spin)

    def get_inttdos(self, spin=0):
        """Apply ReadFdmSd.get_inttdos."""
        return require(self.sd, "sd").get_inttdos(spin)

    def get_xas(self, spin=0):
        """Apply ReadFdmTxt.get_xas."""
        return require(self.xas, "xas").get_xas(spin)

    def get_eng(self):
        """Apply ReadFdmTxt.get_eng."""
        return require(self.xas, "xas").get_eng()

    def average(self, name, absorber, spin=0, weight=None):
        """Apply ReadFdmTxt.average."""
        return require(self.xas, "xas").average(name, absorber, spin, weight)

    def average_conv(self, name, absorber, weight=None):
        """Apply ReadFdmConv.average_conv."""
        return require(self.convolution, "convolution").average_conv(
            name, absorber, weight
        )

    def get_title(self):
        """Apply ReadFdmInp.get_title."""
        return require(self.structure, "structure").get_title()

    def get_system(self):
        """Apply ReadFdmInp.get_system."""
        return require(self.structure, "structure").get_system()

    def get_scale(self):
        """Apply ReadFdmInp.get_scale."""
        return require(self.structure, "structure").get_scale()

    def get_t(self):
        """Apply ReadFdmInp.get_t."""
        return require(self.structure, "structure").get_t()

    def get_vasp_version(self):
        """Apply ReadFdmInp.get_vasp_version."""
        return require(self.structure, "structure").get_vasp_version()

    def get_atoms(self):
        """Apply ReadFdmInp.get_atoms."""
        return require(self.structure, "structure").get_atoms()

    def get_atoms_j(self):
        """Apply ReadFdmInp.get_atoms_j."""
        return require(self.structure, "structure").get_atoms_j()

    def get_atoms_index(self):
        """Apply ReadFdmInp.get_atoms_index."""
        return require(self.structure, "structure").get_atoms_index()

    def get_atoms_number(self):
        """Apply ReadFdmInp.get_atoms_number."""
        return require(self.structure, "structure").get_atoms_number()

    def get_atoms_index_j(self):
        """Apply ReadFdmInp.get_atoms_index_j."""
        return require(self.structure, "structure").get_atoms_index_j()

    def get_atoms_number_j(self):
        """Apply ReadFdmInp.get_atoms_number_j."""
        return require(self.structure, "structure").get_atoms_number_j()

    def get_nion(self):
        """Apply ReadFdmInp.get_nion."""
        return require(self.structure, "structure").get_nion()

    def get_natom(self):
        """Apply ReadFdmInp.get_natom."""
        return require(self.structure, "structure").get_natom()

    def get_ion(self):
        """Apply ReadFdmInp.get_ion."""
        return require(self.structure, "structure").get_ion()

    def get_ion_local(self):
        """Apply ReadFdmInp.get_ion_local."""
        return require(self.structure, "structure").get_ion_local()

    def get_selective(self):
        """Apply ReadFdmInp.get_selective."""
        return require(self.structure, "structure").get_selective()

    def get_direct(self):
        """Apply ReadFdmInp.get_direct."""
        return require(self.structure, "structure").get_direct()

    def get_position(self):
        """Apply ReadFdmInp.get_position."""
        return require(self.structure, "structure").get_position()

    def get_fix(self):
        """Apply ReadFdmInp.get_fix."""
        return require(self.structure, "structure").get_fix()

    def get_ispin(self):
        """Apply ReadFdmInp.get_ispin."""
        return require(self.structure, "structure").get_ispin()

    def get_nonexc(self):
        """Apply ReadFdmInp.get_nonexc."""
        return require(self.structure, "structure").get_nonexc()

    def get_allsite(self):
        """Apply ReadFdmInp.get_allsite."""
        return require(self.structure, "structure").get_allsite()

    def get_energygpho(self):
        """Apply ReadFdmInp.get_energygpho."""
        return require(self.structure, "structure").get_energygpho()

    def get_convolution(self):
        """Apply ReadFdmInp.get_convolution."""
        return require(self.structure, "structure").get_convolution()

    def get_conv_out(self):
        """Apply ReadFdmInp.get_conv_out."""
        return require(self.structure, "structure").get_conv_out()

    def get_calculation(self):
        """Apply ReadFdmInp.get_calculation."""
        return require(self.structure, "structure").get_calculation()

    def get_filout(self):
        """Apply ReadFdmInp.get_filout."""
        return require(self.structure, "structure").get_filout()

    def get_cellparam(self):
        """Apply ReadFdmInp.get_cellparam."""
        return require(self.structure, "structure").get_cellparam()

    def write(
        self,
        outname=None,
        suffix=None,
        code="FDMNES",
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
