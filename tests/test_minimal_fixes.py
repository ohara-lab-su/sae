"""Regression checks for interface corrections, independent of wrapper wiring."""

from itertools import product
import importlib
import json
from pathlib import Path
import numpy as np
import pytest
from sae import VASP, PWscf
from test_regression import POSCAR, ROOT


@pytest.mark.parametrize("times", [(1, 1, 1), (2, 1, 2), (1, 2, 3), (3, 2, 1)])
def test_supercell_sizes_coordinates_and_flags(times, tmp_path):
    path = tmp_path / "POSCAR"
    path.write_text(
        POSCAR.replace("2.0 0.1 0.2", "2.0 0 0")
        .replace("0.3 2.4 0.1", "0 2.4 0")
        .replace("0.2 0.4 2.7", "0 0 2.7")
    )
    calc = VASP(str(path))
    original = calc.structure
    fractions = original.position.copy()
    vectors = original.t.copy()
    flags = original.fix.copy()
    counts = original.atoms.copy()
    scale = original.scale
    calc.conv_supercell(times)
    repetitions = int(np.prod(times))
    assert calc.structure.natom == len(fractions) * repetitions
    np.testing.assert_array_equal(calc.structure.atoms, counts * repetitions)
    np.testing.assert_allclose(calc.structure.t, scale * vectors * np.array(times))
    expected = [
        (position + np.array(shift)) / np.array(times)
        for position in fractions
        for shift in product(*(range(n) for n in times))
    ]
    np.testing.assert_allclose(calc.get_position(), expected, atol=1e-14)
    np.testing.assert_array_equal(
        calc.structure.fix, np.repeat(flags, repetitions, axis=0)
    )
    assert calc.structure.direct is True
    assert calc.structure.scale == 1.0
    calc.print_poscar(str(tmp_path / "supercell.vasp"), STD=False)


def test_existing_two_and_five_return_versions_agree():
    from sae.geometry.coordinates import CoordinateTransforms

    conv_car2direct = CoordinateTransforms().conv_car2direct
    from sae.geometry.coordinates import CoordinateTransforms

    conv_car2directa = CoordinateTransforms().conv_car2directa
    vectors = np.array([[2.0, 0.3, 0.2], [0.1, 2.4, 0.4], [0.2, 0.1, 2.7]])
    a = np.array([[0.2, 0.3, 0.4], [1.1, 0.2, 1.3]])
    b = a.copy()
    two = conv_car2directa(1.7, vectors, len(a), False, a)
    five = conv_car2direct(1.7, vectors, len(b), False, b)
    assert tuple(two) == (five[0], five[3])
    np.testing.assert_array_equal(a, b)


def test_integrated_dos_returns_loaded_column(tmp_path):
    path = tmp_path / "input.dos"
    path.write_text("# E up down integral\n-1 2 3 4\n0 4 5 6\n1 6 7 8\n")
    calc = PWscf()
    calc.read_tdos(str(path))
    np.testing.assert_array_equal(calc.get_inttdos(), [4.0, 6.0, 8.0])
    assert np.shares_memory(calc.get_inttdos(), calc.tdos.inttdos_all)


def test_file_specific_namespaces():
    import inspect

    bindings = json.loads((ROOT / "docs/class-bindings.json").read_text())
    for item in bindings:
        if item["kind"] != "constructor":
            continue
        module, name = item["implementation"].rsplit(".", 1)
        cls = getattr(importlib.import_module(module), name)
        assert cls.__module__ == module
        assert str(Path(inspect.getsourcefile(cls)).resolve()).startswith(
            str(ROOT / "src" / "sae")
        )


def test_atomic_weight_text_and_bytes_interface(tmp_path):
    from sae.structure.elements import ElementTable

    get_atomic_weight1 = ElementTable().get_atomic_weight1
    assert get_atomic_weight1("Cu") == get_atomic_weight1(b"Cu")
    assert get_atomic_weight1("O") == get_atomic_weight1(b"O")
    path = tmp_path / "POSCAR"
    path.write_text(POSCAR)
    calc = VASP(str(path))
    calc.write(outname=str(tmp_path / "converted"), code="PWSCF")
    outputs = [p for p in tmp_path.iterdir() if p.name != "POSCAR"]
    assert outputs
    assert any(("ATOMIC_SPECIES" in p.read_text() for p in outputs))
