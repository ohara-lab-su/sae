#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.vps import ReadMxVps

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


def options():
    defaultatom = "C"
    defaultpot = "PBE"
    defaultver = "13"
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom", dest="ATOM", default=defaultatom)
    parser.add_option("-p", "--potential", dest="POT", default=defaultpot)
    parser.add_option("-v", "--version", dest="VER", default=defaultver)
    options, args = parser.parse_args()
    DFT_DATA_BASE = "DFT_DATA"
    DFT_DATA = DFT_DATA_BASE + options.VER
    DFT_DATAPATH = "../" + DFT_DATA
    HOMEPATH = os.environ.get("HOME", "")
    DATAPATH = os.environ.get("OPENMXDATAPATH", "")
    if not os.path.exists(DFT_DATAPATH):
        if os.path.exists("./" + DFT_DATA):
            DFT_DATAPATH = "./" + DFT_DATA
        elif DATAPATH:
            DFT_DATAPATH = DATAPATH
        elif os.path.exists(HOMEPATH + "/" + DFT_DATA):
            DFT_DATAPATH = HOMEPATH + "/" + DFT_DATA
        elif os.path.exists("../" + DFT_DATAPATH):
            DFT_DATAPATH = "../" + DFT_DATAPATH
        else:
            sys.exit("STOP: " + DFT_DATA + " directory not found")
    filename = options.ATOM + "_" + options.POT + options.VER
    if len(args) > 0:
        filename = args[0]
    return [DFT_DATAPATH, options.ATOM, options.POT, options.VER, filename]


if __name__ == "__main__":
    opts = options()
    data, atom, pot, ver, name = opts
    fullname = data + "/VPS/" + name + ".vps"
    if not os.path.exists(fullname):
        SUFFIX = "S"
        name = name + SUFFIX
        fullname = data + "/VPS/" + name + ".vps"
        if not os.path.exists(fullname):
            SUFFIX = "H"
            name = name + SUFFIX
            fullname = data + "/VPS/" + name + ".vps"
    vps = ReadMxVps(fullname)
    electron = vps.get_valence_electron()
    print("DATAPATH        :", data)
    print("VER             :", ver)
    print("POT             :", pot)
    print("ATOM            :", atom)
    print("VPS             :", name)
    print("PATH            :", fullname)
    print("num of electron :", electron)
