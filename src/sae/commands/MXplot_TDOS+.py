#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.pdos import ReadMxPdos
from sae.openmx.tdos import ReadMxTdos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import matplotlib.pyplot as plt


def options():
    from sae.common.paths import FileDiscovery

    name = "openmx"
    suffix_tdos = ".DOS.Tetrahedron"
    suffix_pdos = ".PDOS.Tetrahedron"
    suffix_tdos_g = ".DOS.Gaussian"
    suffix_pdos_g = ".PDOS.Gaussian"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("-p", "--portrait", action="store_true", default=False)
    parser.add_option("-g", "--gaussian", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--emin", dest="EMIN")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    if options.gaussian:
        print("GAUSSIAN MODE")
        suffix_tdos = suffix_tdos_g
        suffix_pdos = suffix_pdos_g
    if not os.path.exists(name + ".out") or not os.path.exists(name + ".out.gz"):
        try:
            name = FileDiscovery().find_datfile("out")
        except:
            pass
    elif not os.path.exists(name + ".dat") or not os.path.exists(name + ".dat"):
        try:
            name = FileDiscovery().find_datfile("dat")
        except:
            pass
    return [
        name,
        suffix_tdos,
        suffix_pdos,
        options.nw,
        options.portrait,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


if __name__ == "__main__":
    (
        name,
        suffix_tdos,
        suffix_pdos,
        NO_WINDOW_FLAG,
        PORTRAIT_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
    ) = options()
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    dos = ReadMxTdos(name, suffix_tdos)
    pdos = ReadMxPdos(name, suffix_pdos)
    out = sys.stdout
    NSPIN = dos.get_ispin()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = 0.0
    ENG = dos.get_eng()
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    if PORTRAIT_FLAG:
        plt.figure(figsize=(7.0, 9.89))
    for spin in range(NSPIN):
        if NSPIN == 1:
            plt.axes([0.13, 0.13, 0.8, 0.8])
            plt.title(TITLE)
        if NSPIN == 2:
            if spin == 0:
                plt.axes([0.13, 0.53, 0.8, 0.4])
            if spin == 1:
                plt.axes([0.13, 0.13, 0.8, 0.4])
        INTTDOS = dos.get_inttdos(spin)
        TDOS = dos.get_tdos(spin)
        plt.fill_between(
            ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
        )
        TDOS = pdos.get_tdos_spd(0, spin)
        plt.plot(ENG - EFERMI, TDOS, color="red", linewidth=2, label="ALL-s")
        TDOS = pdos.get_tdos_spd(1, spin)
        plt.plot(ENG - EFERMI, TDOS, color="green", linewidth=2, label="ALL-p")
        TDOS = pdos.get_tdos_spd(2, spin)
        plt.plot(ENG - EFERMI, TDOS, color="blue", linewidth=2, label="ALL-d")
        plt.ylim(ymin=0)
        plt.axvline(x=0, color="black", linewidth=1)
        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20)
        if OPT_EMAX:
            plt.xlim(xmax=int(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=int(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=int(OPT_YMAX))
        if NSPIN == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0.0])
        plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    leg = plt.legend(fontsize=12)
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
