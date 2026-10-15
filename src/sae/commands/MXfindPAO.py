#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re

try:
    import dircache
except:
    import glob

    pass
import optparse


def options():
    defaultatom = "C"
    defaultpot = "PBE"
    defaultver = "13"
    defaultcut = "5.0"
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom", dest="ATOM", default=defaultatom)
    parser.add_option("-p", "--potential", dest="POT", default=defaultpot)
    parser.add_option("-v", "--version", dest="VER", default=defaultver)
    parser.add_option("-c", "--cut", dest="CUT", default=defaultcut)
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
    filename = options.ATOM + options.CUT
    if len(args) > 0:
        filename = args[0]
    return [DFT_DATAPATH, options.ATOM, options.POT, options.VER, options.CUT, filename]


if __name__ == "__main__":
    opts = options()
    data, atom, pot, ver, cut, name = opts
    fullname = data + "/PAO/" + name + ".pao"
    SUFFIX = ""
    if not os.path.exists(fullname):
        SUFFIX = "S"
        fullname = data + "/PAO/" + name + SUFFIX + ".pao"
        if not os.path.exists(fullname):
            SUFFIX = "H"
            fullname = data + "/PAO/" + name + SUFFIX + ".pao"
            if not os.path.exists(fullname):
                SUFFIX = "dir"
                paolist = []
                pao_txt = atom + "[0-9].*" + "\\.pao"
                pao_reg = re.compile(pao_txt)
                try:
                    for file in dircache.listdir(data + "/PAO/"):
                        if pao_reg.search(file):
                            paolist.append(file)
                except:
                    for file in glob.glob(data + "/PAO/*"):
                        if pao_reg.search(file):
                            paolist.append(file)
    if SUFFIX != "dir":
        print("CUT  :", cut)
        print("PATH :", fullname)
        print("PAO  :", name)
    else:
        for i in range(len(paolist)):
            print(paolist[i])
