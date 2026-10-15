#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse


def options():
    name = "DOSCAR"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("--fermi", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return (name, options.fermi)


if __name__ == "__main__":
    name, FERMI_FLAG = options()
    dos = ReadVaspDoscar(name)
    out = sys.stdout
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    ENG = dos.get_eng()
    print("", file=out)
    print("", file=out)
    print("", file=out)
    if FERMI_FLAG:
        EFERMI = 0.0
        print("## EF = 0", file=out)
    else:
        EFERMI = dos.get_efermi()
        print("## EF = ", EFERMI, file=out)
    print("## Energy = E - EF", file=out)
    for spin in range(NSPIN):
        print("##", file=out)
        print("## INFILE= ", name, file=out)
        print("## ISPIN = ", NSPIN, file=out)
        print("##  SPIN = ", spin + 1, file=out)
        print("## NATOM = ", NATOM, file=out)
        print("## EMAX  = ", EMAX, file=out)
        print("## EMIN  = ", EMIN, file=out)
        print("## NLINE = ", NEDOS, file=out)
        print("## FERMI = ", EFERMI, file=out)
        print("##", file=out)
        print("##", file=out)
        print("##        total", file=out)
        print("##        eng tdos tidos", file=out)
        print("##", file=out)
        print("", file=out)
        print("", file=out)
        print("", file=out)
        TDOS = dos.get_tdos(spin)
        INTTDOS = dos.get_inttdos(spin)
        for i in range(NEDOS):
            print(
                "%13.8f %13.8f %13.8f " % (ENG[i] - EFERMI, TDOS[i], INTTDOS[i]),
                file=out,
            )
        print("", file=out)
        print("", file=out)
        print("", file=out)
