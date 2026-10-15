#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar
from sae.vasp.outcar import ReadVaspOutcar

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
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=oname)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--title")
    parser.add_option("--up", action="store_true", default=False)
    parser.add_option("--dn", "--down", dest="dn", action="store_true", default=False)
    parser.add_option("--total", action="store_true", default=False)
    parser.add_option("--vbm", action="store_true")
    parser.add_option("--shift")
    parser.add_option("--left", action="store_true")
    parser.add_option("--noef", action="store_true")
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.title,
        options.up,
        options.dn,
        options.total,
        options.vbm,
        options.shift,
        options.left,
        options.noef,
        options.NOWINDOW,
    ]


if __name__ == "__main__":
    (
        dname,
        oname,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_TITLE,
        FLAG_UP,
        FLAG_DN,
        FLAG_TOT,
        FLAG_VBM,
        OPT_SHIFT,
        FLAG_LEFT,
        FLAG_NOEF,
        FLAG_NW,
    ) = options()
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    out = sys.stdout
    print("READ %s" % str(dname))
    dos = ReadVaspDoscar(dname)
    print("END READ")
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    ENG = dos.get_eng()
    LMAX = dos.lmax
    if not OPT_TITLE:
        TITLE = dos.get_title()
    else:
        TITLE = OPT_TITLE
    if FLAG_VBM:
        EFERMI0 = dos.efermi
        print("SEARCH VBM MODE")
        print("  ORIGINAL EF =", end="")
        print(EFERMI0)
        EFERMI = dos.get_vbm()
        print("          VBM = %s" % str(EFERMI))
    if OPT_SHIFT:
        print("EF_SHIFT MODE")
        print("     NEW EF =")
        EFERMI = float(OPT_SHIFT)
    print("READ %s" % str(oname))
    outcar = ReadVaspOutcar(oname)
    print("END READ")
    NION = outcar.get_nion()
    atoms = outcar.get_atoms_index()
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    orgx = 0.15
    orgy = 0.143
    off = 0.0
    xsize = 0.75
    ysize0 = 0.75
    if NSPIN >= 2:
        print("SPIN MODE")
        spin_index = ["up", "dn"]
        if FLAG_UP:
            spin_list = [0]
            out_suffix = "_up"
            ysize = ysize0
            FLAG_BOTH_SPIN = False
        elif FLAG_DN:
            spin_list = [1]
            out_suffix = "_dn"
            ysize = ysize0
            FLAG_BOTH_SPIN = False
        else:
            spin_list = [1, 0]
            out_suffix = ""
            ysize = ysize0 / 2.0
            FLAG_BOTH_SPIN = True
    else:
        print("NONMAGNETIC MODE")
        spin_list = [0]
        out_suffix = ""
        ysize = ysize0
        FLAG_BOTH_SPIN = False
    FLAG_YTICKS = False
    for spin in spin_list:
        plt.axes([orgx, orgy, xsize, ysize])
        if not FLAG_TOT:
            INTTDOS = dos.get_inttdos(spin)
            TDOS = dos.get_tdos(spin)
            plt.fill_between(
                ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
            )
        j = 0
        for ion in range(NION):
            atom = str(atoms[ion])
            if NSPIN == 1:
                print("ion = %d %s" % (ion + 1, str(atom)))
            else:
                print(
                    "ion (spin) : %d (%s) %s"
                    % (ion + 1, str(spin_index[spin]), str(atom))
                )
            c = cm.prism(float(j) / (3 * NION))
            ADOS = dos.get_ldos_ion(0, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle=":",
                color=c,
                linewidth=2,
                label=atom + "-s",
            )
            j += 1
            c = cm.prism(float(j) / (3 * NION))
            ADOS = dos.get_ldos_ion(1, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom + "-p",
            )
            j += 1
            if LMAX >= 2:
                c = cm.prism(float(j) / (3 * NION))
                ADOS = dos.get_ldos_ion(2, ion, spin)
                plt.plot(
                    ENG - EFERMI,
                    ADOS,
                    linestyle="--",
                    color=c,
                    linewidth=2,
                    label=atom + "-d",
                )
                j += 1
            if LMAX >= 3:
                c = cm.prism(float(j) / (3 * NION))
                ADOS = dos.get_ldos_ion(3, ion, spin)
                plt.plot(
                    ENG - EFERMI,
                    ADOS,
                    linestyle="-.",
                    color=c,
                    linewidth=2,
                    label=atom + "-f",
                )
                j += 1
            plt.ylim(ymin=0)
        if not FLAG_YTICKS:
            yl = plt.ylabel("DOS/eV", fontsize=20)
            xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
            FLAG_YTICKS = True
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if FLAG_BOTH_SPIN:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0])
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
        orgy = orgy + off + ysize
    if FLAG_UP:
        plt.title(TITLE + " (up-spin)")
    elif FLAG_DN:
        plt.title(TITLE + " (dn-spin)")
    else:
        plt.title(TITLE)
    if FLAG_LEFT:
        leg = plt.legend(fontsize=12, loc="upper left")
    else:
        leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    plt.savefig("ADOS" + out_suffix + ".pdf")
    if not FLAG_NW:
        plt.show()
    plt.close("all")
