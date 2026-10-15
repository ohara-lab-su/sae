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
import optparse
import glob


def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-d", dest="DEST")
    options, args = parser.parse_args()
    fildst = None
    filsrc = None
    inpname = None
    if options.DEST:
        fildst = options.DEST
    if len(args) == 0:
        sys.exit("STOP args < 1 ")
    if len(args) == 1:
        if options.INPUT:
            inpname = options.INPUT
        elif os.path.exists("fdmfile.txt"):
            fdmfiletxt = ReadFdmFdmfile()
            inpname = fdmfiletxt.filout
        else:
            inpname = "read_pdb.inp"
        if not os.path.exists(inpname) or inpname is None:
            sys.exit(inpname + " file not fount")
        fildst = args[0]
    if len(args) == 2:
        filsrc = args[0]
        fildst = args[1]
    return (inpname, filsrc, fildst)


if __name__ == "__main__":
    inpname, filsrc, fildst = options()
    if filsrc is None:
        print("inp :", inpname)
        out = ReadFdmInp(inpname)
        filsrc = out.get_filout()
    print("src :", filsrc)
    print("dst :", fildst)
    print("")
    filelist = [".txt", "_bav.txt", "_conv.txt"]
    for i in glob.glob(filsrc + "_sd*.txt"):
        filelist.append(i.replace(filsrc, ""))
    for i in filelist:
        if os.path.exists(filsrc + i):
            print("MOVE : " + filsrc + i + " --> " + fildst + i)
            os.rename(filsrc + i, fildst + i)
