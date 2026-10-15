#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.doscar import ReadVaspDoscar
from sae.vasp.outcar import ReadVaspOutcar

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
    parser.add_option("-i", "--input", dest="INPUT", default=name)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]
    return name


if __name__ == "__main__":
    name = options()
    oname = "OUTCAR"
    out = sys.stdout
    dos = ReadVaspDoscar(name)
    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE = dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()
    ENG = dos.get_eng()
    outcar = ReadVaspOutcar(oname)
    NION = outcar.get_nion()
    ADOS_ALL = dos.get_ldos_ion_all()
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
        print("##")
        print("##")
        print("##        total")
        print("##        eng tdos tidos")
        print("##")
        print("")
        print("")
        print("")
        TDOS = dos.get_tdos(spin)
        INTTDOS = dos.get_inttdos(spin)
        for i in range(NEDOS):
            print("%13.8f %13.8f %13.8f " % (ENG[i] - EFERMI, TDOS[i], INTTDOS[i]))
        print("", file=out)
        print("", file=out)
        print("", file=out)
        for ion in range(NION):
            print("", file=out)
            print("", file=out)
            print("", file=out)
            print("##", file=out)
            print("## INFILE= %s" % str(name), file=out)
            print("## ISPIN = %s" % str(NSPIN), file=out)
            print("##  SPIN = %s" % str(spin + 1), file=out)
            print("##  NION = %s" % str(NION), file=out)
            print("## EMAX  = %s" % str(EMAX), file=out)
            print("## EMIN  = %s" % str(EMIN), file=out)
            print("## NLINE = %s" % str(NEDOS), file=out)
            print("## FERMI = %s" % str(EFERMI), file=out)
            print("##", file=out)
            print("##", file=out)
            print("##      ION= %s" % (ion + 1), file=out)
            print("##      eng s p d", file=out)
            print("##", file=out)
            print("", file=out)
            print("", file=out)
            print("", file=out)
            for i in range(NEDOS):
                print("%13.8f " % (ENG[i] - EFERMI), file=out, end="")
                for l in range(0, 3):
                    print("%13.8f " % ADOS_ALL[i, l, ion, spin], file=out, end="")
                print("", file=out)
