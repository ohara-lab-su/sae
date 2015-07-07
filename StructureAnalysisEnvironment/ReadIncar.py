#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Read INCAR
#
################################################################################
#
# 2015.06.18
#  タグが存在しないときは VASP デフォルトを返す
#  注意) NBANDS は INCAR だけからではデフォルト値は出せないので None を返す
#
# 2015.06.18 startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.0"
################################################################################

#import sys
#import os
import re
#import gzip
#import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadIncar(object):

    ###############################################
    ## init and Read INCAR
    def __init__(self,INCAR='INCAR'):

        # read INCAR
        self.datlines,self.num = SAE.read_dataline1(INCAR)

        # set TAG rule
        title_reg = re.compile('.*SYSTEM',re.IGNORECASE)
        nsw_reg = re.compile('.*NSW',re.IGNORECASE)
        sigma_reg = re.compile('.*SIGMA',re.IGNORECASE)
        ismear_reg = re.compile('.*ISMEAR',re.IGNORECASE)
        ediff_reg = re.compile('.*EDIFF',re.IGNORECASE)
        ediffg_reg = re.compile('.*EDIFFG',re.IGNORECASE)
        nbands_reg = re.compile('.*NBANDS',re.IGNORECASE)
        ispin_reg = re.compile('.*ISPIN',re.IGNORECASE)
        nelm_reg = re.compile('.*NELM',re.IGNORECASE)
        smass_reg = re.compile('.*SMASS',re.IGNORECASE)
        ibrion_reg = re.compile('.*IBRION',re.IGNORECASE)
        laechg_reg = re.compile('.*LAECHG',re.IGNORECASE)

        self.ispin = 1
        self.nsw = 0
        self.laechg = '.FALSE.'

        for i in range(self.num):

            # SYSTEM
            if bool(title_reg.match(self.datlines[i])):
                self.title = str(re.sub('.*=','',self.datlines[i]).split()[0])

            # NSW
            if bool(nsw_reg.match(self.datlines[i])):
                self.nsw = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # SIGMA
            if bool(sigma_reg.match(self.datlines[i])):
                self.sigma = float(re.sub('.*=','',self.datlines[i]).split()[0])

            # ISMEAR
            if bool(ismear_reg.match(self.datlines[i])):
                self.ismear = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # EDIFF
            if bool(ediff_reg.match(self.datlines[i])) and not bool(ediffg_reg.match(self.datlines[i])):
                self.ediff = float(re.sub('.*=','',self.datlines[i]).split()[0])

            # EDIFFG
            if bool(ediffg_reg.match(self.datlines[i])):
                self.ediffg = float(re.sub('.*=','',self.datlines[i]).split()[0])

            # NBANDS
            if bool(nbands_reg.match(self.datlines[i])):
                self.nbands = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # ISPIN
            if bool(ispin_reg.match(self.datlines[i])):
                self.ispin = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # NELM
            if bool(nelm_reg.match(self.datlines[i])):
                self.nelm = int(re.sub('.*=','',self.datlines[i]).split()[0])
                print self.nelm

            # SMASS
            if bool(smass_reg.match(self.datlines[i])):
                self.smass = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # IBRION
            if bool(ibrion_reg.match(self.datlines[i])):
                self.ibrion = int(re.sub('.*=','',self.datlines[i]).split()[0])

            # LAECHG
            if bool(ibrion_reg.match(self.datlines[i])):
                self.laechg = int(re.sub('.*=','',self.datlines[i]).split()[0])

    def get_title(self):
        self.title = self.title if hasattr(self.__class__.__name__,'title') else 'unknown system'
        return self.title

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
            self.ediffg = ediff*10.0
        return self.ediffg

    def get_nbands(self):
        self.nbands = self.nbands if hasattr(self, 'nbands') else None
        return self.nbands

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

################################################################################
if __name__ == '__main__':

    name = 'INCAR'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    options, args = parser.parse_args()

    if options.INPUT:
        name = parser.INPUT

    incar = ReadIncar()

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

#   print "TITLE  :", TITLE
    print "SYSTEM :", SYSTEM
    print "NSW    :", NSW
    print "IBRION :", IBRION
    print "SIGMA  :", SIGMA
    print "ISMEAR :", ISMEAR
    print "EDIFF  :", EDIFF
    print "EDIFFG :", EDIFFG
    print "NBANDS :", NBANDS
    print "ISPIN  :", ISPIN
    print "NELM   :", NELM

