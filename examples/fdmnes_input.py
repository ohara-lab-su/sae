"""Original change_Rmt_FDM.py input-generation steps through FDMNES."""

from ase.io.vasp import read_vasp
from sae import FDMNES

atoms = read_vasp("POSCAR")
fdm = FDMNES()
fdm.prepare_writer(atoms)
fdm.write_fdmnes(name="structure", STD=False, MOL=True)
fdm.write_fdmnes_inp(
    name="read_pdb.inp",
    absorber=1,
    fileout="Pd",
    e_range="-15. 0.2  0. 0.5 10. 1. 80.",
    radius=5,
    rmt=1.5,
    MOL=True,
)
