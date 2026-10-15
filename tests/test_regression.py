import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[1]
POSCAR = "regression triclinic\n1.7\n2.0 0.1 0.2\n0.3 2.4 0.1\n0.2 0.4 2.7\nCu O\n1 2\nSelective dynamics\nDirect\n0.1 0.2 0.3 T F T\n0.4 0.5 0.6 F T F\n0.7 0.8 0.9 T T T\n"


@pytest.mark.parametrize(
    "case",
    [
        "vasp-direct",
        "vasp-cartesian",
        "vasp-convert",
        "fdmnes",
        "athena",
        "pwscf-dos",
        "openmx-frac",
        "openmx-ang",
        "openmx-au",
        "hilapw",
        "fdmnes-xas",
        "fdmnes-conv",
        "fdmnes-output",
    ],
)
def test_old_and_new(case, tmp_path):
    mode = "new"
    if True:
        cwd = tmp_path / mode
        cwd.mkdir()
        (cwd / "POSCAR").write_text(
            POSCAR.replace("Direct", "Cartesian")
            if case == "vasp-cartesian"
            else POSCAR
        )
        (cwd / "case.nor").write_text(
            "# sample E0=8979\n8970 0.1\n8979 0.5\n8990 1.0\n"
        )
        (cwd / "case.dos").write_text(
            "# E DOSup DOSdown IntDOS\n-1 2 3 4\n0 4 5 6\n1 6 7 8\n"
        )
        (cwd / "sets.in").write_text(
            "sample\n--spin\n1\n--space group\nP1\n3 4 5\n90 90 90\n--atoms\n1\nCu 1\n0.1 0.2 0.3\n--k points\n1\n2 2 2\n"
        )
        units = {"openmx-frac": "FRAC", "openmx-ang": "Ang", "openmx-au": "AU"}
        (cwd / "case.dat").write_text("""System.Name sample
scf.SpinPolarization Off
Species.Number 2
<Definition.of.Atomic.Species
Cu Cu6.0-s2p2d2 Cu_PBE13
O O5.0-s2p2d1 O_PBE13
Definition.of.Atomic.Species>
Atoms.Number 3
Atoms.SpeciesAndCoordinates.Unit UNIT
<Atoms.SpeciesAndCoordinates
1 Cu 0.1 0.2 0.3 5.5 5.5
2 O 0.4 0.5 0.6 3.0 3.0
3 O 0.7 0.8 0.9 3.0 3.0
Atoms.SpeciesAndCoordinates>
Atoms.UnitVectors.Unit Ang
<Atoms.UnitVectors
2.0 0.1 0.2
0.3 2.4 0.1
0.2 0.4 2.7
Atoms.UnitVectors>
<MD.Fixed.XYZ
1 1 0 1
2 0 1 0
3 0 0 0
MD.Fixed.XYZ>
""".replace("UNIT", units.get(case, "FRAC")))
        env = dict(
            os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONPATH=str(ROOT / "src")
        )
        run = subprocess.run(
            [
                sys.executable,
                "-W",
                "ignore",
                str(ROOT / "tests/regression_driver.py"),
                "new",
                case,
            ],
            cwd=str(cwd),
            env=env,
            capture_output=True,
            text=True,
        )
        assert run.returncode == 0, run.stdout + run.stderr
        expected = json.loads((ROOT / "tests/golden" / (case + ".json")).read_text())
        assert json.loads((cwd / "result.json").read_text()) == expected["result"]
        actual = {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in cwd.iterdir()
            if p.is_file()
            and p.name
            not in (
                "POSCAR",
                "case.nor",
                "case.dos",
                "case.dat",
                "sets.in",
                "result.json",
            )
            and not p.name.startswith("Fe")
        }
        assert actual == expected["files"]
