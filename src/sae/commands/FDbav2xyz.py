#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.bav import ReadFdmBav

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


def options():
    from sae.common.paths import FileDiscovery

    name = "Cu"
    suffix = "_bav.txt"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-s", "--std", action="store_true")
    options, args = parser.parse_args()
    if not os.path.exists(name + suffix):
        name0 = FileDiscovery().find_datfile1(suffix)
        name = name0.replace(suffix, "")
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return (name, suffix, options.std)


if __name__ == "__main__":
    name, suffix, STD_FLAG = options()
    bav = ReadFdmBav(name, suffix)
    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()
    if STD_FLAG:
        xyz = sys.stdout
    else:
        try:
            xyz = open(name + ".xyz", "w")
        except:
            xyz.close()
    print(natom, file=xyz)
    print("", file=xyz)
    for i in range(natom):
        print(
            " %s %14.10f %14.10f %14.10f"
            % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2]),
            file=xyz,
        )
    xyz.close()
