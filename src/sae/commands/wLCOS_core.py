#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.wien2k.dos import ReadWienDos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import optparse
import numpy as np
import matplotlib.pyplot as plt


def options():
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    options, args = parser.parse_args()
    return [options.nw, options.EMAX, options.EMIN]


if __name__ == "__main__":
    OPT_EMIN0 = "-5"
    OPT_EMAX0 = "30"
    case1 = "111/DOS/DOS"
    case2 = "222hole_inm/DOS/DOS"
    times = 1.0
    ymax_total = 38
    ymax_d = 2.5
    ymax_p = 0.2
    ymax_s = 0.17
    unit = "ev"
    title = "TEST"
    NO_WINDOW_FLAG, OPT_EMAX, OPT_EMIN = options()
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    else:
        OPT_EMAX = OPT_EMAX0
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    else:
        OPT_EMIN = OPT_EMIN0
    nspin = 1
    ion = 1
    FLAG_SPIN = False
    orgx = 0.155
    orgy = 0.088
    xsize = 0.77
    ysize = 0.75 / 4
    off = 0.03
    lists1 = FileDiscovery().find_suffix3(case1 + ".dos", unit)
    print("READ FILE(1)  :", end="")
    for i in lists1:
        print(i, end="")
    print("")
    dos1 = ReadWienDos(lists1)
    eng1 = dos1.get_eng()
    lists2 = FileDiscovery().find_suffix3(case2 + ".dos", unit)
    print("READ FILE(2)  :", end="")
    for i in lists2:
        print(i, end="")
    print("")
    dos2 = ReadWienDos(lists2)
    eng2 = dos2.get_eng()
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    plt.axes([orgx, orgy, xsize, ysize])
    tdos1 = np.array(dos1.get_raw_dos(atom=ion, orbit="total-DOS"))
    tdos2 = np.array(dos2.get_raw_dos(atom=ion, orbit="total-DOS"))
    plt.plot(
        eng1,
        tdos1 * times,
        color="black",
        linestyle=":",
        linewidth=2,
        label="nch-total",
    )
    plt.plot(eng2, tdos2, color="red", linestyle="-", linewidth=1, label="fch-total")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.ylim(ymin=0)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=20)
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=int(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=int(OPT_EMIN))
    plt.ylim(ymax=ymax_total)
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    d1 = dos1.get_raw_dos(atom=ion, orbit="d")
    d2 = dos2.get_raw_dos(atom=ion, orbit="d")
    plt.plot(eng1, d1, color="black", linestyle=":", linewidth=2, label="nch-d")
    plt.plot(eng2, d2, color="blue", linestyle="-", linewidth=1, label="fch-d")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.ylim(ymin=0)
    plt.xticks([])
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=int(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=int(OPT_EMIN))
    plt.ylim(ymax=ymax_d)
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    p1 = dos1.get_raw_dos(atom=ion, orbit="p")
    p2 = dos2.get_raw_dos(atom=ion, orbit="p")
    plt.plot(eng1, p1, color="black", linestyle=":", linewidth=2, label="nch-p")
    plt.plot(eng2, p2, color="green", linestyle="-", linewidth=1, label="fch-p")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.ylim(ymin=0)
    plt.xticks([])
    yl = plt.ylabel("DOS/" + unit, fontsize=20)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=int(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=int(OPT_EMIN))
    plt.ylim(ymax=ymax_p)
    orgy = orgy + ysize + off
    plt.axes([orgx, orgy, xsize, ysize])
    s1 = dos1.get_raw_dos(atom=ion, orbit="s")
    s2 = dos2.get_raw_dos(atom=ion, orbit="s")
    plt.plot(eng1, s1, color="black", linestyle=":", linewidth=2, label="nch-s")
    plt.plot(eng2, s2, color="red", linestyle="-", linewidth=1, label="fch-s")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.ylim(ymin=0)
    plt.xticks([])
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=int(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=int(OPT_EMIN))
    plt.ylim(ymax=ymax_s)
    plt.savefig("LDOS_core.eps")
    plt.savefig("LDOS_core.pdf")
    plt.savefig("LDOS_core.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
