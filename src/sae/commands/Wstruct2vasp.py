#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import re
import os
import optparse
from ase.io import read, write
from ase.io.vasp import *
from ase.io.xyz import *


def options():
    from sae.common.paths import FileDiscovery

    base = re.sub(".*/", "", os.getcwd())
    suffix = ".struct"
    out_suffix = ".vasp"
    name = base + suffix
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if not os.path.exists(name):
        base = FileDiscovery().find_datfile(suffix)
        if not base is None:
            name = base + suffix
    if options.INPUT:
        name = options.INPUT
        base = re.sub(suffix, "", name)
    if len(args) > 0:
        name = args[0]
        base = re.sub(suffix, "", name)
    if not os.path.exists(name):
        sys.exit("STOP: " + name + " file not found")
    return (name, base, suffix, out_suffix)


if __name__ == "__main__":
    structname, structbase, wiensuffix, out_suffix = options()
    poscarname = structname + out_suffix
    print("INPUT STRUCT file  = ", structname)
    print("OUTPUT POSCAR file = ", poscarname)
    atoms = read(structname, format="struct")
    atoms.write(poscarname, format="vasp", direct=True, vasp5=True)
