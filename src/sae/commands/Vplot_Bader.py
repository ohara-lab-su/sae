#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.acf import ReadVaspAcf
from sae.vasp.poscar import ReadVaspPoscar
from sae.vasp.potcar import ReadVaspPotcar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import sae as SAEG
import wx
import os
import optparse


def options():
    inpname = "POSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-b", "--bond", action="store_true", default=False)
    parser.add_option("-l", "--log", action="store_true", default=False)
    parser.add_option("-c", "--charge", action="store_true", default=False)
    parser.add_option("-n", "--noncell", action="store_true", default=False)
    parser.add_option("--cmax")
    parser.add_option("--cmin")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    if not os.path.exists(inpname):
        inpname0 = "CONTCAR"
        if not os.path.exists(inpname0):
            sys.exit("STOP: " + inpname + " and " + inpname0 + " file not found")
        else:
            inpname = inpname0
    if len(args) < 3:
        super_x = 1
        super_y = 1
        super_z = 1
    else:
        super_x = int(args[0])
        super_y = int(args[1])
        super_z = int(args[2])
        print(
            "Super Cell         : [%s, %s, %s]"
            % (str(super_x), str(super_y), str(super_z))
        )
    return (
        inpname,
        options.bond,
        options.log,
        options.charge,
        options.noncell,
        options.cmax,
        options.cmin,
        super_x,
        super_y,
        super_z,
    )


if __name__ == "__main__":
    (
        readfile,
        OPT_BOND,
        OPT_LOG,
        OPT_CHARGE,
        OPT_CELL,
        CMAX,
        CMIN,
        super_x,
        super_y,
        super_z,
    ) = options()
    app = wx.PySimpleApp()
    print("INPUT file name    : %s" % str(readfile))
    print("plot BOND Mode     : %s" % str(OPT_BOND))
    print("plot without cell  : %s" % str(OPT_CELL))
    if OPT_CHARGE:
        print("plot charge        : charge")
    else:
        print("plot charge        : ABS(charge)")
    if CMAX:
        print("charge MAX         : %s" % str(CMAX))
    if CMIN:
        print("charge MIN         : %s" % str(CMIN))
    print("-----------------------------------")
    poscar = ReadVaspPoscar(readfile)
    potcar = ReadVaspPotcar()
    acf = ReadVaspAcf(poscar=poscar, potcar=potcar)
    crystal = SAEG.CrystalMaker(
        poscar, origin=[-0.5, -0.5, 0], times=[super_x, super_y, super_z]
    )
    crystal.plot_atoms()
    if OPT_CHARGE:
        crystal.plot_bader(acf, mode="CHARGE", cmax=CMAX, cmin=CMIN)
    if not OPT_CHARGE:
        crystal.plot_bader(acf, cmax=CMAX, cmin=CMIN)
    if OPT_BOND:
        crystal.plot_bonds()
    if not OPT_CELL:
        crystal.plot_unit_cell()
