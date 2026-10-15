#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.text import TextFiles

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np
import matplotlib.pyplot as plt


def options():
    IN = "igzo"
    IN_FIT = IN + ".fit"
    IN_CALC = IN + ".calcdat"
    return [IN, IN_FIT, IN_CALC]


if __name__ == "__main__":
    IN, IN_FIT, IN_CALC = options()
    sfit = 12
    scalc = 13
    nfit0 = sum((1 for line in open(IN_FIT)))
    fitdat = np.zeros((nfit0, 5))
    nfit = TextFiles().read_dat5(IN_FIT, fitdat, sfit)
    ncalc0 = sum((1 for line in open(IN_CALC)))
    calcdat = np.zeros((ncalc0, 2))
    ncalc = TextFiles().read_dat2(IN_CALC, calcdat, scalc)
    x0 = np.zeros(ncalc)
    y0 = np.zeros(ncalc)
    for i in range(ncalc):
        x0[i] = calcdat[scalc + i, 0]
        y0[i] = calcdat[scalc + i, 1]
    cal_y = np.zeros(nfit)
    for i in range(nfit):
        cal_y[i] = fitdat[sfit + i, 1]
    exp_y = np.zeros(nfit)
    for i in range(nfit):
        exp_y[i] = fitdat[sfit + i, 3]
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 18
    plt.rcParams["axes.linewidth"] = 1.5
    plt.axes([0.105, 0.125, 0.85, 0.8])
    plt.plot(x0, cal_y, color="red", linewidth=2, label="cal S(Q)")
    plt.plot(x0, exp_y, color="green", linewidth=2, label="obs S(Q)")
    plt.plot(x0, y0, color="blue", linewidth=2, label="initial cal S(Q)")
    import matplotlib

    tmp = matplotlib.__version__
    version = tmp.split(".")
    if int(version[0]) > 0:
        plt.xlabel("Q/$\\AA^{-1}$", fontsize=20, fontname="Times New Roman")
    else:
        plt.xlabel("Q/A^-1", fontsize=20, fontname="Times New Roman")
    plt.ylabel("S(Q)", fontsize=20, fontname="Times New Roman")
    plt.legend()
    plt.savefig(IN + "_fit.eps")
    plt.savefig(IN + "_fit.pdf")
    plt.close("all")
