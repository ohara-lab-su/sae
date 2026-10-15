# Copyright Kengo NAKADA; SAE class library.
"""Bader owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class Bader:
    """Bader calculation and its structure, results and analysis objects."""

    def __init__(self):
        self.atomic_volumes = None
        self.charges = None
        self.volume = None
        self.volume_operations = None
        self.volume_writer = None

    def read_atomic_volumes(self, name="AVF.dat", logger=None):
        """Create ReadBaderAvf; retain it as atomic_volumes and return it."""
        from sae.bader.avf import ReadBaderAvf

        value = ReadBaderAvf(name, logger)
        self.atomic_volumes = value
        return value

    def read_charges(self, name="BCF.dat", logger=None):
        """Create ReadBaderBcf; retain it as charges and return it."""
        from sae.bader.bcf import ReadBaderBcf

        value = ReadBaderBcf(name, logger)
        self.charges = value
        return value

    def read_volume(
        self,
        num,
        BvAt="BvAt",
        suffix=".dat",
        sort=False,
        atoms_index=None,
        logger=None,
        split_chgcar=False,
        POSCAR="POSCAR",
    ):
        """Create ReadBaderBvat; retain it as volume and return it."""
        from sae.bader.bvat import ReadBaderBvat

        value = ReadBaderBvat(
            num, BvAt, suffix, sort, atoms_index, logger, split_chgcar, POSCAR
        )
        self.volume = value
        return value

    def prepare_volume_operations(self, logger=None):
        """Create UtilBader; retain it as volume_operations and return it."""
        from sae.bader.volume_operations import UtilBader

        value = UtilBader(logger)
        self.volume_operations = value
        return value

    def prepare_volume_writer(
        self,
        outname="CHGCAR_BvAt",
        chgdata=None,
        poscar_info=None,
        ngx_max=None,
        ngy_max=None,
        ngz_max=None,
        logger=None,
    ):
        """Create WriteBaderVolume; retain it as volume_writer and return it."""
        from sae.bader.volume_writer import WriteBaderVolume

        value = WriteBaderVolume(
            outname, chgdata, poscar_info, ngx_max, ngy_max, ngz_max, logger
        )
        self.volume_writer = value
        return value

    def get_charge(self, atom):
        """Apply ReadBaderBcf.get_charge."""
        return require(self.charges, "charges").get_charge(atom)

    def get_distance(self, atom):
        """Apply ReadBaderBcf.get_distance."""
        return require(self.charges, "charges").get_distance(atom)

    def sum_bader_volume(self, volume_list, split_chgcar=False):
        """Apply UtilBader.sum_bader_volume."""
        return require(self.volume_operations, "volume_operations").sum_bader_volume(
            volume_list, split_chgcar
        )

    def write_bader_volume(self, outname=None):
        """Apply WriteBaderVolume.write_bader_volume."""
        return require(self.volume_writer, "volume_writer").write_bader_volume(outname)
