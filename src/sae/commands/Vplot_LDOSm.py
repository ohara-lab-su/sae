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
import os
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    dname = "DOSCAR"
    oname = "OUTCAR"
    atom = 1
    parser = optparse.OptionParser()
    parser.add_option("-d", "--doscar", dest="DOSCAR", default=dname)
    parser.add_option("-o", "--outcar", dest="OUTCAR", default=oname)
    parser.add_option("-a", "--atom")
    parser.add_option("--all", dest="ALL", action="store_true", default=False)
    parser.add_option("--s", action="store_true", default=False)
    parser.add_option("--p", action="store_true", default=False)
    parser.add_option("--d", action="store_true", default=False)
    parser.add_option("--f", action="store_true", default=False)
    parser.add_option("--sp", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("--spdf", action="store_true", default=False)
    parser.add_option("--total", action="store_true", default=False)
    parser.add_option("--up", action="store_true", default=False)
    parser.add_option("--down", action="store_true", default=False)
    parser.add_option("--spin", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--title")
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
        atom = int(options.atom)
    if options.ALL:
        options.nw = True
    if len(args) > 0:
        atom = int(args[0])
    return [
        dname,
        oname,
        atom,
        options.ALL,
        options.s,
        options.p,
        options.d,
        options.f,
        options.sp,
        options.spd,
        options.spdf,
        options.total,
        options.up,
        options.down,
        options.spin,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        options.title,
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
        atom,
        ALL_FLAG,
        FLAG_S,
        FLAG_P,
        FLAG_D,
        FLAG_F,
        FLAG_SP,
        FLAG_SPD,
        FLAG_SPDF,
        FLAG_TOT,
        FLAG_UP,
        FLAG_DN,
        FLAG_SPIN,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_TITLE,
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
    atom -= 1
    orgx = 0.15
    orgy = 0.08
    off = 0.015
    xsize = 0.75
    ysize0 = 0.71
    dos = ReadVaspDoscar(dname)
    natom = dos.natom
    efermi = dos.efermi
    eng = dos.eng
    nspin = dos.ispin
    lmax = dos.lmax
    print("lmax = %s" % str(lmax))
    if not OPT_TITLE:
        title = dos.title
    else:
        title = OPT_TITLE
    if FLAG_VBM:
        print("EF SHIFT")
        efermi0 = dos.efermi
        efermi = dos.get_vbm()
        print(efermi0, efermi)
    if OPT_SHIFT:
        efermi = float(OPT_SHIFT)
    if FLAG_S:
        orbit_list = ["s"]
        orbit_out = "_s"
    elif FLAG_P:
        orbit_list = ["p"]
        orbit_out = "_p"
    elif FLAG_D:
        orbit_list = ["d"]
        orbit_out = "_d"
    elif FLAG_F:
        orbit_list = ["f"]
        orbit_out = "_f"
    elif FLAG_SP:
        orbit_list = ["s", "p"]
        orbit_out = "_sp"
    elif FLAG_SPD:
        orbit_list = ["s", "p", "d"]
        orbit_out = "_spd"
    elif FLAG_SPDF:
        orbit_list = ["s", "p", "d", "f"]
        orbit_out = "_spdf"
    else:
        if lmax >= 1:
            orbit_list = ["s", "p"]
            orbit_out = "_sp"
        if lmax >= 2:
            orbit_list = ["s", "p", "d"]
            orbit_out = "_spd"
        if lmax >= 3:
            orbit_list = ["s", "p", "d", "f"]
            orbit_out = "_spdf"
    print("orbit list=", orbit_list)
    norbit0 = len(orbit_list)
    print("NSPIN = %s" % str(nspin))
    FLAG_SPIN = False
    norbit = norbit0
    if FLAG_UP:
        print("SPIN-UP")
        spin = 0
        spin_list = [0]
        spin_name = ["_up", ""]
        spin_out = "_up"
    elif FLAG_DN:
        print("SPIN-DOWN")
        spin = 1
        spin_list = [1]
        spin_name = ["", "_dn"]
        spin_out = "_dn"
    elif FLAG_SPIN or nspin >= 2:
        print("BOTH SPIN ( UP, DOWN-SPIN )")
        spin = 1
        spin_list = [1, 0]
        spin_name = ["_up", "_dn"]
        spin_out = "_spin"
        norbit = norbit0 * 2
        FLAG_SPIN = True
    else:
        print("NONMAGNETIC or SPIN-UP ")
        spin = 0
        spin_list = [0]
        spin_name = [""]
        spin_out = ""
    ysize = ysize0 / (norbit + 1)
    if os.path.exists(oname) or os.path.exists(oname + ".gz"):
        FLAG_OUTCAR = True
        outcar = ReadVaspOutcar(oname)
        atoms_index_j = outcar.atoms_index_j
    if FLAG_OUTCAR:
        atom_label = atoms_index_j[atom] + str(atom + 1)
        print("atom = %d %s" % (atom + 1, str(atom_label + spin_out)))
    else:
        atom_label = str(atom)
        print("atom = %d %s" % (atom + 1, str(atom_label + spin_out)))
    if ALL_FLAG:
        a1 = 0
        a2 = natom
        print("plot atom number: #%s -%s" % (str(a1), str(a2)))
    else:
        a1 = int(atom)
        a2 = int(atom) + 1
        print("plot atom number: #%s" % str(a2))
    for atom in range(a1, a2):
        plt.rcParams["font.size"] = 15
        plt.rcParams["legend.fontsize"] = 10
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        XTICKS_FLAG = False
        if not FLAG_TOT:
            for spin in spin_list:
                plt.axes([orgx, orgy, xsize, ysize])
                tdos = dos.get_tdos(spin)
                label = "total" + spin_name[spin]
                plt.plot(eng - efermi, tdos, color="black", linewidth=2, label=label)
                if not FLAG_NW:
                    plt.axvline(x=0, color="black", linewidth=1)
                if FLAG_SPIN:
                    plt.locator_params(axis="y", nbins=4)
                if not XTICKS_FLAG:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=15)
                    yl = plt.ylabel("DOS/eV", fontsize=15)
                    XTICKS_FLAG = True
                else:
                    plt.xticks([])
                if FLAG_SPIN and spin == 1:
                    xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                    plt.ylim([ymax_dn, 0])
                else:
                    plt.ylim(ymin=0)
                if OPT_EMAX:
                    plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=float(OPT_EMIN))
                if OPT_YMAX:
                    plt.ylim(ymax=float(OPT_YMAX))
                leg = plt.legend(fontsize=12)
                if FLAG_LEFT:
                    leg = plt.legend(loc="upper left")
                leg.get_frame().set_alpha(0.5)
                orgy = orgy + ysize
            orgy = orgy + off
        j = 1
        for orbit in orbit_list:
            for spin in spin_list:
                plt.axes([orgx, orgy, xsize, ysize])
                d = dos.get_ldos(l=orbit, atom=atom, spin=spin)
                e = eng - efermi
                c = cm.prism(j * 20 / norbit0)
                lab = atom_label + "_" + str(orbit) + spin_name[spin]
                plt.plot(e, d, linestyle="-", color=c, linewidth=2, label=lab)
                if not FLAG_NOEF:
                    plt.axvline(x=0, color="black", linewidth=1)
                if FLAG_SPIN:
                    plt.locator_params(axis="y", nbins=4)
                if not XTICKS_FLAG:
                    xl = plt.xlabel("$E -  E_{\\mathrm{F}}$ [eV]", fontsize=15)
                    yl = plt.ylabel("DOS/eV", fontsize=15)
                    XTICKS_FLAG = True
                else:
                    plt.xticks([])
                if spin == 0:
                    plt.ylim(ymin=0)
                    xmin_up, xmax_up, ymin_up, ymax_up = plt.axis()
                    plt.ylim([0, ymax_up])
                if FLAG_SPIN and spin == 1:
                    xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                    plt.ylim([ymax_dn, 0])
                leg = plt.legend(fontsize=12)
                if FLAG_LEFT:
                    leg = plt.legend(loc="upper left")
                leg.get_frame().set_alpha(0.5)
                plt.ylabel("")
                if OPT_EMAX:
                    plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN:
                    plt.xlim(xmin=float(OPT_EMIN))
                if OPT_YMAX:
                    plt.ylim(ymax=float(OPT_YMAX))
                orgy = orgy + ysize
            orgy = orgy + off
            j += 1
        plt.savefig("LDOS" + str(atom + 1) + orbit_out + spin_out + ".pdf")
        if FLAG_PDF:
            plt.savefig("LDOS" + str(atom + 1) + orbit_out + spin_out + ".eps")
            plt.savefig("LDOS" + str(atom + 1) + orbit_out + spin_out + ".png")
        if not FLAG_NW:
            plt.show()
        plt.close("all")
