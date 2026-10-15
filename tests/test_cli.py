import json
from sae.cli import main


def test_openmx_cli(openmx_text, tmp_path, capsys):
    source = tmp_path / "in.dat"
    source.write_text(openmx_text)
    assert main(["openmx", "inspect", str(source)]) == 0
    assert json.loads(capsys.readouterr().out)["sites"] == 3
    destination = tmp_path / "out.dat"
    args = ["openmx", "set", str(source), "scf.maxIter", "300", str(destination)]
    assert main(args) == 0
    assert "scf.maxIter  300" in destination.read_text()
    assert main(args) == 2


def test_missing_file(tmp_path, capsys):
    assert main(["vasp", "inspect", str(tmp_path / "missing")]) == 2
    assert "sae:" in capsys.readouterr().err
