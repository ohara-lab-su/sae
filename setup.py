"""Packaging that can run under Python 3.7."""

from pathlib import Path
from setuptools import find_packages, setup

ROOT = Path(__file__).parent
setup(
    name="StructureAnalysisEnvironment",
    version="0.1.0",
    description="Code-specific libraries for structure and electronic-state analysis",
    long_description=(ROOT / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Kengo NAKADA",
    license="Apache-2.0",
    python_requires=">=3.7",
    package_dir={"": "src"},
    packages=find_packages("src", exclude=["StructureAnalysisEnvironment.bin"]),
    package_data={"StructureAnalysisEnvironment": ["*.list"]},
    install_requires=["numpy>=1.17"],
    extras_require={
        "analysis": ["ase", "pandas", "matplotlib", "humanfriendly", "coloredlogs"],
        "test": ["pytest>=7,<8"],
    },
    entry_points={"console_scripts": ["sae=sae.cli:main"]},
)
