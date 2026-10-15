#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014-2015, Kengo NAKADA"
__license__ = "MIT"
import os


def options():
    from sae.common.paths import FileDiscovery
    import optparse

    name = "openmx"
    suffix = ".dat"
    mxname = name + suffix
    poscarname = "openmx"
    xyzname = "openmx.xyz"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option(
        "-d", "--direct", action="store_true", default=False, dest="DIRECT"
    )
    parser.add_option("-s", "--std", action="store_true", default=False, dest="STDOUT")
    options, args = parser.parse_args()
    if not os.path.exists(mxname):
        name0 = FileDiscovery().find_datfile("dat")
        if not name0 is None:
            name = name0
            mxname = name + suffix
            poscarname = mxname
            xyzname = mxname + ".xyz"
    if options.INPUT:
        mxname = options.INPUT
        poscarname = mxname
        xyzname = mxname + ".xyz"
    if options.OUTPUT:
        poscarname = options.OUTPUT
    return [mxname, poscarname, xyzname, options.STDOUT, options.DIRECT]


if __name__ == "__main__":
    mxname, poscarname, xyzname, STD, DIRECT = options()
    print("INPUT", mxname)
    print("OUTPUT", poscarname + ".vasp")
    cell = Read(filename=mxname, code="OpenMX")
    cell.write(outname=poscarname, code="VASP", STD=STD)
