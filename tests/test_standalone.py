import ast
import importlib
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
from test_regression import ROOT


def test_no_legacy_runtime_dependencies():
    assert not (ROOT / "setup.py").exists()
    assert not (ROOT / "src/StructureAnalysisEnvironment").exists()
    assert "[project]" in (ROOT / "pyproject.toml").read_text()
    for path in (ROOT / "src/sae").rglob("*.py"):
        tree = ast.parse(path.read_text())
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                names = [a.name for a in node.names] + [getattr(node, "module", "") or ""]
                assert not any("StructureAnalysisEnvironment" in n for n in names), path
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                # Documentation and comments may retain historical names.
                if node.value.startswith("StructureAnalysisEnvironment"):
                    raise AssertionError((path, node.value))
                assert "/OLD/" not in node.value, path


def test_all_implementation_modules_import():
    entries = json.loads((ROOT / "docs/implementation-map.json").read_text())
    for module in sorted({e["module"] for e in entries}):
        importlib.import_module(module)


def test_openmx_dos_resolves_new_data_class(tmp_path, monkeypatch):
    from sae.openmx.dos_methods import ReadMxDosMethod
    import sae.openmx.dat as dat_module

    name = tmp_path / "sample"
    name.with_suffix(".dat").write_text("fixture")
    data = SimpleNamespace(get_ispin=lambda: 2, get_natom=lambda: 3)
    factory = Mock(return_value=data)
    monkeypatch.setattr(dat_module, "ReadMxDat", factory)
    dos = ReadMxDosMethod()
    dos.name = str(name)
    assert dos.get_ispin() == 2
    assert dos.get_natom() == 3
    factory.assert_called_with(str(name) + ".dat")
