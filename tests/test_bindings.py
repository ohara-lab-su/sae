"""Check ownership, original signatures, argument identity, returns and failures."""

import hashlib
import importlib
import inspect
import json
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock
import pytest

ROOT = Path(__file__).resolve().parents[1]
BINDINGS = json.loads((ROOT / "docs/class-bindings.json").read_text())


@pytest.mark.parametrize("item", BINDINGS, ids=lambda b: b["code"] + "." + b["method"])
def test_binding(item, monkeypatch):
    namespace = importlib.import_module("sae." + item["namespace"])
    module = importlib.import_module(getattr(namespace, item["code"]).__module__)
    obj = getattr(module, item["code"])()
    method = getattr(obj, item["method"])
    parts = item["implementation"].split(".")
    if item["kind"] == "constructor":
        original = getattr(importlib.import_module(".".join(parts[:-1])), parts[-1])
        original_method = original.__init__
    else:
        original = getattr(importlib.import_module(".".join(parts[:-2])), parts[-2])
        original_method = getattr(original, parts[-1])
    params = list(inspect.signature(method).parameters.values())
    old_params = list(inspect.signature(original_method).parameters.values())[1:]
    assert [(p.name, p.kind, p.default) for p in params] == [
        (p.name, p.kind, p.default) for p in old_params
    ]
    args = []
    for p in params:
        if p.kind == inspect.Parameter.VAR_POSITIONAL:
            args.extend([object(), object()])
        else:
            assert p.kind == inspect.Parameter.POSITIONAL_OR_KEYWORD
            args.append(object())
    sentinel = object()
    spy = Mock(return_value=sentinel)
    if item["kind"] == "constructor":
        original_module = importlib.import_module(".".join(parts[:-1]))
        monkeypatch.setattr(original_module, parts[-1], spy)
    else:
        setattr(obj, item["component"], SimpleNamespace(**{item["method"]: spy}))
    assert method(*args) is sentinel
    spy.assert_called_once_with(*args)
    if item["kind"] == "constructor":
        assert getattr(obj, item["component"]) is sentinel
    spy.reset_mock()
    error = ValueError("original failure")
    spy.side_effect = error
    with pytest.raises(ValueError) as caught:
        method(*args)
    assert caught.value is error
