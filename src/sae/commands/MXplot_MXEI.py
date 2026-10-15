#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.dat import ReadMxDat

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re
import optparse
import matplotlib.pyplot as plt

if __name__ == "__main__":
    name = "openmx"
    suffix = ".out"
    mxname = name + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(mxname):
        name0 = FileDiscovery().find_datfile("dat")
        if not name0 is None:
            name = name0
            mxname = name + suffix
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub("\\.out$", "", mxname)
        mxname = name + suffix
    if len(args) > 0:
        name = args[0]
        name = re.sub("\\.out$", "", name)
    mxname = name + suffix
    if not os.path.exists(name + ".out"):
        if os.path.exists(name + ".dat"):
            dat = ReadMxDat(name + ".dat")
            sysname = dat.get_title()
            name = sysname
            mxname = name + suffix
        else:
            sys.exit("STOP: " + name + ".out and " + name + ".dat file not found.")
    module_name = "sae._class_registry"
    if not os.path.exists(mxname):
        mxname = name + ".DFTSCF"
        class_name = "ReadMxDftscf"
        FLAG_DFTSCF = True
    else:
        FLAG_DFTSCF = False
        class_name = "ReadMxOut"
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    out = klass(mxname)
    n_ion_loop = out.get_n_ion_loop()
    max_n_scf = out.get_max_n_scf()
    utot = out.get_utot()
    uele, uele_index = out.get_uele()
    y = []
    x = []
    i = 0
    for md in range(n_ion_loop):
        for scf in range(uele_index[md]):
            x.append(i)
            y.append(uele[md, scf])
            i += 1
    if FLAG_DFTSCF:
        md = n_ion_loop
        for scf in range(uele_index[md]):
            x.append(i)
            y.append(uele[md, scf])
            i += 1
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    plt.axes([0.13, 0.13, 0.8, 0.8])
    plt.plot(x, y, color="red", linewidth=2, label="Total Energy")
    plt.ylabel("Band Energy [Hartree]", fontsize=20)
    plt.xlabel("Total Loop ( ION Loop & SCF Loop) [n]", fontsize=20)
    plt.savefig("convergeION.eps")
    plt.savefig("convergeION.pdf")
    plt.savefig("convergeION.png")
    plt.show()
    plt.close("all")
