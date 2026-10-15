#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import argparse
import matplotlib.pyplot as plt


def options():
    parser = argparse.ArgumentParser()
    parser.add_argument("--emax")
    parser.add_argument("--emin")
    options = parser.parse_args()
    return (options.emax, options.emin)


if __name__ == "__main__":
    OPT_EMAX, OPT_EMIN = options()
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax     =", OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin     =", OPT_EMIN)
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    fig = plt.figure(figsize=(7.0, 9.89))
    f0 = fig.add_subplot(311)
    f1 = fig.add_subplot(312, sharex=f0)
    f2 = fig.add_subplot(313, sharex=f0)
    txt = ReadFdmTxt("BaTiO3_R3m")
    sd_sd0 = ReadFdmSd("BaTiO3_R3m", suffix="_sd0.txt", inpname="read_pdb.inp")
    ef = txt.E_edge + txt.E_fermi
    dos_s_sd0 = sd_sd0.get_ldos(l="s")
    dos_p_sd0 = sd_sd0.get_ldos(l="p")
    f0.plot(
        sd_sd0.eng + txt.E_edge, dos_p_sd0, color="red", linewidth=1, label="sd0, Ba-p"
    )
    f0.axvline(x=ef, color="black", linewidth=1)
    f0.set_ylabel("LDOS [stat/eV]")
    l0 = f0.legend(loc="upper right")
    l0.get_frame().set_alpha(0.5)
    f0.ticklabel_format(axis="x", useOffset=False)
    sd_sd1 = ReadFdmSd("BaTiO3_R3m", suffix="_sd1.txt", inpname="read_pdb.inp")
    dos_s_sd1 = sd_sd1.get_ldos(l="s")
    dos_p_sd1 = sd_sd1.get_ldos(l="p")
    f1.plot(
        sd_sd1.eng + txt.E_edge, dos_p_sd1, color="red", linewidth=1, label="sd1, Ba-p"
    )
    f1.axvline(x=ef, color="black", linewidth=1)
    f1.set_ylabel("LDOS [stat/eV]")
    l1 = f1.legend(loc="upper right")
    l1.get_frame().set_alpha(0.5)
    f1.ticklabel_format(axis="x", useOffset=False)
    sd_sd2 = ReadFdmSd("BaTiO3_R3m", suffix="_sd2.txt", inpname="read_pdb.inp")
    dos_s_sd2 = sd_sd2.get_ldos(l="s")
    dos_p_sd2 = sd_sd2.get_ldos(l="p")
    f2.plot(
        sd_sd2.eng + txt.E_edge, dos_p_sd2, color="red", linewidth=1, label="sd2, Ti-p"
    )
    f2.axvline(x=ef, color="black", linewidth=1)
    f2.set_ylabel("LDOS [stat/eV]")
    l2 = f2.legend(loc="upper right")
    l2.get_frame().set_alpha(0.5)
    f2.ticklabel_format(axis="x", useOffset=False)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    plt.savefig("LDOSmulti.eps")
    plt.savefig("LDOSmulti.pdf")
    plt.savefig("LDOSmulti.png")
    plt.show()
    plt.close("all")
