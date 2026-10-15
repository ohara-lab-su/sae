#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.bav import ReadFdmBav
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.txt import ReadFdmTxt

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--name")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.filout
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    return (inpname, options.name)


if __name__ == "__main__":
    inpname, filout = options()
    if not filout:
        inp = ReadFdmInp(inpname)
        filout = inp.filout
    txt = ReadFdmTxt(filout, suffix=".txt")
    bav = ReadFdmBav(filout, suffix="_bav.txt")
    efermi = txt.E_Fermi
    eedge = txt.E_edge
    edge = bav.edge
    print("E_Fermi")
    print(efermi)
    print("E_Edge (" + edge + ")")
    print(eedge)
