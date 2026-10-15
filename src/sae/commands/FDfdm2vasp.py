#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014,2015 Kengo NAKADA"
__license__ = "MIT"
if __name__ == "__main__":
    import optparse

    name = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    print("INPUT :", name)
    print("OUTPUT:", name + ".vasp")
    cell = Read(filename=name, code="FDMNES")
    cell.write(code="VASP", outname=name, STD=True)
    cell.write(code="VASP", outname=name)
