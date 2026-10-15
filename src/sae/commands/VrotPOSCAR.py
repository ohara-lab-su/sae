#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.poscar import ReadVaspPoscar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015 Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse

if __name__ == "__main__":
    poscarname = "POSCAR"
    outputname = poscarname + ".vasp"
    alpha = 0
    beta = 0
    gamma = 0
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-a", "--alpha", dest="ALPHA")
    parser.add_option("-b", "--beta", dest="BETA")
    parser.add_option("-g", "--gamma", dest="GAMMA")
    parser.add_option("-s", "--std", action="store_true")
    parser.add_option("-d", "--debug", action="store_true")
    options, args = parser.parse_args()
    STD = False
    DEBUG = False
    if options.ALPHA:
        alpha = float(options.ALPHA)
    if options.BETA:
        beta = float(options.BETA)
    if options.GAMMA:
        gamma = float(options.GAMMA)
    if options.INPUT:
        poscarname = options.INPUT
    if options.OUTPUT:
        outputname = options.OUTPUT
    if options.std:
        STD = True
    if options.debug:
        DEBUG = True
        STD = True
    if len(args) > 2:
        alpha = float(args[0])
        beta = float(args[1])
        gamma = float(args[2])
    if not STD or DEBUG:
        print("INPUT      :", poscarname)
        print("OUTPUT     :", outputname)
        print("ALPHA(DEG) :", alpha)
        print("BETA(DEG)  :", beta)
        print("GAMMA(DEG) :", gamma)
    poscar = ReadVaspPoscar(poscarname)
    title = poscar.get_title()
    scale = poscar.get_scale()
    t = poscar.get_t()
    vasp = poscar.get_vasp_version()
    nion = poscar.get_nion()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    natom = poscar.get_natom()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()
    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    atoms_index_j = poscar.get_atoms_index_j()
    if STD:
        out = sys.stdout
    else:
        try:
            out = open(outputname, "w")
        except:
            sys.exit("STOP: " + out + " can't open")
    if DEBUG:
        print(" ", scale, file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
        print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)
        print("", file=out)
    title0 = "alpha=" + str(alpha) + ", beta=" + str(beta) + ", gamma=" + str(gamma)
    t, position = poscar.conv_rot_euler(alpha, beta, gamma)
    print(title + ": " + title0, file=out)
    print(" ", scale, file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=out)
    print("  %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=out)
    if vasp >= 5:
        print(" ", file=out, end="")
        for i in range(nion):
            print(atoms_index[i], file=out, end="")
        print(" ", file=out)
    print(" ", file=out, end="")
    for i in range(nion):
        print(atoms[i], file=out, end="")
    print(" ", file=out)
    if direct:
        print("Direct", file=out)
    else:
        print("Cartesian", file=out)
    for j in range(natom):
        print(
            " %13.9f %13.9f %13.9f" % (position[j, 0], position[j, 1], position[j, 2]),
            file=out,
            end="",
        )
        print("")
    if not STD:
        out.close()
