import ast
import re
import copy
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
ENTRIES = json.loads((ROOT / "tests/golden/arithmetic.json").read_text())


class Normalize(ast.NodeTransformer):
    def visit_Call(self, node):
        self.generic_visit(node)
        if isinstance(node.func, ast.Attribute):
            node.func = ast.Name(id=node.func.attr, ctx=ast.Load())
        return node


@pytest.mark.parametrize("item", ENTRIES, ids=lambda x: x["class"] + "." + x["method"])
def test_arithmetic_expressions_retained(item):
    path = ROOT / "src" / Path(*item["module"].split(".")).with_suffix(".py")
    tree = ast.parse(path.read_text())
    cls = next(
        n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == item["class"]
    )
    method = next(
        n
        for n in cls.body
        if isinstance(n, ast.FunctionDef) and n.name == item["method"]
    )
    actual = [
        ast.dump(Normalize().visit(copy.deepcopy(n)), include_attributes=False)
        for n in ast.walk(method)
        if isinstance(n, ast.BinOp)
    ]
    normalize = lambda value: re.sub(r", [A-Za-z_]+=\[\]", "", value)
    assert [normalize(v) for v in actual] == [normalize(v) for v in item["expressions"]]
