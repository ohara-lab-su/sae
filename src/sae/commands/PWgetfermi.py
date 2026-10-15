#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from sae.pwscf.out import ReadPwOut

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import re
import optparse
import numpy as np


def options():
    name = "scf.out"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


if __name__ == "__main__":
    name = options()
    out = ReadPwOut(name)
    print("NAME", name)
    print("TITLE", out.get_title())
    print("LATTICE PARAMETER %6.4f" % out.get_scale())
    print("NATOM", out.get_natom())
    print("NION", out.get_nion())
    print("NBANDS", out.get_nbands())
    print("NSW", out.get_nsw())
    print("ION-LOOP", out.get_n_ion_loop())
    print("")
    print("EFERMI(eV)", out.get_efermi())
    print("EFERMI(Ry)", out.get_efermi() / 13.6)
