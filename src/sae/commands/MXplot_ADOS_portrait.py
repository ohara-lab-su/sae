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
    parser.add_option("-d", "--dat", dest="DATFILE")
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option(
        "-l", "--landscape", action="store_true", default=False, dest="LANDSCAPE"
    )
    parser.add_option("-g", "--gaussian", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.gaussian:
        print("GAUSSIAN MODE")
        suffix_tdos = suffix_tdos_g
        suffix_pdos = suffix_pdos_g
    if not os.path.exists(name + ".out") or not os.path.exists(name + ".out.gz"):
        try:
            options.INPUT = FileDiscovery().find_datfile("out")
        except:
            pass
    elif not os.path.exists(name + ".dat") or not os.path.exists(name + ".dat"):
        try:
            options.INPUT = FileDiscovery().find_datfile("dat")
        except:
            pass
    if not options.DATFILE:
        options.DATFILE = options.INPUT
    return [
        options.INPUT,
        options.DATFILE,
        suffix_tdos,
        suffix_pdos,
        options.nw,
        options.LANDSCAPE,
        options.EMAX,
        options.EMIN,
        options.YMAX,
    ]


if __name__ == "__main__":
    (
        name,
        datname,
        suffix_tdos,
        suffix_pdos,
        NO_WINDOW_FLAG,
        LANDSCAPE_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
    ) = options()
    TDOS_FLAG = True
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    out = sys.stdout
    module_name = "sae._class_registry"
    FLAG_DATFILE = False
    if os.path.exists(datname + ".out") or os.path.exists(datname + ".out" + ".gz"):
        class_name = "ReadMxOut"
        datname = datname + ".out"
    elif os.path.exists(datname + ".dat") or os.path.exists(datname + ".dat" + ".gz"):
        class_name = "ReadMxDat"
        datname = datname + ".dat"
    else:
        sys.exit("STOP: " + datname + ".dat or .dat.gz file not found")
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    dat = klass(datname)
    NION = dat.get_nion()
    NSPIN = dat.get_ispin()
    NATOM = dat.get_natom()
    TITLE = dat.get_title()
    EFERMI = 0.0
    atoms = dat.get_atoms_index()
    tdos = ReadMxTdos(name, suffix_tdos)
    EMAX = tdos.get_emax()
    EMIN = tdos.get_emin()
    NEDOS = tdos.get_nedos()
    ENG = tdos.get_eng()
    pdos = ReadMxPdos(name, suffix_pdos)
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
                print("ion = ", ion + 1, atoms[ion])
            else:
                print("ion(spin) = ", ion + 1, "(" + str(spin + 1) + ")", atoms[ion])
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
                TDOS = tdos.get_tdos(spin)
                plt.fill_between(
                    ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
                )
            c = "red"
            ADOS = pdos.get_ldos_ion(0, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle=":",
                color=c,
                linewidth=2,
                label=atom + "-s",
            )
            c = "green"
            ADOS = pdos.get_ldos_ion(1, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom + "-p",
            )
            c = "blue"
            ADOS = pdos.get_ldos_ion(2, ion, spin)
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
