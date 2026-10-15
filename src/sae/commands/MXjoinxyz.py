#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.text import TextFiles

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


def options(suffix, sumfile):
    from sae.common.paths import FileDiscovery

    xyznames = FileDiscovery().find_datfiles(suffix)
    if os.path.exists(sumfile):
        xyznames.remove(re.sub(".xyz", "", sumfile))
    parser = optparse.OptionParser()
    parser.add_option("-s", "--std", action="store_true", default=False)
    options, args = parser.parse_args()
    if len(args) > 0:
        xyznames = []
        for i in range(0, len(args)):
            xyznames.append(re.sub(".xyz$", "", args[i]))
    FLAG_STD = options.std
    return [xyznames, FLAG_STD]


if __name__ == "__main__":
    suffix = "xyz"
    sumfile = "sum" + "." + suffix
    xyznames, FLAG_STD = options(suffix, sumfile)
    if not FLAG_STD:
        print("OUTPUT   =", sumfile)
        print("SUMFILES =")
        for xyz in xyznames:
            print("          ")
            print(xyz + "." + suffix)
    sumnum = 0
    sumdat = []
    for name in xyznames:
        datlines, num = TextFiles().read_dataline(name + "." + suffix)
        sumnum = sumnum + int(datlines[0])
        for j in range(num - 2):
            sumdat.append(datlines[j + 2])
    if not FLAG_STD:
        try:
            dat = open(sumfile, "w")
        except:
            sys.exit("STOP: " + sumfile + " can't open")
    else:
        dat = sys.stdout
    print(sumnum, file=dat)
    print("", file=dat)
    for i in range(sumnum):
        print(sumdat[i], file=dat)
    dat.close()
