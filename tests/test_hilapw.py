import numpy as np
import pytest
from sae.hilapw import Input


def test_sets_roundtrip(hilapw_text, tmp_path, capsys):
    doc = Input.from_string(hilapw_text)
    assert doc.nspin == 2 and doc.space_group == "P1"
    assert doc.species == ("Si", "O") and doc.counts == (2, 1)
    doc.set_kpoints([8, 9, 10], kinfo=2)
    doc.write(tmp_path / "sets.in")
    assert capsys.readouterr().out == ""
    again = Input.read(tmp_path / "sets.in")
    np.testing.assert_array_equal(again.kpoints, [8, 9, 10])
    np.testing.assert_allclose(again.sites, doc.sites)
    assert again.trailing_lines == ("extra preserved line",)
    np.testing.assert_allclose(
        again.to_structure("bohr").cell,
        again.to_structure("angstrom").cell * 0.529177210903,
    )
    with pytest.raises(TypeError):
        again.to_structure()
    with pytest.raises(ValueError):
        again.set_kpoints([1.5, 2, 2])
