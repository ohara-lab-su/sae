import numpy as np
import pytest
from sae.openmx import Input
from sae.openmx.dos import TotalDOS
from sae.errors import ParseError


def test_document_roundtrip(openmx_text, tmp_path):
    doc = Input(openmx_text)
    assert doc.structure.symbols == ("Si", "O", "Si")
    np.testing.assert_allclose(
        doc.structure.cell, [[3, 0, 0], [1, 4, 0], [0.2, 0.3, 5]]
    )
    np.testing.assert_allclose(doc.structure.positions[0], [0.56, 0.89, 1.5])
    np.testing.assert_array_equal(doc.fixed, [[1, 0, 1], [0, 0, 0], [0, 1, 0]])
    assert doc.species["Si"] == ("Si7.0-s2p2", "Si_PBE19")
    before = doc.structure.positions
    doc.set_structure(doc.structure.translate([0.1, 0.2, 0.3]))
    doc.set_parameter("scf.maxIter", 200)
    doc.write(tmp_path / "openmx.dat.gz")
    again = Input.read(tmp_path / "openmx.dat")
    np.testing.assert_allclose(again.structure.positions, before + [0.1, 0.2, 0.3])
    assert again.get_parameter("scf.maxIter") == "200"
    assert "Unknown.Future.Parameter keep" in again.to_string()
    assert "# keep this" in again.to_string()
    assert again.get_block("Unknown.Block") == [["uninterpreted", "words"]]
    assert again.get_block("Atoms.SpeciesAndCoordinates")[1][5:] == ["3.0", "3.0"]
    with pytest.raises(FileExistsError):
        again.write(tmp_path / "openmx.dat.gz")
    with pytest.raises(ValueError, match="Site count"):
        again.set_structure(again.structure.repeat([2, 1, 1]))


def test_units_and_constraints(openmx_text):
    doc = Input(openmx_text).set_parameter("Atoms.UnitVectors.Unit", "AU")
    doc.set_parameter("Atoms.SpeciesAndCoordinates.Unit", "AU")
    np.testing.assert_allclose(
        doc.structure.positions[0], np.array([0.1, 0.2, 0.3]) * 0.529177210903
    )
    doc.set_fixed([[0, 0, 0], [1, 1, 1], [0, 1, 0]])
    np.testing.assert_array_equal(doc.fixed[1], [1, 1, 1])
    with pytest.raises(ValueError):
        doc.set_fixed([[1, 1, 1]])


@pytest.mark.parametrize(
    "change", ["count", "unit", "index", "species", "unclosed", "duplicate"]
)
def test_bad_input(openmx_text, change):
    text = openmx_text
    if change == "count":
        text = text.replace("Atoms.Number 3", "Atoms.Number 4")
    if change == "unit":
        text = text.replace(".Unit FRAC", ".Unit wrong")
    if change == "index":
        text = text.replace("3 Si 0.7", "2 Si 0.7")
    if change == "species":
        text = text.replace("2 O 0.4", "2 N 0.4")
    if change == "unclosed":
        text = text.replace("Unknown.Block>", "")
    if change == "duplicate":
        text += "Atoms.Number 3\n"
    with pytest.raises(ParseError):
        Input(text).structure


def test_total_dos_spin_integrals(tmp_path):
    path = tmp_path / "dos"
    path.write_text("-1 1 -2 0 0\n0 2 -4 1 2\n1 3 -6 3 6")
    d = TotalDOS.read(path)
    assert d.nspin == 2
    np.testing.assert_allclose(d.density[:, 1], [2, 4, 6])
    np.testing.assert_allclose(d.integrate(), [4, 8])
    np.testing.assert_allclose(d.integrate(-0.5, 0.5), [2, 4])
    np.testing.assert_allclose(d.shifted(1).energy, [-2, -1, 0])
    with pytest.raises(ValueError):
        d.integrate(-2, 1)
    with pytest.raises(ValueError):
        d.integrate(spin=2)


def test_total_dos_unpolarized(tmp_path):
    p = tmp_path / "dos"
    p.write_text("0 1 0\n1 1 1\n")
    assert TotalDOS.read(p).integrate(spin=0) == pytest.approx(1)
