import pytest


@pytest.fixture
def openmx_text():
    return """# preserved comment
System.Name sample
Species.Number 2
<Definition.of.Atomic.Species
Si Si7.0-s2p2 Si_PBE19
O O6.0-s2p2 O_PBE19
Definition.of.Atomic.Species>
Atoms.Number 3
Atoms.SpeciesAndCoordinates.Unit FRAC
<Atoms.SpeciesAndCoordinates
1 Si 0.1 0.2 0.3 2.0 2.0
2 O 0.4 0.5 0.6 3.0 3.0
3 Si 0.7 0.8 0.9 2.0 2.0
Atoms.SpeciesAndCoordinates>
Atoms.UnitVectors.Unit Ang
<Atoms.UnitVectors
3.0 0.0 0.0
1.0 4.0 0.0
0.2 0.3 5.0
Atoms.UnitVectors>
<MD.Fixed.XYZ
1 1 0 1
2 0 0 0
3 0 1 0
MD.Fixed.XYZ>
scf.SpinPolarization off
scf.maxIter 100 # keep this
Unknown.Future.Parameter keep
<Unknown.Block
uninterpreted words
Unknown.Block>
"""


@pytest.fixture
def hilapw_text():
    return """HiLAPW fixture
-----nspin
2
-----space group
P1
3.0 4.0 5.0
80.0 90.0 100.0
-----atoms
2
Si 2
0.0 0.0 0.0
0.5 0.5 0.5
O 1
0.25 0.25 0.25
-----k points
1
4 5 6
extra preserved line
"""
