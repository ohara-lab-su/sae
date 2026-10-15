#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


def options():
    cname = "igzo"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--atoms_index")
    options, args = parser.parse_args()
    if options.INPUT:
        cname = options.INPUT
    if len(args) > 0:
        cname = args[0]
    if cname:
        print("INPUT file name : %s" % cname + ".cfg")
        print("OUTPUT file name: %s" % cname + ".vasp")
        print("atoms_index = %s" % options.atoms_index)
    return (cname, options.atoms_index)


if __name__ == "__main__":
    "\n    usage:\n    V と O 原子の時\n    LVOF.cfg ファイルに対するアプローチとしては\n       ./Rcfg2vasp.py --atoms_index=V,O LVOF.cfg\n"
    cname, atoms_index0 = options()
    atoms_index = []
    if atoms_index0 == None:
        pass
    else:
        for i in atoms_index0.split(","):
            print(i)
            atoms_index.append(i)
    name_, ext_ = os.path.splitext(cname)
    print("name = %s" % name_)
    print("ext = %s" % ext_)
    if ext_ == "":
        filename = cname + ".cfg"
    else:
        filename = cname
    if not os.path.exists(filename):
        sys.exit(filename + " file not found")
    outname = name_
    print(f"atoms_index = {atoms_index}")
    cell = Read(filename=filename, code="RMC", atoms_index=atoms_index)
    cell.write(outname=outname, code="VASP")
