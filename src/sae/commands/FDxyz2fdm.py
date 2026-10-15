#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.ase_input import AseInputOperations
from sae.openmx.md import ReadMd

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import sys
import optparse


def write_fdmnes(xyz, name="POSCAR", STD=True):
    from sae.structure.elements import ElementTable

    if STD:
        out = sys.stdout
    else:
        try:
            out = open(name + ".fdmnes", "w")
        except:
            out.close()
            sys.exit("STOP:" + name + ".fdmnes file can't open")
    natom = xyz.get_natom()
    atoms_index_j = xyz.get_atoms_index_j()
    position = xyz.get_position()
    print(" molecule", file=out)
    print("      1.0 1.0 1.0 90.0 90.0 90.0", file=out)
    for ii in range(natom):
        pos = position[ii]
        sym = atoms_index_j[ii]
        zza = ElementTable().get_atomic_number1(atoms_index_j[ii])
        print(
            "   %2d %12.6f %12.6f %12.6f    ! %s" % (zza, pos[0], pos[1], pos[2], sym),
            file=out,
        )
    if not STD:
        out.close()


def write_fdmnes_inp(xyz, name="read_pdb.inp"):
    from sae.structure.elements import ElementTable

    natom = xyz.get_natom()
    atoms_index_j = xyz.get_atoms_index_j()
    position = xyz.get_position()
    try:
        out = open(name, "w")
    except:
        out.close()
        sys.exit("STOP:" + name + ".fdmnes file can't open")
    print("! FDMNES indata file", file=out)
    print("", file=out)
    print(" Absorber", file=out)
    print("  1", file=out)
    print("! allsite", file=out)
    print("", file=out)
    print(" Filout", file=out)
    print("  Cu", file=out)
    print("", file=out)
    print(" Range                        ! Energy range of calculation (eV)", file=out)
    print(
        "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy",
        file=out,
    )
    print("! -15. 0.1 50. 1. 200.        !", file=out)
    print("", file=out)
    print("!Energpho", file=out)
    print("", file=out)
    print(" Edge", file=out)
    print("  K", file=out)
    print("! L23", file=out)
    print("", file=out)
    print(" Relativism", file=out)
    print("", file=out)
    print("!Magnetism", file=out)
    print("", file=out)
    print("!Quadrupole", file=out)
    print("", file=out)
    print("!TDDFT", file=out)
    print("", file=out)
    print(" Green", file=out)
    print("", file=out)
    print("!No_Fermi", file=out)
    print("! SCF", file=out)
    print("", file=out)
    print(
        " Radius                       ! Radius of the cluster where final state calculation is performed",
        file=out,
    )
    print(
        "   3.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems",
        file=out,
    )
    print("", file=out)
    print(" Memory_save", file=out)
    print("", file=out)
    print(" molecule", file=out)
    print("      1.0 1.0 1.0 90.0 90.0 90.0", file=out)
    for ii in range(natom):
        pos = position[ii]
        sym = atoms_index_j[ii]
        zza = ElementTable().get_atomic_number1(atoms_index_j[ii])
        px = pos[0]
        py = pos[1]
        pz = pos[2]
        print("   %2d %12.6f %12.6f %12.6f    ! %s" % (zza, px, py, pz, sym), file=out)
    print("", file=out)
    print(" Density", file=out)
    print("  state_all", file=out)
    print("", file=out)
    print("!Adimp", file=out)
    print("! 0.20", file=out)
    print("", file=out)
    print(" Convolution", file=out)
    print("", file=out)
    print(" End", file=out)
    print("", file=out)
    out.close()


def options():
    from sae.common.paths import FileDiscovery

    MD0 = "xyzfile"
    suffix = "md"
    MD = MD0 + "." + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        MD = options.INPUT
    if len(args) > 0:
        MD = args[0]
    if not os.path.exists(MD):
        MD0 = FileDiscovery().find_datfile("md")
        suffix = "md"
        if MD0 is None:
            MD0 = FileDiscovery().find_datfile("xyz")
            suffix = "xyz"
            if MD0 is None:
                sys.exit("STOP: INPUT file not found.")
        if not os.path.exists(MD0 + ".md"):
            MD0 = FileDiscovery().find_datfile("xyz")
            suffix = "xyz"
            if not os.path.exists(MD0 + ".xyz"):
                sys.exit("STOP")
    MD = MD0 + "." + suffix
    MOL = True
    return (MD0, suffix, MOL)


if __name__ == "__main__":
    MD0, suffix, MOL = options()
    MD = MD0 + "." + suffix
    xyz = ReadMd(MD)
    AseInputOperations().write_fdmnes(xyz)
    AseInputOperations().write_fdmnes(xyz, name=MD0, STD=False)
    AseInputOperations().write_fdmnes_inp(xyz)
