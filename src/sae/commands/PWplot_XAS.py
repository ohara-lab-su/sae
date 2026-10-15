#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.pwscf.xanes import ReadPwXanes

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import matplotlib.pyplot as plt


def options():
    name = "xanes.dat"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if options.EMAX:
        options.EMAX = float(options.EMAX)
    if options.EMIN:
        options.EMIN = float(options.EMIN)
    if options.YMAX:
        options.YMAX = float(options.YMAX)
    if len(args) > 0:
        name = args[0]
    return (name, options.EMAX, options.EMIN, options.YMAX)


if __name__ == "__main__":
    name, OPT_EMAX, OPT_EMIN, OPT_YMAX = options()
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
    E_edge = 0.0
    timesP = 1.0
    pw = ReadPwXanes("xanes.dat")
    plt.plot(pw.eng + E_edge, pw.xas * timesP, linewidth=1, label="PWSCF fch")
    plt.axvline(x=0, color="black", linewidth=1)
    plt.xlabel("Energy above Fermi [eV]")
    plt.ylabel("Absorption [arb. unit]")
    leg = plt.legend(fontsize=12, loc="lower right")
    leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")
    plt.show()
