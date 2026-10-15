"""Source information and OLD-recorded GUI output remain part of the release."""
import ast
import collections
import hashlib
import io
import json
import sys
import tokenize
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from sae.gui.unit_cell import UnitCellDrawing

ROOT = Path(__file__).resolve().parents[1]


def test_complete_original_readme_and_changelog():
    readme = (ROOT / 'README.md').read_text()
    start = readme.index('<!-- BEGIN SAE v0.1.0 ADDITION -->')
    end = readme.index('<!-- END SAE v0.1.0 ADDITION -->') + len('<!-- END SAE v0.1.0 ADDITION -->')
    # The inserted block has one surrounding newline on each side.
    stripped = readme[:start - 1] + readme[end + 1:]
    original = (ROOT / 'docs/README-original.md').read_text()
    assert stripped == original
    assert (ROOT / 'CHANGELOG.md').read_bytes().endswith((ROOT / 'docs/CHANGELOG-original.md').read_bytes())
    for name, record in json.loads((ROOT / 'docs/document-preservation.json').read_text()).items():
        assert hashlib.sha256((ROOT / 'docs' / name).read_bytes()).hexdigest() == record['sha256']


def test_restored_comments_are_present_with_multiplicity():
    expected = collections.defaultdict(collections.Counter)
    for entry in json.loads((ROOT / 'docs/source-comments.json').read_text()):
        expected[entry['module']][entry['comment']] += 1
    for module, comments in expected.items():
        source = (ROOT / 'src' / Path(*module.split('.')).with_suffix('.py')).read_text()
        actual = collections.Counter(t.string for t in tokenize.generate_tokens(io.StringIO(source).readline) if t.type == tokenize.COMMENT)
        assert not (comments - actual), module


def test_inventory_destinations_and_original_data():
    for item in json.loads((ROOT / 'docs/migration-inventory.json').read_text()):
        for destination in item['destinations']:
            path = ROOT / destination
            assert path.is_file(), destination
            if item['kind'] == 'unchanged data':
                assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256']


def test_gui_unit_cell_matches_recorded_old_calls(monkeypatch):
    calls = []
    def cylinder(**kw):
        obj = SimpleNamespace(**kw)
        calls.append(vars(obj))
        return obj
    monkeypatch.setitem(sys.modules, 'visual', SimpleNamespace(cylinder=cylinder))
    UnitCellDrawing().crystal_make_unit(np.array([[2., .3, .4], [.5, 3., .6], [.7, .8, 4.]]), origin=[-.3, .2, -.1], radius=.12, color=[7, 8, 9])
    expected = json.loads((ROOT / 'tests/golden/gui-unit-cell.json').read_text())
    assert json.loads(json.dumps(calls)) == expected


def test_gui_atom_conversion_uses_existing_return_interfaces(monkeypatch):
    from sae.gui.crystal import CrystalMaker
    from sae.geometry.coordinates import CoordinateTransforms
    obj = CrystalMaker.__new__(CrystalMaker)
    calls = []
    cell = SimpleNamespace(direct=True, scale=2., t=np.eye(3), natom=0, position=np.zeros((0, 3)), conv_supercell=lambda **kw: calls.append(('supercell', kw)))
    obj.cell, obj.times, obj.origin = cell, [1, 1, 1], [0, 0, 0]
    def direct(self, *args):
        calls.append(('direct', args))
        return 2., False
    def absolute(self, *args):
        calls.append(('absolute', args))
        return 1.
    monkeypatch.setattr(CoordinateTransforms, 'conv_direct2cara', direct)
    monkeypatch.setattr(CoordinateTransforms, 'conv_car2carABSa', absolute)
    monkeypatch.setitem(sys.modules, 'visual', SimpleNamespace())
    obj.plot_atoms()
    assert [c[0] for c in calls] == ['supercell', 'direct', 'absolute']
    assert calls[1][1][0] is False
    assert calls[1][1][-1] is cell.position
    assert calls[2][1][3] is False
    assert cell.scale == 1. and cell.direct is False
