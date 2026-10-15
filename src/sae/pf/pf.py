# Copyright Kengo NAKADA; SAE class library.
"""PF owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class PF:
    """PF calculation and its structure, results and analysis objects."""

    def __init__(self):
        self.data = None

    def read_data(self, name):
        """Create ReadPfformat; retain it as data and return it."""
        from sae.pf.pf_format import ReadPfformat

        value = ReadPfformat(name)
        self.data = value
        return value

    def write_head(self, *args):
        """Apply ReadPfformat.write_head."""
        return require(self.data, "data").write_head(*args)

    def write_pf(self, *args):
        """Apply ReadPfformat.write_pf."""
        return require(self.data, "data").write_pf(*args)
