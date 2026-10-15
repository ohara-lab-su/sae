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
    parser.add_option("-d", "--outdos", dest="DOS")
    parser.add_option("-o", "--outscf", dest="SCF")
    options, args = parser.parse_args()
    if options.DOS:
        dosname = options.DOS
    if options.SCF:
        outname = options.SCF
    return (dosname, outname)


if __name__ == "__main__":
    dosname, outname = options()
    if outname is not None:
        out = ReadPwOut(outname)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.17
    orgy = 0.08
    off = 0.01
    xsize = 0.75
    ysize = 0.83 / 2.0
    plt.axes([orgx, orgy, xsize, ysize])
    pw = ReadPwTdos(dosname)
    pw.dos_up = pw.get_tdos(spin=0)
    if outname is None:
        plt.plot(pw.eng, pw.dos_up, linewidth=1, label="PWSCF TDOS")
    else:
        plt.plot(pw.eng - out.efermi, pw.dos_up, linewidth=1, label="PWSCF TDOS")
    leg = plt.legend(fontsize=12, loc="upper right")
    leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0)
    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")
    plt.show()
