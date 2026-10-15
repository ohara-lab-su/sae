import importlib
import json
from pathlib import Path
import subprocess
import sys
import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
ROWS = json.loads((ROOT / "docs/migration-map.json").read_text())


@pytest.mark.parametrize("row", ROWS, ids=[r["old_class"] for r in ROWS])
def test_compatibility_class_identity(row):
    modern = getattr(importlib.import_module(row["module"]), row["class"])
    legacy = getattr(importlib.import_module(row["old_module"]), row["old_class"])
    assert modern is legacy
    assert modern.__module__ == row["module"]


def test_fresh_imports_are_independent_and_quiet():
    code = """
import sys
import sae, sae.openmx, sae.hilapw, sae.fdmnes, sae.vasp
assert 'numpy' not in sys.modules
assert 'pandas' not in sys.modules
assert 'ase' not in sys.modules
from sae.openmx import Input
assert 'sae.vasp.structure_legacy' not in sys.modules
assert 'pandas' not in sys.modules
assert 'ase' not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout == ""


def test_legacy_hilapw_dispatch(hilapw_text, tmp_path):
    from StructureAnalysisEnvironment import Read

    p = tmp_path / "sets.in"
    p.write_text(hilapw_text)
    reader = Read(p, code="HI")
    assert reader.nspin == 2
    np.testing.assert_allclose(
        reader.get_position(), [[0, 0, 0], [0.5, 0.5, 0.5], [0.25, 0.25, 0.25]]
    )
    with pytest.raises(ValueError):
        Read(p, code="made-up-code")


def test_legacy_vasp_values(tmp_path):
    from StructureAnalysisEnvironment import ReadVaspPoscar

    p = tmp_path / "POSCAR"
    p.write_text(
        "test\n1\n3 0 0\n1 4 0\n.2 .3 5\nSi O\n1 1\nDirect\n.1 .2 .3\n.5 .5 .5\n"
    )
    reader = ReadVaspPoscar(str(p))
    assert reader.natom == 2
    np.testing.assert_allclose(
        reader.get_position(), [[0.1, 0.2, 0.3], [0.5, 0.5, 0.5]]
    )
    # Old API retains column cell vectors; new Structure uses row vectors.
    np.testing.assert_allclose(reader.get_t(), [[3, 1, 0.2], [0, 4, 0.3], [0, 0, 5]])


def test_legacy_openmx_values(openmx_text, tmp_path):
    from sae.openmx import LegacyInput

    p = tmp_path / "openmx.dat"
    p.write_text(openmx_text)
    r = LegacyInput(str(p), sort=False)
    assert r.natom == 3
    np.testing.assert_allclose(r.t, [[3, 1, 0.2], [0, 4, 0.3], [0, 0, 5]])
    assert r.get_ispin() == 1


def test_qe_dos_values(tmp_path):
    from sae.quantum_espresso.dos import TotalDOS

    p = tmp_path / "qe.dos"
    p.write_text("# E DOSup DOSdown IntDOS\n-1 1 2 0\n0 2 4 3\n1 3 6 9")
    d = TotalDOS(str(p))
    np.testing.assert_allclose(d.get_eng(), [-1, 0, 1])
    np.testing.assert_allclose(d.get_tdos(1), [2, 4, 6])
    np.testing.assert_allclose(d.get_inttdos(), [0, 3, 9])


def test_fdmnes_input_values(tmp_path):
    from sae.fdmnes import Input

    p = tmp_path / "fdm.inp"
    p.write_text(
        "Filout\nfixture\nAbsorber\n1\nCrystal\n3 4 5 90 90 90\n14 0 0 0\n8 .5 .5 .5\nEnd\n"
    )
    obj = Input(str(p), sort=False)
    assert obj.get_natom() == 2
    assert obj.get_filout() == "fixture"
    np.testing.assert_allclose(obj.get_cellparam(), [3, 4, 5, 90, 90, 90])


def test_athena_values(tmp_path):
    from sae.athena import NormalizedSpectrum

    p = tmp_path / "x.nor"
    p.write_text("# test E0=7112\n7111 0.1\n7112 0.5\n7113 1.0")
    s = NormalizedSpectrum(str(p))
    assert s.e0 == 7112
    np.testing.assert_allclose(s.eng, [7111, 7112, 7113])
    np.testing.assert_allclose(s.nor, [0.1, 0.5, 1.0])


def test_missing_files_do_not_exit(tmp_path):
    from StructureAnalysisEnvironment import read_dataline
    from sae.openmx.pseudopotential import Pseudopotential
    from sae.errors import ParseError

    with pytest.raises(FileNotFoundError):
        read_dataline(tmp_path / "absent")
    with pytest.raises(ParseError):
        Pseudopotential(str(tmp_path / "absent"))
