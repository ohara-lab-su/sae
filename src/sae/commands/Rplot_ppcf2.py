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
    IN_PSQ = IN + ".psq"
    IN_FIT = IN + ".fit"
    IN_CALC = IN + ".calcdat"
    IN_PPCF = IN + ".ppcf"
    return [IN, IN_PSQ, IN_FIT, IN_CALC, IN_PPCF]


if __name__ == "__main__":
    IN, IN_PSQ, IN_FIT, IN_CALC, IN_PPCF = options()
    dimm = 11
    spsq = 5
    sfit = 12
    scalc = 13
    sppcf = 8
    nppcf0 = sum((1 for line in open(IN_PPCF)))
    ppcfdat = np.zeros((nppcf0, dimm))
    nppcf = TextFiles().read_dat(IN_PPCF, dimm, ppcfdat, sppcf)
    npsq0 = sum((1 for line in open(IN_PSQ)))
    psqdat = np.zeros((npsq0, dimm))
    npsq = TextFiles().read_dat(IN_PSQ, dimm, psqdat, spsq)
    nfit0 = sum((1 for line in open(IN_FIT)))
    fitdat = np.zeros((nfit0, 5))
    nfit = TextFiles().read_dat5(IN_FIT, fitdat, sfit)
    ncalc0 = sum((1 for line in open(IN_CALC)))
    calcdat = np.zeros((ncalc0, 2))
    ncalc = TextFiles().read_dat2(IN_CALC, calcdat, scalc)
    maxq = psqdat[npsq0 - 1, 0]
    init_y = np.zeros(ncalc)
    for i in range(ncalc):
        init_y[i] = calcdat[scalc + i, 1]
    cal_y = np.zeros(nfit)
    exp_y = np.zeros(nfit)
    for i in range(nfit):
        cal_y[i] = fitdat[sfit + i, 1]
        exp_y[i] = fitdat[sfit + i, 3]
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 20
    plt.rcParams["legend.fontsize"] = 11
    plt.rcParams["axes.linewidth"] = 1.5
    psq_x = np.zeros(nppcf)
    for i in range(nppcf):
        psq_x[i] = ppcfdat[sppcf + i, 0]
    plt.axes([0.105, 0.5575, 0.85, 0.4])
    for d in range(1, dimm / 2 + 1):
        psq_y = np.zeros(nppcf)
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.xticks([])
    plt.legend()
    plt.ylabel("partial g(r)", fontsize=20, fontname="Times New Roman")
    plt.axes([0.105, 0.125, 0.85, 0.4])
    for d in range(dimm / 2 + 1, dimm):
        psq_y = np.zeros(nppcf)
        for i in range(nppcf):
            psq_y[i] = ppcfdat[sppcf + i, d]
        plt.plot(psq_x, psq_y, linewidth=1, label=str(d))
    plt.legend()
    plt.ylabel("partial g(r)", fontsize=20, fontname="Times New Roman")
    import matplotlib

    tmp = matplotlib.__version__
    version = tmp.split(".")
    if int(version[0]) > 0:
        plt.xlabel("r[$\\AA$]", fontsize=20, fontname="Times New Roman")
    else:
        plt.xlabel("r[A]", fontsize=20, fontname="Times New Roman")
    plt.savefig(IN + "_ppcf2.eps")
    plt.savefig(IN + "_ppcf2.pdf")
    plt.close("all")
