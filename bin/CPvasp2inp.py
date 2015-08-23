#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#   convert VASP POSCAR to CP2K *.inp
#
################################################################################
#
# 2015.03.12
#  startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import optparse
import sys
import os
import re
#import numpy as np

#import glob
import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
def options():

    poscarname = 'POSCAR'
    outbase    = 'POSCAR'
    inpsuffix  = '.inp'

    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()

    parser.add_option(  '-s','--stdout',
                       action='store_true',
    )
    parser.add_option(  '-a','--allinp',
                       action='store_true',
    )
    parser.add_option( '-i','--input',
                       dest='INPUT',
    )
    parser.add_option( '-o','--output',
                       dest='OUTPUT',
    )
    options, args = parser.parse_args()

    outbase=re.sub('\.inp$','',outbase)
    outinp=outbase+inpsuffix

    if options.INPUT:
        poscarname=options.INPUT

    if options.OUTPUT:
        outbase=re.sub('\.inp$','',options.OUTPUT)
        outinp=outbase+inpsuffix

    # オプション無し引数の時は拡張子自動削除を付けずにそのままファイル名とする
    if len(args) >0:
        poscarname=args[0]

    if poscarname == outinp:
        sys.exit("STOP: INPUT_NAME = OUTPUT_NAME :"+poscarname)

    return [poscarname,outbase,inpsuffix,options.stdout,options.allinp]

################################################################################
if __name__ == '__main__':

    ############################################################################
    # set default

#   RTYPE="MD"
    RTYPE="BAND"
    CPUTIME="36000"

    BASIS_SET_FILE_NAME="BASIS_SET"
    POTENTIAL_FILE_NAME="GTH_POTENTIALS"
    WAVE_FILE_NAME=""
    RESTART_FILE_NAME=""

    CUTOFF="300"
    MGRIDS="5"
    SCF_NCYCLES="500"
    SCF_OCYCLES="100"
    SCF_CONV="1E-6"

    SCF_MIN="CG"
#   FUNCTIONAL="BLYP"
    FUNCTIONAL="GGA"

    GEO_MINI="CG"
    GEO_MAXS="10000"

    MD_ENS="NVT"
    MD_STEPS="10000"
    MD_DT="2.0"
    MD_TEMP="300"

    OUT_FORM="XYZ"
    OUT_UNIT="angstrom"
    ############################################################################


    poscarname,outbase,inpsuffix,OPT_STD,OPT_INP = options()

    ## POSCAR 読み込み
    poscar = SAE.ReadVaspPoscar(poscarname)

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


    # scale factor を1に変更(内部座標もスケール)
    scale,t,natom,direct,position = \
            SAE.conv_scale21(scale,t,natom,direct,position)

    # 内部座標をスケール
    if direct:
        scale,t,natom,direct,position = \
                SAE.conv_direct2carABS(scale,t,natom,direct,position)
    else:
        scale,t,natom,direct,position = \
                SAE.conv_car2carABS(scale,t,natom,direct,position)


    ############################################################################
    # output system.inp
    if OPT_STD:
        system = sys.stdout
    elif OPT_INP:
        try:
            system = open(outbase+inpsuffix,'w')
        except:
            system.close()
            sys.exit("STOP: "+outbase+inpsuffix+" can't open")

    if OPT_STD or OPT_INP:
        #########################################################################
        # set
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! General options"
        print >> system, "!"
        print >> system, " @SET SYSNAME                   "+title
        print >> system, " @SET RTYPE                     "+RTYPE
        print >> system, "!@SET RTYPE                     BAND"
        print >> system, "!@SET RTYPE                     ENERGY_FORCE"
        print >> system, "!@SET RTYPE                     GEO_OPT"
        print >> system, "!@SET RTYPE                     MD"
        print >> system, "!@SET CPUTIME                   "+CPUTIME
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! Files options"
        print >> system, "!"
        print >> system, " @SET RESTART                   FALSE"
        print >> system, " @SET BASISFILE                 "+BASIS_SET_FILE_NAME
        print >> system, " @SET PSEUDOFILE                "+POTENTIAL_FILE_NAME
        print >> system, "!@SET WAVEFILE                  "+WAVE_FILE_NAME
        print >> system, "!@SET RESTARTFILE               "+RESTART_FILE_NAME
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! DFT calculation options"
        print >> system, "!"
        print >> system, " @SET CUTOFF                    "+CUTOFF
        print >> system, " @SET MGRIDS                    "+MGRIDS
        print >> system, " @SET SCF_NCYCLES               "+SCF_NCYCLES
        print >> system, " @SET SCF_CONV                  "+SCF_CONV
        print >> system, " @IF ( ${RESTART} == TRUE )"
        print >> system, "   @SET SCF_GUESS               RESTART"
        print >> system, " @ENDIF"
        print >> system, " @IF ( ${RESTART} == FALSE )"
        print >> system, "   @SET SCF_GUESS               ATOMIC"
        print >> system, " @ENDIF"
        print >> system, ""
        print >> system, " @SET SCF_MINI                  "+SCF_MIN
        print >> system, " @SET FUNCTIONAL                "+FUNCTIONAL
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! Geometry optimization options"
        print >> system, "!"
        print >> system, " @SET GEO_MIN                   "+GEO_MINI
        print >> system, " @SET GEO_MAXS                  "+GEO_MAXS
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! Molecular dynamics options"
        print >> system, "!"
        print >> system, " @SET MD_ENS                    "+MD_ENS
        print >> system, " @SET MD_STEPS                  "+MD_STEPS
        print >> system, " @SET MD_DT                     "+MD_DT
        print >> system, " @SET MD_TEMP                   "+MD_TEMP
        print >> system, ""
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "! Output options"
        print >> system, "!"
        print >> system, " @SET OUT_FORM                  "+OUT_FORM
        print >> system, ""
        print >> system, ""
        print >> system, ""

        ########################################################################
        # GLOBAL
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, " &GLOBAL"
        print >> system, "   PROJECT                     ${SYSNAME}"
        print >> system, "   RUN_TYPE                    ${RTYPE}"
        print >> system, "   PRINT_LEVEL                 LOW"
        print >> system, "!  WALLTIME                    ${CPUTIME}"
        print >> system, " &END GLOBAL"
        print >> system, ""

        ########################################################################
        # FORCE_EVAL (START)
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, " &FORCE_EVAL"

        ########################################################################
        # METHOD
        print >> system, "   METHOD Quickstep"
        print >> system, ""
        print >> system, "   &PRINT"
        print >> system, "     &FORCE"
        print >> system, "     &END FORCE"
        print >> system, "   &END PRINT"
        print >> system, ""
        if not OPT_STD:
            print >> system, "   @INCLUDE 'subsys.inc'"
            print >> system, ""

    ############################################################################
    if OPT_STD:
        subsys = sys.stdout
    else:
        try:
            subsys = open('subsys.inc','w')
        except:
            subsys.close()
            sys.exit("STOP: "+'subsys.inc'+" can't open")

    ############################################################################
    # SUBSYS (START)
    if OPT_STD:
        print >> subsys, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    print >> subsys, "   &SUBSYS"
    print >> subsys, ""

    for ion in range(nion):
        print >> subsys, "     &KIND",atoms_index[ion]
        print >> subsys, "       ELEMENT ",atoms_index[ion]
        print >> subsys, "       BASIS_SET DZVP_GTH-PADE"
        print >> subsys, "       POTENTIAL GTH-PADE-q4"
        print >> subsys, "     &END KIND"
        print >> subsys, ""

    ########################################################################
    # Crystal Structure
    print >> subsys, "     &CELL"
    print >> subsys, "       A %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0])
    print >> subsys, "       B %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1])
    print >> subsys, "       C %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2])
    print >> subsys, "       PERIODIC XYZ"
   #print >> subsys, "       UNIT ANGSTROM"
    print >> subsys, "     &END CELL"
    print >> subsys, ""

    print >> subsys, "     &COORD"
    for i in range(natom):
        atom = re.sub('_.*','',atoms_index_j[i])
        atoms_index_j[i]=atom

        print >> subsys, "       %2s %12.8f %12.8f %12.8f " \
               %(atoms_index_j[i], \
               position[i][0],position[i][1],position[i][2])

    print >> subsys, "     &END COORD"
    print >> subsys, ""


    ############################################################################
    # SUBSYS (END)
    print >> subsys, "   &END SUBSYS"
    print >> subsys, ""

    if not OPT_STD:
        subsys.close()

    if OPT_INP or OPT_STD:
        ########################################################################
        # DFT
        print >> system, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        print >> system, "   &DFT"
        print >> system, "      BASIS_SET_FILE_NAME           ${BASISFILE}"
        print >> system, "      POTENTIAL_FILE_NAME           ${PSEDOFILE}"
        print >> system, ""
        print >> system, "      @IF ( ${RESTART} == TRUE )"
        print >> system, "          WFN_RESTART_FILE_NAME     ${WAVEFILE}"
        print >> system, "      @ENDIF"
        print >> system, ""
        print >> system, "      &QS"
        print >> system, "        EPS_DEFAULT                 1.0E-10"
        print >> system, "      &END QS"
        print >> system, ""
        print >> system, "      &MGRID"
        print >> system, "        MGRIDS                      ${MGRIDS}"
        print >> system, "        CUTOFF                      ${CUTOFF}"
        print >> system, "        REL_CUTOFF 60"
        print >> system, "      &END MGRID"
        print >> system, ""
        print >> system, "     &XC"
        print >> system, "       &XC_FUNCTIONAL PADE"
        print >> system, "       &END XC_FUNCTIONAL"
        print >> system, "     &END XC"
        print >> system, ""
        print >> system, "     &SCF"
        print >> system, "       SCF_GUESS ATOMIC"
        print >> system, "       EPS_SCF 1.0E-7"
        print >> system, "       MAX_SCF 300"
        print >> system, "       &DIAGONALIZATION ON"
        print >> system, "         ALGORITHM STANDARD"
        print >> system, "       &END DIAGONALIZATION"
        print >> system, "       &MIXING T"
        print >> system, "         METHOD BROYDEN_MIXING"
        print >> system, "         ALPHA 0.4"
        print >> system, "         NBROYDEN 8"
        print >> system, "     &END SCF"
        print >> system, ""
        print >> system, "   &END DFT"
        print >> system, ""
        print >> system, "   &PRINT"
        print >> system, "     &FORCES ON"
        print >> system, "     &END FORCES"
        print >> system, "   &END PRINT"
        print >> system, ""

        ########################################################################
        # FORCE_EVAL (END)
        print >> system, "&END FORCE_EVAL"

    if not OPT_STD and OPT_INP:
        system.close()

