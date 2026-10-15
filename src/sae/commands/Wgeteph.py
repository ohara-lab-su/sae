#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.wien2k.scf import ReadWienScf

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015 Kengo NAKADA"
__license__ = "MIT"
import os
import re
import optparse

if __name__ == "__main__":
    case = re.sub(".*/", "", os.getcwd())
    suffix = "scf"
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-a", "--atom")
    parser.add_option("-s", "--suffix")
    options, args = parser.parse_args()
    if options.INPUT:
        case = options.INPUT
    if options.atom:
        ion = options.atom
    else:
        ion = "None"
    if options.suffix:
        suffix = options.suffix
    scf = ReadWienScf(case=case, suffix=suffix)
    print("CASE   = ", case)
    print("SUFFIX = ", suffix)
    print("ION    = ", ion)
    scf.write_eph(ion=ion)
