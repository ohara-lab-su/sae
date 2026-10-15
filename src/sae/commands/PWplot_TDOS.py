#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.pwscf.out import ReadPwOut
from sae.pwscf.tdos import ReadPwTdos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import matplotlib.pyplot as plt


def options():
    dosname = "input.dos"
    outname = None
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-d", "--outdos", dest="DOS")
    parser.add_option("-o", "--outscf", dest="SCF")
    parser.add_option("-s", "--scf", dest="SCF")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--ymax", dest="YMAX")
    parser.add_option("--emin", dest="EMIN")
    options, args = parser.parse_args()
    if options.INPUT:
        dosname = options.INPUT
    if options.DOS:
        dosname = options.DOS
    if options.SCF:
        outname = options.SCF
    if options.EMAX:
        options.EMAX = float(options.EMAX)
    if options.EMIN:
        options.EMIN = float(options.EMIN)
    if options.YMAX:
        options.YMAX = float(options.YMAX)
    return (dosname, outname, options.EMAX, options.EMIN, options.YMAX)


if __name__ == "__main__":
    dosname, outname, OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
    if outname is not None:
        out = ReadPwOut(outname)
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if OPT_YMAX:
        print("Ymax=", OPT_YMAX)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    pw = ReadPwTdos(dosname)
    for spin in range(pw.ispin):
        orgx = 0.13
        orgy = 0.13
        xsize = 0.8
        ysize = 0.7
        if pw.ispin > 1:
            ysize = ysize / 3.0
            if spin == 0:
                orgy = orgy + ysize
            if spin == 1:
                orgy = orgy
        else:
            ysize = ysize / 2.0
        plt.axes([orgx, orgy, xsize, ysize])
        pw.dos = pw.get_tdos(spin=spin)
        if outname is None:
            plt.plot(pw.eng, pw.dos, linewidth=1, label="total")
        else:
            plt.plot(pw.eng - out.efermi, pw.dos, linewidth=1, label="total")
            plt.axvline(x=0, color="black", linewidth=1)
        plt.ylim(ymin=0)
        if spin == 0:
            plt.ylabel("DOS/eV", fontsize=20)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        if pw.ispin == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                xmin, xmax, ymin, ymax = plt.axis()
                plt.ylim([ymax, 0])
    if outname is None:
        plt.xlabel("Energy [eV]", fontsize=20)
    else:
        plt.xlabel("$E - E_{\\mathrm{F}}$ [eV]", fontsize=20)
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")
    plt.show()
    plt.close("all")
