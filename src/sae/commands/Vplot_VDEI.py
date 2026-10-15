#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import gzip
import re
import matplotlib.pyplot as plt


def options():
    OSZICAR = "OSZICAR"
    return OSZICAR


if __name__ == "__main__":
    OSZICAR = options()
    if os.path.exists(OSZICAR):
        GZIP = False
    elif os.path.exists(OSZICAR + ".gz"):
        GZIP = True
    else:
        sys.exit("STOP: " + OSZICAR + " or " + OSZICAR + ".gz file not found")
    try:
        if GZIP:
            tmp = gzip.open(OSZICAR + ".gz")
        else:
            tmp = open(OSZICAR)
        datfile = tmp.read()
    except:
        tmp.close()
        sys.exit("STOP: " + OSZICAR + " does'nt open")
    finally:
        tmp.close()
    datlines = datfile.split("\n")
    ndat = int(len(datlines)) - 1
    energy_reg = re.compile(".*F=", re.IGNORECASE)
    total_loop = 0
    y = []
    x = []
    for i in range(ndat):
        if bool(energy_reg.match(datlines[i])):
            tmp = datlines[i].split()
            print(tmp[7])
