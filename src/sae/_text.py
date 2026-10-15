"""Text IO shared by readers, including explicitly named gzip files."""

import gzip
from pathlib import Path


def read_text(path):
    path = Path(path)
    if not path.exists() and Path(str(path) + ".gz").exists():
        path = Path(str(path) + ".gz")
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(str(path), "rt", encoding="utf-8-sig") as handle:
        return handle.read()


def write_text(path, text, overwrite=False):
    path = Path(path)
    mode = "wt" if overwrite else "xt"
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(str(path), mode, encoding="utf-8") as handle:
        handle.write(text)
