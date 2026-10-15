#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.base import Method
from sae.vasp.chgcar import ReadVaspChgcar
import sys
import os
import re
import math
import numpy as np

try:
    Method = Method
except ImportError:
    Method = Method
if __name__ == "__main__":
    import optparse

    name = "CHGCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    name = options.INPUT
    chgcar = ReadVaspChgcar(name)
    max = chgcar.chgdata.max()
    min = chgcar.chgdata.min()
    print("origin CHGCAR max = %s" % max)
    print("origin CHGCAR min = %s" % min)
    print("offset            = %s" % max)
    inv_chg = chgcar.inverse_chgcar(offset=max)
    print("origin CHGCAR Inverse max = %s" % inv_chg.max())
    print("origin CHGCAR Inverse min = %s" % inv_chg.min())
    chgcar.print_chgcar(chgcar=inv_chg, outname="CHGCAR_INVERSE")
