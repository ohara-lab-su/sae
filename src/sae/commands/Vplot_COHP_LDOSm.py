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
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    dname = "DOSCAR.lobster"
    atom = 1
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-a", "--atom")
    parser.add_option("--all", dest="ALL", action="store_true", default=False)
    parser.add_option("--s", action="store_true", default=False)
    parser.add_option("--p", action="store_true", default=False)
    parser.add_option("--sp", action="store_true", default=False)
    parser.add_option("--up", action="store_true", default=False)
    parser.add_option("--down", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--left", action="store_true", default=False)
    parser.add_option("-n", "--nw", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.DOSCAR:
        dname = options.DOSCAR
    if options.atom:
        atom = int(options.atom)
    if options.ALL:
        options.nw = True
    if len(args) > 0:
        atom = int(args[0])
    return [
        dname,
        atom,
        options.ALL,
        options.s,
        options.p,
        options.sp,
        options.up,
        options.down,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.left,
        options.nw,
    ]


if __name__ == "__main__":
    (
        dname,
        atom,
        ALL_FLAG,
        FLAG_S,
        FLAG_P,
        FLAG_SP,
        OPT_UP,
        OPT_DN,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        FLAG_LEFT,
        NO_WINDOW_FLAG,
    ) = options()
    if OPT_EMAX:
        print("Emax =", OPT_EMAX)
    if OPT_EMIN:
        print("Emin =", OPT_EMIN)
    if OPT_YMAX:
        print("COHP Ymax=", OPT_YMAX)
    if OPT_UP:
        print("SPIN-UP")
        spin = 0
    elif OPT_DN:
        print("SPIN-DOWN")
        spin = 1
    else:
        print("NONMAGNETIC")
        spin = 0
    atom -= 1
    orgx = 0.15
    orgy = 0.08
    off = 0.034
    xsize = 0.75
    ysize0 = 0.74
    if FLAG_S:
        orbit_list = ["s"]
    elif FLAG_P:
        orbit_list = ["p"]
    elif FLAG_SP:
        orbit_list = ["s", "p"]
    else:
        orbit_list = ["s", "p", "d"]
    norbit0 = len(orbit_list)
    dos = ReadLobDos(dname)
    nspin = dos.nspin
    natom = dos.natom
    title = "DOSCAR.lobster"
    efermi = dos.efermi
    eng = dos.eng
    atoms_index_j = dos.atoms_index_j
    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True
    ysize = ysize0 / (float(norbit0) + 1.0)
    atom_label = str(atoms_index_j[atom]) + str(atom + 1)
    if nspin == 1:
        print("atom =", atom + 1, atom_label)
    else:
        print("atom(spin) =", atom + 1, "(" + str(spin + 1) + ")", atom_label)
    if ALL_FLAG:
        a1 = 0
        a2 = natom
    else:
        a1 = int(atom)
        a2 = int(atom) + 1
    for atom in range(a1, a2):
        plt.rcParams["font.size"] = 14
        plt.rcParams["legend.fontsize"] = 5
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        plt.axes([orgx, orgy, xsize, ysize])
        tdos = dos.get_tdos(spin)
        plt.plot(eng, tdos, color="black", linewidth=2, label="total")
        plt.axvline(x=0, color="black", linewidth=1)
        leg = plt.legend(fontsize=12)
        if FLAG_LEFT:
            leg = plt.legend(loc="upper left")
        leg.get_frame().set_alpha(0.5)
        xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=20)
        yl = plt.ylabel("DOS/eV", fontsize=20)
        plt.ylim(ymin=0)
        if OPT_EMAX:
            plt.xlim(xmax=int(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=int(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=int(OPT_YMAX))
        orgy = orgy + ysize + off
        j = 1
        for orbit in orbit_list:
            plt.axes([orgx, orgy, xsize, ysize])
            c = cm.prism(j * 20 / 4)
            ldos = dos.get_ldos(l=orbit, atom=atom, spin=spin)
            plt.plot(
                eng,
                ldos,
                linestyle="-",
                color=c,
                linewidth=2,
                label=atom_label + "-" + str(orbit),
            )
            plt.axvline(x=0, color="black", linewidth=1)
            leg = plt.legend(fontsize=12)
            if FLAG_LEFT:
                leg = plt.legend(loc="upper left")
            leg.get_frame().set_alpha(0.5)
            plt.xticks([])
            plt.ylabel("")
            plt.ylim(ymin=0)
            if OPT_EMAX:
                plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=float(OPT_EMIN))
            if OPT_YMAX:
                plt.ylim(ymax=float(OPT_YMAX))
            orgy = orgy + ysize + off
            j += 1
        if FLAG_SPIN:
            if OPT_UP:
                plt.title(title + "  spin-up (" + str(atom_label) + ") ", fontsize=18)
            if OPT_DN:
                plt.title(title + "  spin-down (" + str(atom_label) + ") ", fontsize=18)
        else:
            plt.title(title + "  (" + str(atom_label) + ") ", fontsize=18)
        plt.savefig("COHP_LDOS" + str(atom + 1) + ".eps")
        plt.savefig("COHP_LDOS" + str(atom + 1) + ".pdf")
        plt.savefig("COHP_LDOS" + str(atom + 1) + ".png")
        if not NO_WINDOW_FLAG:
            plt.show()
        plt.close("all")
