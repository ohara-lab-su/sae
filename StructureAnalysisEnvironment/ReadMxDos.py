#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
# ReadMxDos.py
#
#  *.Dos.Tetrahedron
#
################################################################################
#
# 2015.02.25
#  get_tdos, get_inttdos, get_ispin, get_natom, get_titile  の実装等
#
# 2015.02.24
#    startup
#    主に ReadMxDat, ReadMxDatMethod の整備
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

import sys
import os
import gzip
#import re
import optparse
import numpy as np

#from copy import deepcopy

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadMxDos(object):

    ###################################
    # インスタンス作成
    def __init__(self,name,suffix):

        dosname = name+suffix
        if os.path.exists(dosname):
            GZIP=False
        elif os.path.exists(dosname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+dosname+" or "+dosname+".gz file not found")
    
        try:
            if GZIP:
                tmp = gzip.open(dosname+".gz")
            else:
                tmp = open(dosname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+dosname+" or "+dosname+".gz does'nt open")
        finally:
            tmp.close()
    
        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1

    ###################################
    # *.out or *.dat から ISPIN 情報を読み込む( out 優先 )
    def get_ispin(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(name+'.out') or os.path.exists(name+'.out'+'.gz'):
            class_name = 'ReadMxOut'
            datname = name+'.out'
        elif os.path.exists(name+'.dat') or os.path.exists(name+'.dat'+'.gz'):
            class_name = 'ReadMxDat'
            datname = name+'.dat'
        else:
            sys.exit("STOP: "+name+".out or "+name+".dat file not found")

        module = __import__(module_name,globals(),locals(),[class_name],-1)
        klass = getattr(module,class_name)

        dat = klass(datname)
        self.ispin = dat.get_ispin()

        return self.ispin
    
    ###################################
    # *.out or *.dat から NATOM 情報を読み込む( out 優先 )
    def get_natom(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(name+'.out') or os.path.exists(name+'.out'+'.gz'):
            class_name = 'ReadMxOut'
            datname = name+'.out'
        elif os.path.exists(name+'.dat') or os.path.exists(name+'.dat'+'.gz'):
            class_name = 'ReadMxDat'
            datname = name+'.dat'
        else:
            sys.exit("STOP: "+name+".out or "+name+".dat file not found")

        module = __import__(module_name,globals(),locals(),[class_name],-1)
        klass = getattr(module,class_name)

        dat = klass(datname)
        self.natom = dat.get_natom()

        return self.natom

    ###################################
    # *.out or *.dat から TITLE 情報を読み込む( out 優先 )
    def get_title(self):
        module_name = 'StructureAnalysisEnvironment'
        if os.path.exists(name+'.out') or os.path.exists(name+'.out'+'.gz'):
            class_name = 'ReadMxOut'
            datname = name+'.out'
        elif os.path.exists(name+'.dat') or os.path.exists(name+'.dat'+'.gz'):
            class_name = 'ReadMxDat'
            datname = name+'.dat'
        else:
            sys.exit("STOP: "+name+".out or "+name+".dat file not found")

        module = __import__(module_name,globals(),locals(),[class_name],-1)
        klass = getattr(module,class_name)

        dat = klass(datname)
        self.title = dat.get_title()

        return self.title


    ###################################
    # EMAX (エネルギー固有値の最大値)
    def get_emax(self):
        NEDOS = self.get_nedos()
        self.EMAX = float(self.datlines[NEDOS-1].split()[0])
        return self.EMAX

    ###################################
    # EMAX (エネルギー固有値の最小値)
    def get_emin(self):
        self.EMIN = float(self.datlines[0].split()[0])
        return self.EMIN

    ###################################
    # NEDOS (DOSの分割数, OpenMXの*.DOS.Tetrahedron ではファイルの行数に相当)
    def get_nedos(self):
        return self.num

    ###################################
    def get_efermi(self):
        pass

    ###################################
    def get_lorbit(self):
        pass

    ###################################
    def get_eng(self):
        pass

    ###################################
    # TDOS ( *.DOS.Tetrahedron ) 読み込み
    def get_tdos(self,spin=0):

        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
            if NSPIN >= 2:
                dos[i,0] = float(self.datlines[i].split()[1])
                dos[i,1] = float(self.datlines[i].split()[2])
                intdos[i,0] = float(self.datlines[i].split()[3])
                intdos[i,1] = float(self.datlines[i].split()[4])
            else:
                dos[i,0] = float(self.datlines[i].split()[1])
                intdos[i,0] = float(self.datlines[i].split()[2])

        self.TDOS = dos[:,spin]
        return self.TDOS

    ###################################
    # INTTDOS ( *.DOS.Tetrahedron ) 読み込み
    def get_inttdos(self,spin=0):
        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
            if NSPIN >= 2:
                dos[i,0] = float(self.datlines[i].split()[1])
                dos[i,1] = float(self.datlines[i].split()[2])
                intdos[i,0] = float(self.datlines[i].split()[3])
                intdos[i,1] = float(self.datlines[i].split()[4])
            else:
                dos[i,0] = float(self.datlines[i].split()[1])
                intdos[i,0] = float(self.datlines[i].split()[2])

        self.INTTDOS = intdos[:,spin]
        return self.INTTDOS

    def get_pdos(self,lm=0,atom=0,spin=0):
        pass

    def get_pdos_all(self):
        pass

    def get_ldos(self,l=0,atom=0,spin=0):
        pass

    def get_ldos_all(self):
        pass

    def get_tdos_spd(self,l=0,spin=0):
        pass

    def get_ldos_ion(self,l=0,ion=0,spin=0):
        pass

    def get_ldos_ion_all(self):
        pass

################################################################################
if __name__ == '__main__':

    name = 'Cu'
    suffix = '.DOS.Tetrahedron'
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        name=options.INPUT
                                                                                
    if len(args) > 0:
        name=args[0]

    dos = ReadMxDos(name,suffix)

    ispin = dos.get_ispin()
    natom = dos.get_natom()
    title = dos.get_title()

    print ispin
    print natom
    print title

    tdos = dos.get_tdos()

    emax = dos.get_emax()
    emin = dos.get_emin()
    print emin,emax

################################################################################
