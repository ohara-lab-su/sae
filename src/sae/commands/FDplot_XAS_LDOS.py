#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt

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
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = optparse.OptionParser()
    parser.add_option("-i", "--inpname", dest="INPUT")
    parser.add_option("-f", "--filout")
    parser.add_option("-a", "--atom")
    parser.add_option("-l", "--orbit")
    parser.add_option("--fermi", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.filout
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    if len(args) > 0:
        inpname = args[0]
    return [inpname, options.filout, options.atom, options.orbit, options.fermi]


if __name__ == "__main__":
    inpname, filout, atom, orbit, FLAG_fermi = options()
    if not atom:
        atom = 0
    suffix_sd = "_sd" + str(atom) + ".txt"
    suffix_conv = "_conv.txt"
    if not orbit:
        orbit = 1
    inp = ReadFdmInp(inpname)
    ispin = inp.ispin
    if not filout:
        filout = inp.filout
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.17
    orgy = 0.08
    off = 0.01
    xsize = 0.75
    ysize0 = 0.83
    orbit_list = ["s", "p", "d"]
    norbit = len(orbit_list)
    ysize = ysize0 / (norbit + 1)
    num = 0
    txt = ReadFdmTxt(filout, ".txt")
    conv = ReadFdmConv(filout, suffix_conv)
    sd0 = ReadFdmSd(filout, "_sd0.txt")
    if not inp.get_energygpho() and (not FLAG_fermi):
        print("current mode is Fermi")
        print("---> convert to PhotoEnergy")
        print("     + E_edge")
        eng_off = txt.E_edge
    if not inp.get_energygpho() and FLAG_fermi:
        print("current mode is Fermi")
        print("---> subtract E_fermi")
        print("     - E_fermi")
        eng_off = -txt.E_fermi
    if inp.get_energygpho() and FLAG_fermi:
        print("current mode is PhotoEnergy")
        print("---> convert to EF0 mode")
        print("     - E_edge - E_fermi")
        eng_off - txt.E_Fermi - txt.E_edge
    EF0 = txt.E_edge + txt.E_Fermi
    plt.axes([orgx, orgy, xsize, ysize])
    xas = conv.get_xas()
    engx = conv.get_eng() + eng_off
    label = "XAS"
    color = cm.prism(float(num + 1) / float(norbit))
    plt.plot(engx, xas, linewidth=2, color=color, label=label)
    plt.axvline(x=EF0, color="black", linewidth=1)
    plt.ylim(ymin=0)
    leg = plt.legend(loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    orgy = orgy + ysize + off
    sd = ReadFdmSd(filout, suffix_sd)
    for orbit in orbit_list:
        plt.axes([orgx, orgy, xsize, ysize])
        dos = sd.get_ldos(l=orbit)
        eng = sd.get_eng() + eng_off
        num += 1
        label = str(atom) + "-" + orbit
        color = cm.prism((num + 1) * 10)
        plt.plot(eng, dos, linewidth=2, color=color, label=label)
        plt.axvline(x=EF0, color="black", linewidth=1)
        plt.ylim(ymin=0)
        plt.xticks([])
        leg = plt.legend(loc="upper right")
        leg.get_frame().set_alpha(0.5)
        orgy = orgy + ysize + off
    plt.savefig("XAS_LDOS" + str(atom) + ".pdf")
    plt.show()
    plt.close("all")
