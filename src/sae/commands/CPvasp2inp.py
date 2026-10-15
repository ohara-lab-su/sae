#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.geometry.coordinates import CoordinateTransforms
from sae.vasp.poscar import ReadVaspPoscar

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse
import sys
import os
import re


def options():
    poscarname = "POSCAR"
    outbase = "POSCAR"
    inpsuffix = ".inp"
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option("-s", "--stdout", action="store_true")
    parser.add_option("-a", "--allinp", action="store_true")
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    options, args = parser.parse_args()
    outbase = re.sub("\\.inp$", "", outbase)
    outinp = outbase + inpsuffix
    if options.INPUT:
        poscarname = options.INPUT
    if options.OUTPUT:
        outbase = re.sub("\\.inp$", "", options.OUTPUT)
        outinp = outbase + inpsuffix
    if len(args) > 0:
        poscarname = args[0]
    if poscarname == outinp:
        sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :" + poscarname)
    return [poscarname, outbase, inpsuffix, options.stdout, options.allinp]


if __name__ == "__main__":
    RTYPE = "BAND"
    CPUTIME = "36000"
    BASIS_SET_FILE_NAME = "BASIS_SET"
    POTENTIAL_FILE_NAME = "GTH_POTENTIALS"
    WAVE_FILE_NAME = ""
    RESTART_FILE_NAME = ""
    CUTOFF = "300"
    MGRIDS = "5"
    SCF_NCYCLES = "500"
    SCF_OCYCLES = "100"
    SCF_CONV = "1E-6"
    SCF_MIN = "CG"
    FUNCTIONAL = "GGA"
    GEO_MINI = "CG"
    GEO_MAXS = "10000"
    MD_ENS = "NVT"
    MD_STEPS = "10000"
    MD_DT = "2.0"
    MD_TEMP = "300"
    OUT_FORM = "XYZ"
    OUT_UNIT = "angstrom"
    poscarname, outbase, inpsuffix, OPT_STD, OPT_INP = options()
    poscar = ReadVaspPoscar(poscarname)
    vasp = poscar.get_vasp_version()
    if vasp < 5:
        sys.exit("STOP: This script requires VASP5 style POSCAR")
    title = poscar.get_title()
    t = poscar.get_t()
    scale = poscar.get_scale()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    atoms_index_j = poscar.get_atoms_index_j()
    natom = poscar.get_natom()
    nion = poscar.get_nion()
    selective = poscar.get_selective()
    direct = poscar.get_direct()
    position = poscar.get_position()
    fix = poscar.get_fix()
    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    scale, t, natom, direct, position = CoordinateTransforms().conv_scale21(
        scale, t, natom, direct, position
    )
    if direct:
        scale, t, natom, direct, position = CoordinateTransforms().conv_direct2carABS(
            scale, t, natom, direct, position
        )
    else:
        scale, t, natom, direct, position = CoordinateTransforms().conv_car2carABS(
            scale, t, natom, direct, position
        )
    if OPT_STD:
        system = sys.stdout
    elif OPT_INP:
        try:
            system = open(outbase + inpsuffix, "w")
        except:
            system.close()
            sys.exit("STOP: " + outbase + inpsuffix + " can't open")
    if OPT_STD or OPT_INP:
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! General options", file=system)
        print("!", file=system)
        print(" @SET SYSNAME                   " + title, file=system)
        print(" @SET RTYPE                     " + RTYPE, file=system)
        print("!@SET RTYPE                     BAND", file=system)
        print("!@SET RTYPE                     ENERGY_FORCE", file=system)
        print("!@SET RTYPE                     GEO_OPT", file=system)
        print("!@SET RTYPE                     MD", file=system)
        print("!@SET CPUTIME                   " + CPUTIME, file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! Files options", file=system)
        print("!", file=system)
        print(" @SET RESTART                   FALSE", file=system)
        print(" @SET BASISFILE                 " + BASIS_SET_FILE_NAME, file=system)
        print(" @SET PSEUDOFILE                " + POTENTIAL_FILE_NAME, file=system)
        print("!@SET WAVEFILE                  " + WAVE_FILE_NAME, file=system)
        print("!@SET RESTARTFILE               " + RESTART_FILE_NAME, file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! DFT calculation options", file=system)
        print("!", file=system)
        print(" @SET CUTOFF                    " + CUTOFF, file=system)
        print(" @SET MGRIDS                    " + MGRIDS, file=system)
        print(" @SET SCF_NCYCLES               " + SCF_NCYCLES, file=system)
        print(" @SET SCF_CONV                  " + SCF_CONV, file=system)
        print(" @IF ( ${RESTART} == TRUE )", file=system)
        print("   @SET SCF_GUESS               RESTART", file=system)
        print(" @ENDIF", file=system)
        print(" @IF ( ${RESTART} == FALSE )", file=system)
        print("   @SET SCF_GUESS               ATOMIC", file=system)
        print(" @ENDIF", file=system)
        print("", file=system)
        print(" @SET SCF_MINI                  " + SCF_MIN, file=system)
        print(" @SET FUNCTIONAL                " + FUNCTIONAL, file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! Geometry optimization options", file=system)
        print("!", file=system)
        print(" @SET GEO_MIN                   " + GEO_MINI, file=system)
        print(" @SET GEO_MAXS                  " + GEO_MAXS, file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! Molecular dynamics options", file=system)
        print("!", file=system)
        print(" @SET MD_ENS                    " + MD_ENS, file=system)
        print(" @SET MD_STEPS                  " + MD_STEPS, file=system)
        print(" @SET MD_DT                     " + MD_DT, file=system)
        print(" @SET MD_TEMP                   " + MD_TEMP, file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("! Output options", file=system)
        print("!", file=system)
        print(" @SET OUT_FORM                  " + OUT_FORM, file=system)
        print("", file=system)
        print("", file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print(" &GLOBAL", file=system)
        print("   PROJECT                     ${SYSNAME}", file=system)
        print("   RUN_TYPE                    ${RTYPE}", file=system)
        print("   PRINT_LEVEL                 LOW", file=system)
        print("!  WALLTIME                    ${CPUTIME}", file=system)
        print(" &END GLOBAL", file=system)
        print("", file=system)
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print(" &FORCE_EVAL", file=system)
        print("   METHOD Quickstep", file=system)
        print("", file=system)
        print("   &PRINT", file=system)
        print("     &FORCE", file=system)
        print("     &END FORCE", file=system)
        print("   &END PRINT", file=system)
        print("", file=system)
        if not OPT_STD:
            print("   @INCLUDE 'subsys.inc'", file=system)
            print("", file=system)
    if OPT_STD:
        subsys = sys.stdout
    else:
        try:
            subsys = open("subsys.inc", "w")
        except:
            subsys.close()
            sys.exit("STOP: " + "subsys.inc" + " can't open")
    if OPT_STD:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=subsys)
    print("   &SUBSYS", file=subsys)
    print("", file=subsys)
    for ion in range(nion):
        print("     &KIND", atoms_index[ion], file=subsys)
        print("       ELEMENT ", atoms_index[ion], file=subsys)
        print("       BASIS_SET DZVP_GTH-PADE", file=subsys)
        print("       POTENTIAL GTH-PADE-q4", file=subsys)
        print("     &END KIND", file=subsys)
        print("", file=subsys)
    print("     &CELL", file=subsys)
    print("       A %13.9f %13.9f %13.9f" % (t[0, 0], t[1, 0], t[2, 0]), file=subsys)
    print("       B %13.9f %13.9f %13.9f" % (t[0, 1], t[1, 1], t[2, 1]), file=subsys)
    print("       C %13.9f %13.9f %13.9f" % (t[0, 2], t[1, 2], t[2, 2]), file=subsys)
    print("       PERIODIC XYZ", file=subsys)
    print("     &END CELL", file=subsys)
    print("", file=subsys)
    print("     &COORD", file=subsys)
    for i in range(natom):
        atom = re.sub("_.*", "", atoms_index_j[i])
        atoms_index_j[i] = atom
        print(
            "       %2s %12.8f %12.8f %12.8f "
            % (atoms_index_j[i], position[i][0], position[i][1], position[i][2]),
            file=subsys,
        )
    print("     &END COORD", file=subsys)
    print("", file=subsys)
    print("   &END SUBSYS", file=subsys)
    print("", file=subsys)
    if not OPT_STD:
        subsys.close()
    if OPT_INP or OPT_STD:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!", file=system)
        print("   &DFT", file=system)
        print("      BASIS_SET_FILE_NAME           ${BASISFILE}", file=system)
        print("      POTENTIAL_FILE_NAME           ${PSEDOFILE}", file=system)
        print("", file=system)
        print("      @IF ( ${RESTART} == TRUE )", file=system)
        print("          WFN_RESTART_FILE_NAME     ${WAVEFILE}", file=system)
        print("      @ENDIF", file=system)
        print("", file=system)
        print("      &QS", file=system)
        print("        EPS_DEFAULT                 1.0E-10", file=system)
        print("      &END QS", file=system)
        print("", file=system)
        print("      &MGRID", file=system)
        print("        MGRIDS                      ${MGRIDS}", file=system)
        print("        CUTOFF                      ${CUTOFF}", file=system)
        print("        REL_CUTOFF 60", file=system)
        print("      &END MGRID", file=system)
        print("", file=system)
        print("     &XC", file=system)
        print("       &XC_FUNCTIONAL PADE", file=system)
        print("       &END XC_FUNCTIONAL", file=system)
        print("     &END XC", file=system)
        print("", file=system)
        print("     &SCF", file=system)
        print("       SCF_GUESS ATOMIC", file=system)
        print("       EPS_SCF 1.0E-7", file=system)
        print("       MAX_SCF 300", file=system)
        print("       &DIAGONALIZATION ON", file=system)
        print("         ALGORITHM STANDARD", file=system)
        print("       &END DIAGONALIZATION", file=system)
        print("       &MIXING T", file=system)
        print("         METHOD BROYDEN_MIXING", file=system)
        print("         ALPHA 0.4", file=system)
        print("         NBROYDEN 8", file=system)
        print("     &END SCF", file=system)
        print("", file=system)
        print("   &END DFT", file=system)
        print("", file=system)
        print("   &PRINT", file=system)
        print("     &FORCES ON", file=system)
        print("     &END FORCES", file=system)
        print("   &END PRINT", file=system)
        print("", file=system)
        print("&END FORCE_EVAL", file=system)
    if not OPT_STD and OPT_INP:
        system.close()
