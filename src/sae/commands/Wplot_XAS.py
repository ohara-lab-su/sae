#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.wien2k.output0 import ReadWienOutput0
from sae.wien2k.spectra_plot import SpectraPlot

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


def options():
    name = re.sub(".*/", "", os.getcwd())
    parser = optparse.OptionParser(os.getcwd())
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--emax", dest="EMAX")
    parser.add_option("--emin", dest="EMIN")
    parser.add_option("--ymax", dest="YMAX")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    return [name, options.EMAX, options.EMIN, options.YMAX]


if __name__ == "__main__":
    case, EMAX, EMIN, YMAX = options()
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
    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True
    FLAG_SHOW = True
    dos_suffix = ".dos1ev"
    txspec_suffix = ".txspec"
    xspec_suffix = ".xspec"
    outname = "XAS"
    if not FLAG_SPIN:
        SpectraPlot().plot_xas(
            case=case,
            dos_suffix=dos_suffix,
            txspec_suffix=txspec_suffix,
            xspec_suffix=xspec_suffix,
            outname=outname,
            OPT_EMAX=EMAX,
            OPT_EMIN=EMIN,
            OPT_YMAX=YMAX,
            FLAG_SHOW=FLAG_SHOW,
        )
    else:
        for i in ["up", "dn"]:
            print("=== " + str(i))
            FLAG_SHOW = False
            SpectraPlot().plot_xas(
                case=case,
                dos_suffix=dos_suffix + str(i),
                txspec_suffix=txspec_suffix + str(i),
                xspec_suffix=xspec_suffix + str(i),
                outname=outname + str(i),
                OPT_EMAX=EMAX,
                OPT_EMIN=EMIN,
                OPT_YMAX=YMAX,
                FLAG_SHOW=FLAG_SHOW,
            )
        print("=== up+dn")
        FLAG_SHOW = True
        outname = "XAS"
        SpectraPlot().plot_sum_xas(
            case=case,
            dos_suffix=dos_suffix,
            outname=outname,
            OPT_EMAX=EMAX,
            OPT_EMIN=EMIN,
            OPT_YMAX=YMAX,
            FLAG_SHOW=FLAG_SHOW,
        )
