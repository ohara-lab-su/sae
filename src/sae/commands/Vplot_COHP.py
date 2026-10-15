#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.lobster.cohpcar import ReadLobCohp
from sae.lobster.doscar import ReadLobDos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import argparse
import matplotlib.pyplot as plt


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--nw", action="store_true", default=False)
    parser.add_argument("--emax", dest="EMAX")
    parser.add_argument("--emin", dest="EMIN")
    parser.add_argument("--dosmax", "--dmax", dest="DMAX")
    parser.add_argument("--cohpmax", "--ymax", dest="YMAX")
    parser.add_argument("--cohpmin", "--ymin", dest="YMIN")
    parser.add_argument("-u", "--up", action="store_true", default=False)
    parser.add_argument("-d", "--dn", action="store_true", default=False)
    parser.add_argument("--spin", action="store_true", default=False)
    parser.add_argument("-p", "--pair", nargs="*")
    options = parser.parse_args()
    return [
        options.nw,
        options.DMAX,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.YMIN,
        options.up,
        options.dn,
        options.spin,
        options.pair,
    ]


if __name__ == "__main__":
    (
        NO_WINDOW_FLAG,
        OPT_DMAX,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_YMIN,
        OPT_UP,
        OPT_DN,
        OPT_SPIN,
        OPT_PAIR,
    ) = options()
    if OPT_DMAX:
        print("Dmax= %s" % str(OPT_DMAX))
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    if OPT_YMIN:
        print("Ymax= %s" % str(OPT_YMIN))
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    spin_list = [0]
    if OPT_UP:
        spin_list = [0]
    if OPT_DN:
        spin_list = [1]
    if OPT_UP and OPT_DN:
        spin_list = [0, 1]
    if OPT_SPIN:
        spin_list = [0, 1]
    dos = ReadLobDos()
    dos_x = dos.get_eng()
    cohp = ReadLobCohp()
    cohp_x = cohp.get_eng()
    if OPT_PAIR:
        for i in OPT_PAIR:
            par_label = cohp.bond_index[int(i)]
            print(i, par_label)
    plt.subplot(121)
    for s in spin_list:
        if s == 0:
            spin_label = "up"
        if s == 1:
            spin_label = "down"
        label = "TDOS" + "-" + spin_label
        dos_y = dos.get_tdos(spin=s)
        plt.plot(dos_y, dos_x, linewidth=1, label=label)
    plt.axhline(y=0, color="black", linewidth=1)
    if OPT_DMAX:
        plt.xlim(xmax=float(OPT_DMAX))
    if OPT_EMAX:
        plt.ylim(ymax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.ylim(ymin=float(OPT_EMIN))
    plt.xlim(xmin=0)
    plt.xlabel("DOS/eV", fontsize=17)
    plt.ylabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=17)
    leg = plt.legend(fontsize=9, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.subplot(122)
    print("SPIN_LIST = ", spin_list)
    if not OPT_PAIR:
        for s in spin_list:
            if s == 0:
                spin_label = "up"
            if s == 1:
                spin_label = "down"
            label = "Average" + " (" + spin_label + ")"
            cohp_y = cohp.get_ave(spin=s)
            plt.plot(-1.0 * cohp_y, cohp_x, linewidth=1, label=label)
    if OPT_PAIR:
        for s in spin_list:
            for i in OPT_PAIR:
                par_label = cohp.bond_index[int(i)]
                if s == 0:
                    spin_label = "up"
                if s == 1:
                    spin_label = "down"
                label = par_label + "  (" + spin_label + ")"
                cohp_pair = cohp.get_cohp(bond=int(i), spin=s)
                plt.plot(-1.0 * cohp_pair, cohp_x, linewidth=1, label=label)
    plt.axhline(y=0, color="black", linewidth=1)
    plt.axvline(x=0, color="black", linewidth=1)
    if OPT_EMAX:
        plt.ylim(ymax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.ylim(ymin=float(OPT_EMIN))
    if OPT_YMAX:
        plt.xlim(xmax=float(OPT_YMAX))
    if OPT_YMIN:
        plt.xlim(xmin=float(OPT_YMIN))
    plt.yticks([])
    plt.xlabel("-pCOHP", fontsize=17)
    leg = plt.legend(fontsize=9, loc="lower left")
    leg.get_frame().set_alpha(0.5)
    xmin, xmax, ymin, ymax = plt.axis()
    plt.savefig("COHP_tate.eps")
    plt.savefig("COHP_tate.pdf")
    plt.savefig("COHP_tate.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
