#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.pwscf.out import ReadPwOut
from sae.pwscf.pdos import ReadPwPdos

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import matplotlib.pyplot as plt


def options():
    prefix = "input"
    outname = None
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-p", "--prefix")
    parser.add_option("-o", "--outscf", dest="SCF")
    options, args = parser.parse_args()
    if options.INPUT:
        prefix = options.INPUT
    if options.prefix:
        prefix = options.prefix
    if options.SCF:
        outname = options.SCF
    return (prefix, outname)


if __name__ == "__main__":
    prefix, outname = options()
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
    pw = ReadPwPdos(prefix)
    if outname is None:
        pw.pdos = pw.get_ldos(l=0, atom=0, spin=0)
        plt.plot(pw.eng, pw.pdos, linewidth=1, label="s")
        pw.pdos = pw.get_ldos(l=2, atom=0, spin=0)
        plt.plot(pw.eng, pw.pdos, linewidth=1, label="d")
    else:
        pw.pdos = pw.get_ldos(l=0, atom=0, spin=0)
        plt.plot(pw.eng - out.efermi, pw.pdos, linewidth=1, label="s")
        pw.pdos = pw.get_ldos(l=2, atom=0, spin=0)
        plt.plot(pw.eng - out.efermi, pw.pdos, linewidth=1, label="d")
    leg = plt.legend(fontsize=12, loc="upper right")
    leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0)
    plt.savefig("TDOS.eps")
    plt.savefig("TDOS.pdf")
    plt.savefig("TDOS.png")
    plt.show()
