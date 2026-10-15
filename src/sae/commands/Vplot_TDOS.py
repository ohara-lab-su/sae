#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse
import matplotlib.pyplot as plt


def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR")
    parser.add_option("-o", "--outcar", dest="OUTCAR")
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    parser.add_option(
        "-p", "--portrait", action="store_true", default=False, dest="PORTRAIT"
    )
    parser.add_option("--inttdos", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("-f", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--up", action="store_true")
    parser.add_option("--dn", action="store_true")
    parser.add_option("--vbm", action="store_true", default=False)
    parser.add_option("--shift")
    parser.add_option("--left", action="store_true", default=False)
    parser.add_option("--noef", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.NOWINDOW,
        options.PORTRAIT,
        options.inttdos,
        options.spd,
        options.f,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.up,
        options.dn,
        options.vbm,
        options.shift,
        options.left,
        options.noef,
    ]


if __name__ == "__main__":
    (
        dname,
        oname,
        NO_WINDOW_FLAG,
        PORTRAIT_FLAG,
        FLAG_INTTDOS,
        FLAG_SPD,
        FLAG_F,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        FLAG_UP,
        FLAG_DN,
        FLAG_VBM,
        OPT_SHIFT,
        FLAG_LEFT,
        FLAG_NOEF,
    ) = options()
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        OPT_YMAX = float(OPT_YMAX)
        print("Ymax= %s" % str(OPT_YMAX))
    if FLAG_INTTDOS:
        print("INTTDOS mode")
    dos = ReadVaspDoscar(dname)
    out = sys.stdout
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE = dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    LMAX = dos.lmax
    ENG = dos.eng
    if FLAG_VBM:
        print("EF SHIFT")
        EFERMI0 = dos.efermi
        EFERMI = dos.get_vbm()
        print(EFERMI0, EFERMI)
    if OPT_SHIFT:
        EFERMI = float(OPT_SHIFT)
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 15
    plt.rcParams["axes.linewidth"] = 1.5
    if PORTRAIT_FLAG:
        plt.figure(figsize=(7.0, 9.89))
    orgx = 0.13
    orgy = 0.125
    sizex = 0.75
    sizey0 = 0.8
    if NSPIN >= 2:
        spin_list = [0, 1]
        if FLAG_UP:
            spin_list = [0]
            NSPIN = 1
        if FLAG_DN:
            spin_list = [1]
            NSPIN = 1
    else:
        spin_list = [0]
    for spin in spin_list:
        if NSPIN == 1:
            sizey = sizey0
        if NSPIN == 2:
            sizey = sizey0 / 2.0
        if NSPIN == 2 and spin == 0:
            orgy = orgy + sizey
        if NSPIN == 2 and spin == 1:
            orgy = orgy - sizey
        plt.axes([orgx, orgy, sizex, sizey])
        if NSPIN == 1:
            plt.title(TITLE)
        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)
        if not FLAG_SPD:
            plt.fill_between(ENG - EFERMI, TDOS, color="#cccccc", linewidth=2)
        else:
            plt.plot(ENG - EFERMI, TDOS, color="black", linewidth=2, label="total")
            plt.fill_between(ENG - EFERMI, TDOS, color="#cccccc", linewidth=2)
        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20)
        if FLAG_INTTDOS:
            ax = plt.twinx()
            ax.plot(ENG - EFERMI, INTTDOS, color="black", linewidth=2, label="INTTDOS")
            plt.ylabel("INTTDOS [n]", fontsize=20)
        if not FLAG_SPD:
            TDOS = dos.get_tdos_spd(0, spin)
            plt.plot(ENG - EFERMI, TDOS, color="red", linewidth=2, label="ALL-s")
            TDOS = dos.get_tdos_spd(1, spin)
            plt.plot(ENG - EFERMI, TDOS, color="green", linewidth=2, label="ALL-p")
            TDOS = dos.get_tdos_spd(2, spin)
            plt.plot(ENG - EFERMI, TDOS, color="blue", linewidth=2, label="ALL-d")
            if FLAG_F or LMAX >= 3:
                TDOS = dos.get_tdos_spd(3, spin)
                plt.plot(ENG - EFERMI, TDOS, color="yellow", linewidth=2, label="ALL-f")
        plt.ylim(ymin=0)
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if NSPIN == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0.0])
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    if FLAG_LEFT:
        leg = plt.legend(fontsize=12, loc="upper left")
    else:
        leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    xmin, xmax, ymin, ymax = plt.axis()
    if PORTRAIT_FLAG:
        plt.savefig("TDOS.eps", orientation="portrait")
        plt.savefig("TDOS.pdf", orientation="portrait")
        plt.savefig("TDOS.png", orientation="portrait")
    else:
        plt.savefig("TDOS.eps")
        plt.savefig("TDOS.pdf")
        plt.savefig("TDOS.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
