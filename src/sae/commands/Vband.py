#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.eigenval import ReadVaspEigenval

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse


def options():
    name = "EIGENVAL"
    out1 = "band1.dat"
    out2 = "band2.dat"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return [name, out1, out2]


if __name__ == "__main__":
    name, out1, out2 = options()
    band = ReadVaspEigenval(name)
    NATOM = band.get_natom()
    TITLE = band.get_title()
    NKPTS = band.get_nkpts()
    NBANDS = band.get_nbands()
    NSPIN = band.get_ispin()
    eigenval = band.get_eigenval()
    for ispin in range(NSPIN):
        if ispin == 0:
            outfile = out1
        else:
            outfile = out2
        try:
            out = open(outfile, "w")
        except:
            out.cloase()
            sys.exit("STOP:" + outfile + " can't open")
        for j in range(NBANDS):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("## ISPIN = ", NSPIN, file=out)
            print("## SPIN  = ", ispin, file=out)
            print("## NBAND = ", NBANDS, file=out)
            print("## BAND  = ", j, file=out)
            print("## EF    = ", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)
            for k in range(NKPTS):
                print("%5d %14.8f" % (k + 1, eigenval[j, k, ispin]), file=out)
        out.close()
