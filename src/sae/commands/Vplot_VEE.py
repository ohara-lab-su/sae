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
    OUTCAR = "OUTCAR"
    return OUTCAR


if __name__ == "__main__":
    OUTCAR = options()
    if os.path.exists(OUTCAR):
        GZIP = False
    elif os.path.exists(OUTCAR + ".gz"):
        GZIP = True
    else:
        sys.exit("STOP: " + OUTCAR + " or " + OUTCAR + ".gz file not found")
    try:
        if GZIP:
            tmp = gzip.open(OUTCAR + ".gz")
        else:
            tmp = open(OUTCAR)
        datfile = tmp.read()
        datlines = datfile.split("\n")
    except:
        tmp.close()
        sys.exit("STOP: " + OUTCAR + " does'nt open")
    finally:
        tmp.close()
    ndat = int(len(datlines)) - 1
    energy_reg = re.compile(".*energy  without entropy=", re.IGNORECASE)
    num = 4 - 1
    total_loop = 0
    y = []
    x = []
    for i in range(ndat):
        if bool(energy_reg.match(datlines[i])):
            tmp = datlines[i].split()
            y.append(tmp[num])
            x.append(total_loop)
            total_loop += 1
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    plt.axes([0.13, 0.13, 0.8, 0.8])
    plt.plot(x, y, color="red", linewidth=2, label="Total Energy")
    plt.ylabel("Total Energy [eV]", fontsize=20)
    plt.xlabel("Total Loop ( ION Loop) [n]", fontsize=20)
    plt.savefig("convergeION.eps")
    plt.savefig("convergeION.pdf")
    plt.savefig("convergeION.png")
    plt.show()
    plt.close("all")
