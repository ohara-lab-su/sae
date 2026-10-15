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
import matplotlib.cm as cm


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
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    for spin in range(NSPIN):
        if NSPIN == 1:
            plt.axes([0.13, 0.13, 0.8, 0.8])
            plt.title(TITLE)
        if NSPIN == 2:
            if spin == 0:
                plt.axes([0.13, 0.53, 0.8, 0.4])
                plt.title(TITLE)
            if spin == 1:
                plt.axes([0.13, 0.13, 0.8, 0.4])
        INTTDOS = tdos.get_inttdos(spin)
        TDOS = tdos.get_tdos(spin)
        plt.fill_between(
            ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
        )
        j = 0
        for ion in range(NION):
            if NSPIN == 1:
                print("ion = ", ion + 1, atoms[ion])
            else:
                print("ion(spin) = ", ion + 1, "(" + str(spin + 1) + ")", atoms[ion])
            atom = str(atoms[ion])
            c = cm.prism(float(j) / (3 * NION))
            ADOS = pdos.get_ldos_ion(0, ion, spin)
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
            ADOS = pdos.get_ldos_ion(1, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom + "-p",
            )
            j += 1
            c = cm.prism(float(j) / (3 * NION))
            ADOS = pdos.get_ldos_ion(2, ion, spin)
            plt.plot(
                ENG - EFERMI,
                ADOS,
                linestyle="--",
                color=c,
                linewidth=2,
                label=atom + "-d",
            )
            j += 1
            plt.ylim(ymin=0)
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
                plt.ylim([ymax, 0])
        plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    plt.savefig("ADOS.eps")
    plt.savefig("ADOS.pdf")
    plt.savefig("ADOS.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
