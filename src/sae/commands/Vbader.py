#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.acf import ReadVaspAcf
from sae.vasp.poscar import ReadVaspPoscar
from sae.vasp.potcar import ReadVaspPotcar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015 Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re
import numpy as np
import optparse


def options():
    name = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if not os.path.exists(name):
        name0 = "CONTCAR"
        if not os.path.exists(name0):
            sys.exit("STOP: " + name + " and " + name0 + " file not found")
        else:
            name = name0
    return name


if __name__ == "__main__":
    name = options()
    poscar = ReadVaspPoscar(name)
    potcar = ReadVaspPotcar()
    acfdat = ReadVaspAcf(poscar=poscar, potcar=potcar, acf="ACF.dat")
    acfdat.get_max_bader()
    acfdat.get_min_bader()
    print("#  atom  zval  charge  diff")
    for i in range(acfdat.natom):
        print(
            "%3d %s %5.2f %7.3f %7.3f"
            % (
                i + 1,
                acfdat.atoms_index_j[i],
                acfdat.atoms_zval_j[i],
                acfdat.charge[i],
                acfdat.bader[i],
            )
        )
    print("----------")
    print("MAX charge %s" % str(acfdat.max_bader))
    print("MIN charge %s" % str(acfdat.min_bader))
