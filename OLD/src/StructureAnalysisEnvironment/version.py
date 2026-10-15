#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os

#def read_version_from_toml() -> str:
#    with open("../../pyproject.toml", encoding="utf-8") as f:
#        for line in f:
#            if line.strip().startswith("version"):
#                m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', line)
#                if m:
#                    return m.group(1)
#    raise RuntimeError("version not found in pyproject.toml")

try:
    # Python 3.8以降では importlib.metadata が標準だが、3.6では pkg_resources を使用
    import pkg_resources
    __version__ = pkg_resources.get_distribution("StructureAnalysisEnvironment").version
except Exception:
    # 開発時のみ pyproject.toml を読む
    def read_version_from_toml() -> str:
        toml_path = os.path.join(os.path.dirname(__file__), "../../pyproject.toml")
        if not os.path.exists(toml_path):
            return "0.0.0"  # fallback
        with open(toml_path, encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("version"):
                    m = re.search(r'version\s*=\s*["\']([^"\']+)["\']', line)
                    if m:
                        return m.group(1)
        return "0.0.0"

    __version__ = read_version_from_toml()


if __name__ == "__main__":
    print(__version__)

#__version__ = "0.0.54"

# __version__ = "0.0.52"

#__version__ = "0.0.51"
#__version__ = "0.0.50"
#__version__ = "0.0.49"
# __version__ = "0.0.48"
# __version__ = "0.0.47"
# __version__ = "0.0.46"
# __version__ = "0.0.45"
# __version__ = "0.0.44"
# __version__ = "0.0.43"
# __version__ = "0.0.42"
# __version__ = "0.0.41"
# __version__ = "0.0.40"
# __version__ = "0.0.39"
# __version__ = "0.0.38"
# __version__ = "0.0.37"
# __version__ = "0.0.36"
# __version__ = "0.0.35"
# __version__ = "0.0.34"
# __version__ = "0.0.33"
# __version__ = "0.0.32"
# __version__ = "0.0.31"
# __version__ = "0.0.30"
# __version__ = "0.0.29"
#__version__ = "0.0.28"

# __version__ = "0.0.27"
# __version__ = "0.0.26"

# __version__ = "0.0.24"
# __version__ = "0.0.23"
# __version__ = "0.0.22"
# __version__ = "0.0.21"
# __version__ = "0.0.20"
# __version__ = "0.0.19"

# __version__ = "0.0.18"
# __version__ = "0.0.17"
# __version__ = "0.0.16"
# __version__ = "0.0.15"
# __version__ = "0.0.14"
# __version__ = "0.0.13"

# __version__ = "0.0.12"
# __version__ = "0.0.11"

# __version__ = "0.0.9"
# __version__ = "0.0.8"
# __version__ = "0.0.7"
# __version__ = "0.0.6"
