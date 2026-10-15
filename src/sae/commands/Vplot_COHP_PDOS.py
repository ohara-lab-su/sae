#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.lobster.doscar import ReadLobDos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    dname = "DOSCAR.lobster"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR")
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("-l", "--landscape", action="store_true", default=False)
    parser.add_option("--hexagonal", action="store_true", default=False)
    parser.add_option("--cubic", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("--sp", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("-a", "--atom", dest="ATOM")
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    return [
        dname,
        options.nw,
        options.landscape,
        options.hexagonal,
        options.cubic,
        options.spd,
        options.sp,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.ATOM,
    ]


if __name__ == "__main__":
    (
        dname,
        NO_WINDOW_FLAG,
        LANDSCAPE_FLAG,
        HEX_FLAG,
        CUBIC_FLAG,
        SPD_FLAG,
        SP_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_ATOM,
    ) = options()
    if HEX_FLAG:
        print("Hexagonal MODE")
    elif CUBIC_FLAG:
        print("Cubic MODE")
    elif SPD_FLAG:
        print("SPD(lm=0,1,2,,,,9) MODE")
    elif SP_FLAG:
        print("Selective s-orbital and p-orbital MODE (disable d-orbital plot)")
    else:
        print("Default (lm=0,1,2,,,,9) MODE")
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    if OPT_ATOM:
        print("ATOM=", OPT_ATOM)
        atom = int(OPT_ATOM) - 1
    else:
        atom = 0
    out = sys.stdout
    dos = ReadLobDos(dname)
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE = "DOSCAR.lobster"
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    if NATOM < atom + 1:
        sys.exit("STOP: NATOM=" + str(NATOM))
    if LORBIT <= 10:
        sys.exit("STOP: LORIBT=" + str(LORBIT))
    ENG = dos.eng
    plt.rcParams["font.size"] = 14
    plt.rcParams["legend.fontsize"] = 5
    plt.rcParams["axes.linewidth"] = 1.5
    if not LANDSCAPE_FLAG:
        plt.figure(figsize=(7.0, 9.89))
    list1_1 = ["s"]
    list1_2 = ["p_y", "p_z", "p_x"]
    list1_3 = ["d_xy", "d_yz", "d_3z2-r2", "d_xz", "d_x2-y2"]
    list1 = [list1_1, list1_2, list1_3]
    list2_1 = ["s"]
    list2_2 = ["p_y", "p_z", "p_x"]
    list2_3 = ["d_xy", "d_yz", "d_zx"]
    list2_4 = ["d_3z2-r2", "d_x2-y2"]
    list2 = [list2_1, list2_2, list2_3, list2_4]
    list3_1 = ["s", "p_y", "p_x"]
    list3_2 = ["d_yz", "d_xz"]
    list3_3 = ["d_yz", "d_x2-y2"]
    list3_4 = ["d_3z2-r2"]
    list3 = [list3_1, list3_2, list3_3, list3_4]
    list4_1 = ["s"]
    list4_2 = ["p_z"]
    list4_3 = ["p_y", "p_x"]
    list4 = [list4_1, list4_2, list4_3]
    if SP_FLAG:
        block_list = list4
    elif HEX_FLAG:
        block_list = list3
    elif CUBIC_FLAG:
        block_list = list2
    elif SPD_FLAG:
        block_list = list1
    else:
        block_list = list1
    nblock = len(block_list)
    print("Number of nblock = ", nblock)
    orgx = 0.13
    orgy = 0.08
    off = 0.015
    size = 0.83 / nblock / NSPIN
    for blk in range(nblock - 1, -1, -1):
        for spin in range(NSPIN - 1, -1, -1):
            if blk == nblock - 1:
                atom_label = str(atom)
                if spin == 1:
                    print("Atom =", atom + 1)
            plt.axes([orgx, orgy, 0.8, size])
            if NSPIN == 1:
                orgy = orgy + size + off
            if NSPIN == 2:
                if spin == 0:
                    orgy = orgy + size + off
                if spin == 1:
                    orgy = orgy + size
            lm_list = block_list[blk]
            ll = 0
            for lm in lm_list:
                c = cm.prism(float(ll + 1) / 9)
                PDOS = dos.get_pdos(lm=lm, atom=atom, spin=spin)
                plt.plot(
                    ENG,
                    PDOS,
                    linestyle="-",
                    color=c,
                    linewidth=2,
                    label=str(atom_label) + " " + str(lm),
                )
                ll += 1
            plt.axvline(x=0, color="black", linewidth=1)
            if NSPIN == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([0, ymax])
            if NSPIN == 2:
                xmin, xmax, ymin, ymax = plt.axis()
                if spin == 0:
                    plt.ylim([0, ymax])
                if spin == 1:
                    plt.ylim([ymax, 0])
            if blk == 0 and spin == 0:
                plt.title(TITLE, fontsize=16)
            if blk != nblock - 1:
                plt.xticks([])
            if NSPIN == 1:
                if blk == nblock - 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if NSPIN == 2:
                if blk == nblock - 1 and spin == 0:
                    plt.xticks([])
                if blk == nblock - 1 and spin == 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if OPT_EMAX:
                plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=float(OPT_EMIN))
            if OPT_YMAX:
                plt.ylim(ymax=float(OPT_YMAX))
            if spin == 0:
                leg = plt.legend(fontsize=9)
                leg.get_frame().set_alpha(0.5)
    if HEX_FLAG:
        foot = "hex"
    elif CUBIC_FLAG:
        foot = "cubic"
    elif SPD_FLAG:
        foot = "spd"
    elif SP_FLAG:
        foot = "sp"
    else:
        foot = ""
    if LANDSCAPE_FLAG:
        plt.savefig("COHP_PDOS" + str(atom + 1) + "_" + foot + ".eps")
        plt.savefig("COHP_PDOS" + str(atom + 1) + "_" + foot + ".pdf")
        plt.savefig("COHP_PDOS" + str(atom + 1) + "_" + foot + ".png")
    else:
        plt.savefig(
            "COPHP_PDOS" + str(atom + 1) + "_" + foot + ".eps", orientation="portrait"
        )
        plt.savefig(
            "COPHP_PDOS" + str(atom + 1) + "_" + foot + ".pdf", orientation="portrait"
        )
        plt.savefig(
            "COPHP_PDOS" + str(atom + 1) + "_" + foot + ".png", orientation="portrait"
        )
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
