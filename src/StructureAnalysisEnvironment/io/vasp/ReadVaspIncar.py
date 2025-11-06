#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Read INCAR
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応暫定
#
# 2015.06.18
#  タグが存在しないときは VASP デフォルトを返す
#  注意) NBANDS は INCAR だけからではデフォルト値は出せないので None を返す
#
# 2015.06.18 startup
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.0"

################################################################################

import sys
import os
import re
# import gzip
# import numpy as np

import optparse

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.Method import *


# import SpaceGroupEnvironment as SGE

################################################################################
class ReadVaspIncar(object):

    ###############################################
    ## init and Read INCAR
    def __init__(self, INCAR='INCAR'):

        # read INCAR
        self.datlines, self.num = SAEnv.read_dataline1(INCAR)

        # set TAG rule
        title_reg = re.compile('.*SYSTEM', re.IGNORECASE)
        nsw_reg = re.compile('.*NSW', re.IGNORECASE)
        sigma_reg = re.compile('.*SIGMA', re.IGNORECASE)
        ismear_reg = re.compile('.*ISMEAR', re.IGNORECASE)
        ediff_reg = re.compile('.*EDIFF', re.IGNORECASE)
        ediffg_reg = re.compile('.*EDIFFG', re.IGNORECASE)
        nbands_reg = re.compile('.*NBANDS', re.IGNORECASE)
        ispin_reg = re.compile('.*ISPIN', re.IGNORECASE)
        nelm_reg = re.compile('.*NELM', re.IGNORECASE)
        smass_reg = re.compile('.*SMASS', re.IGNORECASE)
        ibrion_reg = re.compile('.*IBRION', re.IGNORECASE)
        laechg_reg = re.compile('.*LAECHG', re.IGNORECASE)
        ngxf_reg = re.compile('.*NGXF', re.IGNORECASE)
        ngyf_reg = re.compile('.*NGYF', re.IGNORECASE)
        ngzf_reg = re.compile('.*NGZF', re.IGNORECASE)
        npar_reg = re.compile('.*NPAR', re.IGNORECASE)
        isym_reg = re.compile('.*ISYM', re.IGNORECASE)
        gga_reg = re.compile('.*GGA', re.IGNORECASE)
        istart_reg = re.compile('.*ISTART', re.IGNORECASE)
        icharg_reg = re.compile('.*ICHARG', re.IGNORECASE)

        # defaults
        self.ispin = 1
        self.nsw = 0
        self.ismear = 1
        self.sigma = 0.2
        self.npar = 1
        self.laechg = False
        self.ngxf = None
        self.ngyf = None
        self.ngzf = None
        self.nbands = None
        self.ediff = 1.0e-4
        self.ediffg = self.ediff * 10.0
        self.alog = 'Normal'
        self.nedos = 301
        self.lreal = False
        self.isym = 1
        self.gga = None
        self.nelm = 60

        # check current file
        if os.path.exists('WAVECAR'):
            self.istart = 1
        else:
            self.istart = 0

        for i in range(self.num):

            # ISTART
            if bool(istart_reg.match(self.datlines[i])):
                self.istart = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # ICHARG
            if bool(icharg_reg.match(self.datlines[i])):
                self.icharg = int(re.sub('.*=', '', self.datlines[i]).split()[0])
                print("self.icharg %s" % str(self.icharg))

            # SYSTEM
            if bool(title_reg.match(self.datlines[i])):
                self.title = str(re.sub('.*=', '', self.datlines[i]).split()[0])

            # GGA
            if bool(gga_reg.match(self.datlines[i])):
                self.gga = str(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NSW
            if bool(nsw_reg.match(self.datlines[i])):
                self.nsw = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # SIGMA
            if bool(sigma_reg.match(self.datlines[i])):
                self.sigma = float(re.sub('.*=', '', self.datlines[i]).split()[0])

            # ISMEAR
            if bool(ismear_reg.match(self.datlines[i])):
                self.ismear = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # EDIFF
            if bool(ediff_reg.match(self.datlines[i])) and not bool(ediffg_reg.match(self.datlines[i])):
                self.ediff = float(re.sub('.*=', '', self.datlines[i]).split()[0])

            # EDIFFG
            if bool(ediffg_reg.match(self.datlines[i])):
                self.ediffg = float(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NBANDS
            if bool(nbands_reg.match(self.datlines[i])):
                self.nbands = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # ISYM
            if bool(isym_reg.match(self.datlines[i])):
                self.isym = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # ISPIN
            if bool(ispin_reg.match(self.datlines[i])):
                self.ispin = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NELM
            if bool(nelm_reg.match(self.datlines[i])):
                self.nelm = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # SMASS
            if bool(smass_reg.match(self.datlines[i])):
                self.smass = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # IBRION
            if bool(ibrion_reg.match(self.datlines[i])):
                self.ibrion = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # LAECHG
            if bool(laechg_reg.match(self.datlines[i])):
                if bool(re.compile('^.*=.*T', re.IGNORECASE).match(self.datlines[i])):
                    self.laechg = True
                elif bool(re.compile('^.*=.*F', re.IGNORECASE).match(self.datlines[i])):
                    self.laechg = False

            # NGXF
            if bool(ngxf_reg.match(self.datlines[i])):
                self.ngxf = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NGYF
            if bool(ngyf_reg.match(self.datlines[i])):
                self.ngyf = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NGZF
            if bool(ngzf_reg.match(self.datlines[i])):
                self.ngzf = int(re.sub('.*=', '', self.datlines[i]).split()[0])

            # NPAR
            if bool(npar_reg.match(self.datlines[i])):
                self.npar = int(re.sub('.*=', '', self.datlines[i]).split()[0])

        # check ISTART and ICHARG
        try:
            self.icharg
        except:
            if self.istart == 0:
                self.icharg = 2
            else:
                self.icharg = 0

    def get_title(self):
        self.title = self.title if hasattr(self.__class__.__name__, 'title') else 'unknown system'
        return self.title

    def get_istart(self):
        return self.istart

    def get_icharg(self):
        return self.icharg

    def get_system(self):
        self.system = self.system if hasattr(self, 'system') else 'unknown system'
        return self.title

    def get_nsw(self):
        self.nsw = self.nsw if hasattr(self, 'nsw') else 0
        return self.nsw

    def get_sigma(self):
        self.sigma = self.sigma if hasattr(self, 'sigma') else 0.2
        return self.sigma

    def get_ismear(self):
        self.ismear = self.ismear if hasattr(self, 'ismear') else 1
        return self.ismear

    def get_ediff(self):
        self.ediff = self.ediff if hasattr(self, 'ediff') else 1.0e-4
        return self.ediff

    def get_ediffg(self):
        try:
            self.ediffg = self.ediffg
        except:
            ediff = self.get_ediff()
            self.ediffg = ediff * 10.0
        return self.ediffg

    def get_nbands(self):
        self.nbands = self.nbands if hasattr(self, 'nbands') else None
        return self.nbands

    def get_gga(self):
        self.gga = self.gga if hasattr(self, 'gga') else None
        return self.gga

    def get_isym(self):
        self.isym = self.isym if hasattr(self, 'isym') else 1
        return self.isym

    def get_ispin(self):
        self.ispin = self.ispin if hasattr(self, 'ispin') else 1
        return self.ispin

    def get_nelm(self):
        self.nelm = self.nelm if hasattr(self, 'nelm') else 60
        return self.nelm

    def get_ibrion(self):
        try:
            self.ibrion = self.ibrion
        except:
            NSW = self.get_nsw()
            if NSW > 0:
                self.ibrion = 2
            else:
                self.ibrion = -1
        return self.ibrion

    def get_laechg(self):
        self.laechg = self.laechg if hasattr(self, 'laechg') else False
        return self.laechg

    def get_ngxf(self):
        self.ngxf = self.ngxf if hasattr(self, 'ngxf') else None
        return self.ngxf

    def get_ngyf(self):
        self.ngyf = self.ngyf if hasattr(self, 'ngyf') else None
        return self.ngyf

    def get_ngzf(self):
        self.ngzf = self.ngzf if hasattr(self, 'ngzf') else None
        return self.ngzf


################################################################################
if __name__ == '__main__':

    name = 'INCAR'
    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT:
        name = parser.INPUT

    incar = ReadVaspIncar()

    TITLE = incar.get_title()
    SYSTEM = incar.get_system()
    NSW = incar.get_nsw()
    IBRION = incar.get_ibrion()
    SIGMA = incar.get_sigma()
    ISMEAR = incar.get_ismear()
    EDIFF = incar.get_ediff()
    EDIFFG = incar.get_ediffg()
    NBANDS = incar.get_nbands()
    ISPIN = incar.get_ispin()
    NELM = incar.get_nelm()
    NGXF = incar.get_ngxf()
    NGYF = incar.get_ngyf()
    NGZF = incar.get_ngyf()
    ISTART = incar.get_istart()
    ICHARG = incar.get_icharg()

    #   print "TITLE  :", TITLE
    print("SYSTEM :%s" % str(SYSTEM))
    print("NSW    :%s" % str(NSW))
    print("IBRION :%s" % str(IBRION))
    print("SIGMA  :%s" % str(SIGMA))
    print("ISMEAR :%s" % str(ISMEAR))
    print("EDIFF  :%s" % str(EDIFF))
    print("EDIFFG :%s" % str(EDIFFG))
    print("NBANDS :%s" % str(NBANDS))
    print("ISPIN  :%s" % str(ISPIN))
    print("NELM   :%s" % str(NELM))
    print("NGXF   :%s" % str(NGXF))
    print("NGYF   :%s" % str(NGYF))
    print("NGZF   :%s" % str(NGZF))

    print("")
    print("ISTART :%s" % str(ISTART))
    print("ICHARG :%s" % str(ICHARG))
