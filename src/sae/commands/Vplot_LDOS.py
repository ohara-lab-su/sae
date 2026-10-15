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
import os
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=oname)
    parser.add_option("-a", "--atom")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--title")
    parser.add_option("--total", action="store_true", default=False)
    parser.add_option("--vbm", action="store_true", default=False)
    parser.add_option("--shift")
    parser.add_option("--left", action="store_true", default=False)
    parser.add_option("--noef", action="store_true", default=False)
    parser.add_option("--pdf")
    parser.add_option("-n", "--nw", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.OUTCAR:
        oname = options.OUTCAR
    if options.atom:
        options.atom = int(options.atom)
    plot_atoms = []
    if len(args) > 0:
        for i in range(0, len(args)):
            plot_atoms.append(int(args[i]))
    else:
        plot_atoms = [1]
    return [
        dname,
        oname,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.title,
        options.atom,
        plot_atoms,
        options.total,
        options.vbm,
        options.shift,
        options.left,
        options.noef,
        options.pdf,
        options.nw,
    ]


if __name__ == "__main__":
    (
        dname,
        oname,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_TITLE,
        plot_atom,
        plot_atoms,
        FLAG_TOT,
        FLAG_VBM,
        OPT_SHIFT,
        FLAG_LEFT,
        FLAG_NOEF,
        FLAG_PDF,
        FLAG_NW,
    ) = options()
    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))
    if len(plot_atoms) > 1:
        print("Plot Atoms:")
        for i in plot_atoms:
            print("%d" % i, end="")
        print("")
    elif plot_atom:
        plot_atoms[0] = plot_atom
    print(plot_atoms)
    out = sys.stdout
    dos = ReadVaspDoscar(dname)
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    LMAX = dos.lmax
    ENG = dos.eng
    if not OPT_TITLE:
        TITLE = dos.title
    else:
        TITLE = str(OPT_TITLE)
    if FLAG_VBM:
        EFERMI0 = dos.efermi
        print("SEARCH VBM MODE")
        print("  ORIGINAL EF =", end="")
        print(EFERMI0)
        EFERMI = dos.get_vbm()
        print("          VBM = %s" % str(EFERMI), end="")
    if OPT_SHIFT:
        print("EF_SHIFT MODE")
        print("     NEW EF =")
        EFERMI = float(OPT_SHIFT)
    if os.path.exists(oname) or os.path.exists(oname + ".gz"):
        FLAG_OUTCAR = True
        outcar = ReadVaspOutcar(oname)
        NION = outcar.get_nion()
        atoms = outcar.get_atoms_index()
        atoms_j = outcar.get_atoms_j()
    plt.rcParams["font.size"] = 18
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    orgx = 0.13
    orgy = 0.13
    xsize = 0.8
    ysize0 = 0.8
    ysize = 0.8 / NSPIN
    if NSPIN == 1:
        spin_list = [0]
    if NSPIN == 2:
        spin_list = [1, 0]
    for spin in spin_list:
        plt.axes([orgx, orgy, xsize, ysize])
        if NSPIN == 1:
            plt.title(TITLE)
            plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
        if NSPIN == 2 and spin == 0:
            plt.title(TITLE)
        if NSPIN == 2 and spin == 1:
            plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
        j = 0
        for atom in plot_atoms:
            if len(plot_atoms) > 1:
                if atom == 0:
                    sys.exit("STOP:INPUT ERROR, atom= 0")
            atom -= 1
            if FLAG_OUTCAR:
                atom_label = str(atoms[atoms_j[atom]]) + str(atom + 1)
                if NSPIN == 1:
                    print("atom = %s %s" % (str(atom + 1), str(atom_label)))
                else:
                    print(
                        "atom(spin) = %d (%s) %s"
                        % (atom + 1, str(spin + 1), str(atom_label))
                    )
            else:
                atom_label = str(atom)
                if NSPIN == 1:
                    print("atom = %s" % str(atom + 1))
                else:
                    print("atom(spin) = %d (%s)" % (atom + 1, str(spin + 1)))
            if not FLAG_TOT:
                INTTDOS = dos.get_inttdos(spin)
                TDOS = dos.get_tdos(spin)
                plt.fill_between(
                    ENG - EFERMI, TDOS, color="#cccccc", linewidth=2, label="total"
                )
            c = cm.prism(float(j) / (NATOM * (LMAX + 1)))
            LDOS = dos.get_ldos(l="s", atom=atom, spin=spin)
            plt.plot(
                ENG - EFERMI,
                LDOS,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom_label + "-s",
            )
            j += 1
            if LMAX >= 1:
                c = cm.prism(float(j) / (NATOM * (LMAX + 1)))
                LDOS = dos.get_ldos(l="p", atom=atom, spin=spin)
                plt.plot(
                    ENG - EFERMI,
                    LDOS,
                    linestyle="-",
                    color=c,
                    linewidth=2,
                    label=atom_label + "-p",
                )
                j += 1
            if LMAX >= 2:
                c = cm.prism(float(j) / (NATOM * (LMAX + 1)))
                LDOS = dos.get_ldos(l="d", atom=atom, spin=spin)
                plt.plot(
                    ENG - EFERMI,
                    LDOS,
                    linestyle="-",
                    color=c,
                    linewidth=2,
                    label=atom_label + "-d",
                )
                j += 1
            if LMAX >= 3:
                c = cm.prism(float(j) / (NATOM * (LMAX + 1)))
                LDOS = dos.get_ldos(l="f", atom=atom, spin=spin)
                plt.plot(
                    ENG - EFERMI,
                    LDOS,
                    linestyle="-",
                    color=c,
                    linewidth=2,
                    label=atom_label + "-f",
                )
                j += 1
            plt.ylim(ymin=0)
        if spin == 0:
            yl = plt.ylabel("DOS/eV", fontsize=20)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if NSPIN == 2 and spin == 0:
            plt.xticks([])
        if NSPIN == 2 and spin == 1:
            xmin, xmax, ymin, ymax = plt.axis()
            plt.ylim([ymax, 0])
        if not FLAG_NOEF:
            plt.axvline(x=0, color="black", linewidth=1)
        orgy = orgy + ysize
    leg = plt.legend(fontsize=12)
    if FLAG_LEFT:
        leg = plt.legend(loc="upper left")
    leg.get_frame().set_alpha(0.5)
    if plot_atom:
        tail = str(plot_atom)
    else:
        tial = ""
    plt.savefig("LDOS" + tial + ".pdf")
    if FLAG_PDF:
        plt.savefig("LDOS" + tail + ".eps")
        plt.savefig("LDOS" + tail + ".png")
    if not FLAG_NW:
        plt.show()
    plt.close("all")
