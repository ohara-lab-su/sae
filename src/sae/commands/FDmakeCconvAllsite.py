#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.inp import ReadFdmInp

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import glob
import re
import optparse


def options():
    name = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if not os.path.exists(name):
        name = "conv.inp"
    return name


if __name__ == "__main__":
    inpname = options()
    inp = ReadFdmInp(inpname)
    filout = inp.get_filout()
    if filout is None:
        sys.exit("STOP: fileout TAG not found in " + inpname)
    print("redfile =", inpname)
    print("filout  = ", filout)
    calname = []
    for i in sorted(glob.glob(filout + "_*.txt")):
        if bool(re.compile(filout + "_\\d+.txt").match(i)):
            calname.append(i)
    ncal = len(calname)
    try:
        fdmlist = open("fdmfile.txt", "w")
    except:
        fdmlist.close()
    print("", file=fdmlist)
    print(" " + str(ncal), file=fdmlist)
    for i in range(ncal):
        print(calname[i])
        convname = "conv_" + str(i + 1) + ".inp"
        try:
            convinp = open(convname, "w")
        except:
            convinp.close()
        print(convname, file=fdmlist)
        print("", file=convinp)
        print(" Filout", file=convinp)
        print("   " + filout, file=convinp)
        print("", file=convinp)
        print(" Calculation", file=convinp)
        print("   " + calname[i], file=convinp)
        print("", file=convinp)
        print(" Conv_out", file=convinp)
        print("   " + calname[i].replace(".txt", "") + "_conv.txt", file=convinp)
        print("", file=convinp)
        print(" Convolution", file=convinp)
        print("", file=convinp)
        print("END", file=convinp)
        convinp.close()
    fdmlist.close()
