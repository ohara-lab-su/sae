#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import sys
import os
import re


def options():
    from sae.common.paths import FileDiscovery

    poscarname = "POSCAR"
    datname = "POSCAR"
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-s", "--stdout", action="store_true")
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option("-d", "--direct", action="store_true", dest="FRAC")
    options, args = parser.parse_args()
    if not os.path.exists(poscarname):
        poscarname0 = FileDiscovery().find_datfile("vasp")
        if poscarname0 is None:
            sys.exxit("STOP: POSCAR or .vasp files not found")
        poscarname = poscarname0 + ".vasp"
    if options.INPUT:
        poscarname = options.INPUT
    if options.OUTPUT:
        datname = options.OUTPUT
    datname = re.sub("\\.dat", "", datname)
    if len(args) > 0:
        poscarname = args[0]
    return [poscarname, datname, options.stdout, options.FRAC]


if __name__ == "__main__":
    poscarname, datname, OPT_STD, OPT_FRAC = options()
    print("INPUT :", poscarname)
    print("OUTPUT:", datname + ".dat")
    cell = Read(filename=poscarname, code="VASP")
    cell.write(
        outname=datname, code="OpenMX", calinfo="VASP", STD=OPT_STD, FRAC=OPT_FRAC
    )
