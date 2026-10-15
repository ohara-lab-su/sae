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
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


if __name__ == "__main__":
    name = options()
    dos = ReadVaspDoscar(name)
    out = sys.stdout
    NSPIN = dos.ispin
    LORBIT = dos.lorbit
    NATOM = dos.natom
    TITLE = dos.title
    EMAX = dos.emax
    EMIN = dos.emin
    NEDOS = dos.nedos
    EFERMI = dos.efermi
    ENG = dos.eng
    LDOS_ALL = dos.get_ldos_all()
    for spin in range(NSPIN):
        print("", file=out)
        print("", file=out)
        print("", file=out)
        print("##", file=out)
        print("## INFILE= %s" % str(name), file=out)
        print("## ISPIN = %s" % str(NSPIN), file=out)
        print("##  SPIN = %s" % str(spin + 1), file=out)
        print("## NATOM = %s" % str(NATOM), file=out)
        print("## EMAX  = %s" % str(EMAX), file=out)
        print("## EMIN  = %s" % str(EMIN), file=out)
        print("## NLINE = %s" % str(NEDOS), file=out)
        print("## FERMI = %s" % str(EFERMI), file=out)
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
            print("%13.8f %13.8f %13.8f " % (ENG[i] - EFERMI, TDOS[i], INTTDOS[i]))
        print("", file=out)
        print("", file=out)
        print("", file=out)
        for atom in range(NATOM):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("##", file=out)
            print("## INFILE= %s" % str(name), file=out)
            print("## ISPIN = %s" % str(NSPIN), file=out)
            print("##  SPIN = %s" % str(spin + 1), file=out)
            print("## NATOM = %s" % str(NATOM), file=out)
            print("## EMAX  = %s" % str(EMAX), file=out)
            print("## EMIN  = %s" % str(EMIN), file=out)
            print("## NLINE = %s" % str(NEDOS), file=out)
            print("## FERMI = %s" % str(EFERMI), file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ATOM= %s" % str(atom + 1), file=out)
            print("##      eng s p d", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)
            for i in range(NEDOS):
                print("%13.8f " % (ENG[i] - EFERMI), file=out, end="")
                for l in range(0, 3):
                    print("%13.8f " % LDOS_ALL[i, l, atom, spin], file=out, end="")
                print("")
