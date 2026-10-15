#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.wien2k.dos import ReadWienDos
from sae.wien2k.output0 import ReadWienOutput0

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    name = re.sub(".*/", "", os.getcwd())
    unit = "ev"
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-e", "--ev", action="store_true", default=False)
    parser.add_option("-f", "--fermi", action="store_true", default=False)
    parser.add_option("-n", "--nw", action="store_true", default=False)
    parser.add_option("-a", "--atomtot", action="store_true", default=False)
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.ev:
        unit = "ev"
    else:
        unit = "None"
    if options.INPUT:
        name = options.INPUT
    plot_ions = []
    if len(args) > 0:
        for i in range(0, len(args)):
            plot_ions.append(int(args[i]))
    else:
        plot_ions = [1]
    return [
        name,
        unit,
        options.fermi,
        options.nw,
        options.atomtot,
        options.EMAX,
        options.EMIN,
        options.YMAX,
        plot_ions,
    ]


if __name__ == "__main__":
    (
        case,
        unit,
        FERMI,
        NO_WINDOW_FLAG,
        AT_FLAG,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        plot_ions,
    ) = options()
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    if len(plot_ions) > 1:
        print("Plot Ions:")
        for i in plot_ions:
            print(i, end="")
        print("")
    lists = FileDiscovery().find_suffix3(case + ".dos", unit)
    if not lists:
        sys.exit("STOP: " + case + ".dos* file not found")
    print("READ FILE    :", end="")
    for i in lists:
        print(i, end="")
    print("")
    if unit == "ev":
        unit = "eV"
        FERMI = True
    else:
        unit = "Ry"
    if os.path.exists(case + ".output0"):
        output0_file = case + ".output0"
    elif os.path.exists(case + ".output0.gz"):
        output0_file = case + ".output0.gz"
    elif os.path.exists(case + ".output0000"):
        output0_file = case + ".output0000"
    elif os.path.exists(case + ".output0000.gz"):
        output0_file = case + ".output0000.gz"
    else:
        sys.exit("STOP: output0 file not found")
    output0 = ReadWienOutput0(output0_file)
    nspin = output0.get_ispin()
    nion = output0.get_nion()
    ions_index = output0.get_ions_index()
    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True
    if len(plot_ions) > nion:
        sys.exit("STOP: nion=" + str(nion))
    if max(plot_ions) > nion:
        sys.exit("STOP: nion=" + str(nion))
    if FLAG_SPIN:
        up = []
        dn = []
        for i in lists:
            up.append(re.sub("up", "", re.sub("dn", "", i)) + "up")
            dn.append(re.sub("up", "", re.sub("dn", "", i)) + "dn")
        up_lists = list(set(up))
        dn_lists = list(set(dn))
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    for spin in range(nspin):
        if FLAG_SPIN and spin == 0:
            lists = up_lists
        if FLAG_SPIN and spin == 1:
            lists = dn_lists
        dos = ReadWienDos(lists)
        nion = dos.get_nion()
        nedos = dos.get_nedos()
        efermi = dos.get_efermi()
        emax = dos.get_emax()
        emin = dos.get_emin()
        eng = dos.get_eng()
        title = case
        if nspin == 1:
            plt.axes([0.13, 0.13, 0.8, 0.8])
            plt.title(title)
        if nspin == 2:
            if spin == 0:
                plt.axes([0.13, 0.53, 0.8, 0.4])
                plt.title(title)
            if spin == 1:
                plt.axes([0.13, 0.13, 0.8, 0.4])
        j = 0
        for ion in plot_ions:
            if len(plot_ions) > 1:
                if ion == 0:
                    sys.exit("STOP:INPUT ERROR, ion= 0")
            ion_label = str(ions_index[ion - 1])
            if nspin == 1:
                print("ion =", ion, ion_label)
            else:
                print("ion(spin) =", ion, "(" + str(spin + 1) + ")", ion_label)
            e = []
            for i in range(nedos):
                if FERMI:
                    e.append(eng[i] - efermi)
                else:
                    e.append(eng[i])
            TDOS_FLAG = True
            if dos.chk_raw_dos(atom=0, orbit="total-DOS"):
                tdos = dos.get_raw_dos(atom=ion, orbit="total-DOS")
                plt.fill_between(e, tdos, color="#cccccc", linewidth=2, label="total")
            else:
                TDOS_FLAG = False
            if dos.chk_raw_dos(atom=ion, orbit="total") and AT_FLAG:
                t = dos.get_raw_dos(atom=ion, orbit="total")
                if TDOS_FLAG:
                    c = "black"
                    plt.plot(
                        e,
                        t,
                        linestyle=":",
                        color=c,
                        linewidth=2,
                        label=ion_label + "-tot",
                    )
                else:
                    plt.fill_between(
                        e, t, color="#cccccc", linewidth=2, label=ion_label + "-tot"
                    )
            if dos.chk_raw_dos(atom=ion, orbit="s"):
                s = dos.get_raw_dos(atom=ion, orbit="s")
                c = cm.prism(float(j) / (nion * 2))
                plt.plot(
                    e, s, linestyle=":", color=c, linewidth=2, label=ion_label + "-s"
                )
                j += 1
            if dos.chk_raw_dos(atom=ion, orbit="p"):
                p = dos.get_raw_dos(atom=ion, orbit="p")
                c = cm.prism(float(j) / (nion * 2))
                plt.plot(
                    e, p, linestyle="-", color=c, linewidth=2, label=ion_label + "-p"
                )
                j += 1
            if dos.chk_raw_dos(atom=ion, orbit="d"):
                d = dos.get_raw_dos(atom=ion, orbit="d")
                c = cm.prism(float(j) / (nion * 2))
                plt.plot(
                    e, d, linestyle="--", color=c, linewidth=2, label=ion_label + "-d"
                )
                j += 1
            if dos.chk_raw_dos(atom=ion, orbit="f"):
                f = dos.get_raw_dos(atom=ion, orbit="f")
                c = cm.prism(float(j) / (nion * 2))
                plt.plot(
                    e, f, linestyle="-.", color=c, linewidth=2, label=ion_label + "-f"
                )
                j += 1
            plt.ylim(ymin=0)
        if spin == 0:
            yl = plt.ylabel("DOS/" + unit, fontsize=20)
        if OPT_EMAX:
            plt.xlim(xmax=int(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=int(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=int(OPT_YMAX))
        if nspin == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0])
        if FERMI:
            plt.axvline(x=0, color="black", linewidth=1)
        else:
            plt.axvline(x=efermi, color="black", linewidth=1)
    if FERMI:
        plt.xlabel("$E -  E_{\\mathrm{F}}$ [" + unit + "]", fontsize=20)
    else:
        plt.xlabel("$E$ [" + unit + "]", fontsize=20)
    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)
    plt.savefig("LDOS.eps")
    plt.savefig("LDOS.pdf")
    plt.savefig("LDOS.png")
    if not NO_WINDOW_FLAG:
        plt.show()
    plt.close("all")
