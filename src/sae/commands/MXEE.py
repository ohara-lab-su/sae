#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery
from sae.openmx.dat import ReadMxDat

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

if __name__ == "__main__":
    name = "openmx"
    suffix = ".out"
    mxname = name + suffix
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(mxname):
        try:
            name0 = FileDiscovery().find_datfile("dat")
            if not name0 == None:
                name = name0
                mxname = name + suffix
        except:
            pass
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub("\\.out$", "", mxname)
        mxname = name + suffix
    if len(args) > 0:
        name = args[0]
        name = re.sub("\\.out$", "", name)
    mxname = name + suffix
    if not os.path.exists(name + ".out"):
        if os.path.exists(name + ".dat"):
            dat = ReadMxDat(name + ".dat")
            sysname = dat.get_title()
            name = sysname
            mxname = name + suffix
        else:
            sys.exit("STOP: " + name + ".out and " + name + ".dat file not found.")
    module_name = "sae._class_registry"
    if not os.path.exists(mxname):
        mxname = name + ".DFTSCF"
        class_name = "ReadMxDftscf"
    else:
        class_name = "ReadMxOut"
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    out = klass(mxname)
    n_ion_loop = out.get_n_ion_loop()
    utot = out.get_utot()
    for md in range(n_ion_loop):
        print(" %14.11f" % utot[md])
