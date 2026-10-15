# Copyright Kengo NAKADA; SAE class library.
"""HiLAPW owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class HiLAPW:
    """HiLAPW calculation and its structure, results and analysis objects."""

    def __init__(self, filename=None, **options):
        self.structure = None
        if filename is not None:
            self.read_structure(filename, **options)
        elif options:
            raise TypeError("Structure options require filename")

    def read_structure(self, cname="sets.in"):
        """Create ReadHiSets; retain it as structure and return it."""
        from sae.hilapw.sets import ReadHiSets

        value = ReadHiSets(cname)
        self.structure = value
        return value

    def get_title(self):
        """Apply ReadHiSets.get_title."""
        return require(self.structure, "structure").get_title()

    def get_position(self):
        """Apply ReadHiSets.get_position."""
        return require(self.structure, "structure").get_position()

    def print_sets(
        self,
        cname,
        STD,
        title,
        nspin,
        spg_name,
        lattices,
        nion,
        sg_atoms,
        sg_atoms_index,
        sg_position,
        kinfo,
        kpoints,
    ):
        """Call the original writer with its unchanged arguments."""
        from sae.hilapw.sets_writer import SetsWriter

        print_sets = SetsWriter().print_sets
        return SetsWriter().print_sets(
            cname,
            STD,
            title,
            nspin,
            spg_name,
            lattices,
            nion,
            sg_atoms,
            sg_atoms_index,
            sg_position,
            kinfo,
            kpoints,
        )
