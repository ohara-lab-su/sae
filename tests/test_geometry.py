import numpy as np
import pytest
from sae.structure import Structure, cell_from_parameters
from sae.vasp import Poscar
from sae.errors import ParseError


def test_nonorthogonal_geometry():
    cell = np.array([[3.0, 0.0, 0.0], [1.0, 4.0, 0.0], [0.2, 0.3, 5.0]])
    frac = np.array([[0.1, 0.2, 0.3], [0.7, 0.8, 0.9]])
    s = Structure(["Si", "O"], frac, cell, fractional=True)
    np.testing.assert_allclose(s.positions, frac.dot(cell))
    np.testing.assert_allclose(s.fractional_positions, frac)
    assert s.volume == pytest.approx(60)
    copied = s.copy().translate([1, 0, 0], fractional=True).wrap()
    np.testing.assert_allclose(copied.positions, s.positions)
    repeated = s.repeat([2, 3, 1])
    assert len(repeated) == 12
    assert repeated.volume == pytest.approx(360)
    np.testing.assert_allclose(repeated.positions[2:4], s.positions + cell[1])
    s.set_cell(cell * 2, scale_positions=True)
    np.testing.assert_allclose(s.fractional_positions, frac)
    array = s.positions
    array[:] = 0
    assert np.any(s.positions)


@pytest.mark.parametrize(
    "repeats", [[0, 1, 1], [1.5, 1, 1], [1, 1], [True, True, True]]
)
def test_bad_repeats(repeats):
    with pytest.raises(ValueError):
        Structure(["H"], [[0, 0, 0]], np.eye(3)).repeat(repeats)


def test_cell_parameters():
    c = cell_from_parameters([3, 4, 5, 80, 90, 100])
    np.testing.assert_allclose(np.linalg.norm(c, axis=1), [3, 4, 5])
    assert np.degrees(np.arccos(np.dot(c[0], c[1]) / 12)) == pytest.approx(100)
    with pytest.raises(ValueError):
        cell_from_parameters([3, 4, 5, 10, 10, 170])


@pytest.mark.parametrize("mode", ["Direct", "Cartesian"])
@pytest.mark.parametrize("scale", ["2.0", "-192.0", "2.0 3.0 4.0"])
def test_poscar_scale_and_roundtrip(mode, scale):
    text = "\n".join(
        [
            "sample",
            scale,
            "2 0 0",
            ".5 3 0",
            ".1 .2 4",
            "Si O",
            "1 1",
            "Selective dynamics",
            mode,
            ".1 .2 .3 T F T",
            ".5 .6 .7 F F F",
        ]
    )
    p = Poscar.from_string(text)
    factors = (
        np.array([2.0, 3.0, 4.0])
        if len(scale.split()) == 3
        else np.array([2.0, 2.0, 2.0])
    )
    expected_cell = np.array([[2.0, 0, 0], [0.5, 3, 0], [0.1, 0.2, 4]]) * factors
    np.testing.assert_allclose(p.structure.cell, expected_cell)
    expected = np.array([[0.1, 0.2, 0.3], [0.5, 0.6, 0.7]])
    expected = expected.dot(expected_cell) if mode == "Direct" else expected * factors
    np.testing.assert_allclose(p.structure.positions, expected)
    for direct in (True, False):
        reread = Poscar.from_string(p.to_string(direct=direct))
        np.testing.assert_allclose(reread.structure.positions, expected)
        np.testing.assert_array_equal(
            reread.movable, [[True, False, True], [False, False, False]]
        )


def test_poscar_vasp4_and_tail(tmp_path):
    text = "sample\n1\n1 0 0\n0 1 0\n0 0 1\n1\nDirect\n0 0 0\n\nCartesian\n1 2 3\n"
    with pytest.raises(ParseError, match="species"):
        Poscar.from_string(text)
    p = Poscar.from_string(text, species=["Si"])
    assert "Cartesian\n1 2 3" in p.to_string()
    p.write(tmp_path / "POSCAR.gz")
    assert Poscar.read(tmp_path / "POSCAR.gz").structure.symbols == ("Si",)
    with pytest.raises(FileExistsError):
        p.write(tmp_path / "POSCAR.gz")
    p.structure = p.structure.repeat([2, 1, 1])
    with pytest.raises(ValueError, match="site count"):
        p.to_string()
