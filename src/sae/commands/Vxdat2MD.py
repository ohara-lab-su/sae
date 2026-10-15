#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.xdatcar import ReadVaspXdat

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse


def options():
    XDATCAR = "XDATCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=XDATCAR)
    options, args = parser.parse_args()
    if options.INPUT:
        XDATCAR = options.INPUT
    if len(args) > 0:
        XDATCAR = args[0]
    return XDATCAR


if __name__ == "__main__":
    name = options()
    xdat = ReadVaspXdat(name)
    nion = xdat.get_nion()
    natom = xdat.get_natom()
    vasp = xdat.get_vasp_version()
    title = xdat.get_title()
    scale = xdat.get_scale()
    t = xdat.get_t()
    atoms = xdat.get_atoms()
    atoms_index = xdat.get_atoms_index()
    direct = xdat.get_direct()
    nloop = xdat.get_nloop()
    for i in range(nloop):
        print(natom)
        print("%s %10d" % ("   step=", i + 1))
        xyz = xdat.get_xyz(loop=i)
        j = 0
        for k in range(nion):
            for l in range(int(atoms[k])):
                print(
                    "  %2s %12.8f %12.8f %12.8f"
                    % (atoms_index[k], xyz[j, 0], xyz[j, 1], xyz[j, 2])
                )
                j += 1
