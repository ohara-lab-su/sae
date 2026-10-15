"""Run in a working directory containing POSCAR; original conversion routines."""

from sae import VASP

vasp = VASP("POSCAR")
vasp.conv_direct2car()
vasp.write(outname="converted", code="FDMNES")
