# Copyright Kengo NAKADA; SAE class library.
"""Athena owns the SAE structure, input, output and analysis objects.

File-specific classes in this package implement each operation.
"""

from sae._binding import require


class Athena:
    """Athena calculation and its structure, results and analysis objects."""

    def __init__(self):
        self.spectrum = None

    def read_spectrum(self, name="case.txt.nor"):
        """Create ReadAthenaNor; retain it as spectrum and return it."""
        from sae.athena.nor import ReadAthenaNor

        value = ReadAthenaNor(name)
        self.spectrum = value
        return value

    def get_nor(self):
        """Apply ReadAthenaNor.get_nor."""
        return require(self.spectrum, "spectrum").get_nor()

    def set_nor(self, _val):
        """Apply ReadAthenaNor.set_nor."""
        return require(self.spectrum, "spectrum").set_nor(_val)

    def get_xas(self):
        """Apply ReadAthenaNor.get_xas."""
        return require(self.spectrum, "spectrum").get_xas()

    def set_xas(self, _val):
        """Apply ReadAthenaNor.set_xas."""
        return require(self.spectrum, "spectrum").set_xas(_val)

    def get_eng(self):
        """Apply ReadAthenaNor.get_eng."""
        return require(self.spectrum, "spectrum").get_eng()

    def set_eng(self, _val):
        """Apply ReadAthenaNor.set_eng."""
        return require(self.spectrum, "spectrum").set_eng(_val)

    def get_e0(self):
        """Apply ReadAthenaNor.get_e0."""
        return require(self.spectrum, "spectrum").get_e0()
