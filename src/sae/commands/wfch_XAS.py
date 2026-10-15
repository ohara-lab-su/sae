#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.wien2k.dos import ReadWienDos
from sae.wien2k.txspec import ReadWienTxspec
from sae.wien2k.xspec import ReadWienXspec

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
import numpy as np
import pylab
import matplotlib.pyplot as plt


def options():
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    return [options.EMAX, options.EMIN, options.YMAX]


if __name__ == "__main__":
    case1 = "111/111"
    case2 = "222fch/222fch"
    OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
    FLAG_SHOW = True
    dos_suffix = ".dos1ev"
    txspec_suffix = ".txspec"
    xspec_suffix = ".xspec"
    outname = "fch_XAS"
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    unit = "ev"
    name1 = [case1 + dos_suffix]
    name2 = [case2 + dos_suffix]
    print("DOS(1) = ", name1[0])
    dos1 = ReadWienDos(name1)
    efermi1 = dos1.get_efermi()
    eng1 = dos1.get_eng()
    eng1_emin = dos1.get_emin()
    eng1_emax = dos1.get_emax()
    dos1_total = np.array(dos1.get_raw_dos(atom=0, orbit="total-DOS"))
    dos1_p = np.array(dos1.get_raw_dos(atom=1, orbit="p"))
    print("DOS(2) = ", name2[0])
    dos2 = ReadWienDos(name2)
    efermi2 = dos2.get_efermi()
    eng2 = dos2.get_eng()
    eng2_emin = dos2.get_emin()
    eng2_emax = dos2.get_emax()
    dos2_total = np.array(dos2.get_raw_dos(atom=0, orbit="total-DOS"))
    dos2_p = np.array(dos2.get_raw_dos(atom=1, orbit="p"))
    txspec = ReadWienTxspec(case=case2, suffix=txspec_suffix)
    unbroad = txspec.get_unbroad_xas()
    xspec = ReadWienXspec(case=case2, suffix=xspec_suffix)
    eng_xas = xspec.get_eng()
    xas = xspec.get_xas()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.15
    orgy = 0.08
    off = 0.01
    xsize = 0.75
    ysize0 = 0.83
    ysize = ysize0 / 3.5
    ysize_dos = ysize0 / 4
    if OPT_EMAX:
        emax = float(OPT_EMAX)
    else:
        emax = eng2_emax
    if OPT_EMIN:
        emin = float(OPT_EMIN)
    else:
        emin = eng2_emin
    plt.axes([orgx, orgy, xsize, ysize_dos])
    eng1 = eng1 - efermi1
    eng2 = eng2 - efermi2
    plt.plot(
        eng1,
        dos1_total * 8.0,
        color="black",
        linestyle=":",
        linewidth=1,
        label="nch total-DOS",
    )
    plt.plot(
        eng2, dos2_total, color="red", linestyle="-", linewidth=1, label="fch total-DOS"
    )
    plt.ylabel("DOS [unit/" + unit + "]")
    plt.xlabel("Energy above Fermi [" + unit + "]")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.xlim([emin, emax])
    plt.ylim(ymin=0)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    orgy = orgy + ysize_dos + off
    plt.axes([orgx, orgy, xsize, ysize_dos])
    eng1 = eng1 - efermi1
    eng2 = eng2 - efermi2
    plt.plot(eng1, dos1_p, color="black", linestyle=":", linewidth=1, label="nch-p")
    plt.plot(eng2, dos2_p, color="red", linestyle="-", linewidth=1, label="fch-p")
    plt.xticks([])
    plt.xlabel("")
    plt.ylabel("")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.xlim([emin, emax])
    plt.ylim(ymin=0)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    orgy = orgy + ysize + off + off + off + off
    plt.axes([orgx, orgy, xsize, ysize])
    plt.plot(eng_xas, xas, color="black", linewidth=2, label="XAS")
    plt.plot(
        eng_xas, unbroad, linestyle="-", color="green", linewidth=0.8, label="unbroad"
    )
    plt.yticks([])
    plt.xlabel("Energy above Fermi [" + unit + "]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.xlim([emin, emax])
    plt.ylim(ymin=0)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    else:
        ymax = xspec.get_ymax_xas()
        ymax0 = ymax / 10.0
        ymax = ymax + ymax0 * 1.5
        plt.ylim(ymax=ymax)
    plt.savefig(outname + ".eps")
    plt.savefig(outname + ".pdf")
    plt.savefig(outname + ".png")
    if FLAG_SHOW:
        plt.show()
    plt.close("all")
