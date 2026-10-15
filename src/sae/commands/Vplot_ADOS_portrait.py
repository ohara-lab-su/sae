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


def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=oname)
    parser.add_option("-n", "--nw", action="store_true", default=False, dest="NOWINDOW")
    parser.add_option(
        "-l", "--landscape", action="store_true", default=False, dest="LANDSCAPE"
    )
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    return [
        dname,
        oname,
        options.NOWINDOW,
        options.LANDSCAPE,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


if __name__ == "__main__":
    dname, oname, NO_WINDOW_FLAG, LANDSCAPE_FLAG, OPT_EMAX, OPT_EMIN, OPT_YMAX = (
        options()
    )
    TDOS_FLAG = True
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    out = sys.stdout
    dos = ReadVaspDoscar(dname)
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    outcar = ReadVaspOutcar(oname)
    NION = outcar.get_nion()
    atoms = outcar.get_atoms_index()
    ENG = dos.get_eng()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    if not LANDSCAPE_FLAG:
        plt.figure(figsize=(7.0, 9.89))
    orgx = 0.13
    orgy = 0.08
    off = 0.015
    size = 0.83 / NION / NSPIN
    for ion in range(NION):
        for spin in range(NSPIN - 1, -1, -1):
            if NSPIN == 1:
                print("ion = %d %s" % (ion + 1, str(atoms[ion])))
            else:
                print(
                    "ion(spin) = %d (%s) %s" % (ion + 1, str(spin + 1), str(atoms[ion]))
                )
            atom = str(atoms[ion])
            plt.axes([orgx, orgy, 0.8, size])
            if NSPIN == 1:
                orgy = orgy + size + off
            if NSPIN == 2:
                if spin == 0:
                    orgy = orgy + size + off
                if spin == 1:
                    orgy = orgy + size
            if TDOS_FLAG:
                TDOS = dos.get_tdos(spin)
                plt.fill_between(
                    ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
                )
            c = "red"
            ADOS = dos.get_ldos_ion(0, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle=":",
                color=c,
                linewidth=2,
                label=atom + "-s",
            )
            c = "green"
            ADOS = dos.get_ldos_ion(1, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom + "-p",
            )
            c = "blue"
            ADOS = dos.get_ldos_ion(2, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="--",
                color=c,
                linewidth=2,
                label=atom + "-d",
            )
            if NSPIN == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([0, ymax])
            if NSPIN == 2:
                xmin, xmax, ymin, ymax = plt.axis()
                if spin == 0:
                    plt.ylim([0, ymax])
                if spin == 1:
                    plt.ylim([ymax, 0])
            if OPT_EMAX:
                plt.xlim(xmax=int(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=int(OPT_EMIN))
            if OPT_YMAX:
                plt.ylim(ymax=int(OPT_YMAX))
            if ion == NION - 1 and spin == 0:
                plt.title(TITLE, fontsize=16)
            if ion != 0:
                plt.xticks([])
            if NSPIN == 1:
                if ion == 0:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            if NSPIN == 2:
                if ion == 0 and spin == 0:
                    plt.xticks([])
                if ion == 0 and spin == 1:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=16)
                    yl = plt.ylabel("DOS/eV", fontsize=16)
            plt.axvline(x=0, color="black", linewidth=1)
            if spin == 0:
                leg = plt.legend(fontsize=12)
                leg.get_frame().set_alpha(0.5)
    if LANDSCAPE_FLAG:
        plt.savefig("ADOS.eps")
        plt.savefig("ADOS.pdf")
        plt.savefig("ADOS.png")
    else:
        plt.savefig("ADOS_portrait.eps", orientation="portrait")
        plt.savefig("ADOS_portrait.pdf", orientation="portrait")
        plt.savefig("ADOS_portrait.png", orientation="portrait")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
