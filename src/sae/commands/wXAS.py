#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.wien2k.xspec import ReadWienXspec

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import re
import optparse
import matplotlib.pyplot as plt


def options():
    name = re.sub(".*/", "", os.getcwd())
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    return [name, options.EMAX, options.EMIN, options.YMAX]


if __name__ == "__main__":
    case, OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
        OPT_EMAX = float(OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
        OPT_EMIN = float(OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
        OPT_YMAX = float(OPT_YMAX)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.15
    orgy = 0.08
    off = 0.015
    xsize = 0.75
    ysize = 0.83 / 3.5
    ysize0 = 0.83 / 4
    plt.axes([orgx, orgy, xsize, ysize])
    xspec1 = ReadWienXspec(case="111")
    eng = xspec1.get_eng()
    eng_emin = xspec1.get_emin()
    eng_emax = xspec1.get_emax()
    xas1 = xspec1.get_xas() * 0.85
    plt.plot(eng, xas1, linestyle=":", color="black", linewidth=2, label="222")
    xspec2 = ReadWienXspec(case="222fch")
    xas2 = xspec2.get_xas() * 0.85
    eng2 = xspec2.get_eng()
    plt.plot(eng2, xas2, linestyle="-", color="red", linewidth=1, label="222 with hole")
    plt.yticks([])
    plt.xlabel("Energy above Fermi [ev]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color="black", linewidth=1)
    if OPT_EMAX:
        emax = OPT_EMAX
    else:
        emax = eng_emax
    if OPT_EMIN:
        emin = OPT_EMIN
    else:
        emin = eng_emin
    plt.xlim([emin, emax])
    plt.ylim(ymin=0)
    leg = plt.legend(fontsize=12, loc="lower center")
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    else:
        ymax = xspec1.get_ymax_xas()
        print("YMAX = ", ymax)
        plt.ylim(ymax=ymax)
    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")
    plt.show()
    plt.close("all")
