#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import sys
import os
import re


def options():
    poscarname = "POSCAR"
    outbase = "POSCAR"
    inpsuffix = ".in"
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-s", "--stdout", action="store_true")
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    options, args = parser.parse_args()
    outbase = re.sub("\\.in$", "", outbase)
    outinp = outbase + inpsuffix
    if options.INPUT:
        poscarname = options.INPUT
    outbase = poscarname
    if options.OUTPUT:
        outbase = re.sub("\\.inp$", "", options.OUTPUT)
        outinp = outbase + inpsuffix
    if len(args) > 0:
        poscarname = args[0]
    if poscarname == outinp:
        sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :" + poscarname)
    print("INPUT :", poscarname)
    print("OUTPUT:", outbase + inpsuffix)
    return [poscarname, outbase, inpsuffix, options.stdout]


if __name__ == "__main__":
    poscarname, outbase, inpsuffix, OPT_STD = options()
    cname = outbase + inpsuffix
    cell = Read(filename=poscarname, code="VASP")
    cell.write(outname=cname, code="PWScf", STD=OPT_STD)
