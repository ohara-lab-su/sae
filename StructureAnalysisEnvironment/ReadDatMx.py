#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み class
#
#  ReadDatMx
#    *.dat 名の重複があるので DatMx とする( 例 RMC_POT の *.dat 形式 )
#
################################################################################
#
# 2015.02.12 1st
#
################################################################################
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2014, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.2"                                                                  
################################################################################

import sys
import os
import re
import gzip
import numpy as np

import optparse 


################################################################################
class ReadDatMx(object):

    ###############################################
    ## init and Read POSCAR
    def __init__(self,datname):

        if os.path.exists(datname):
            GZIP=False
        elif os.path.exists(datname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+datname+" or "+datname+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(datname+".gz")
            else:
                tmp = open(datname)

            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+datname+" does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num = int(len(self.datlines)) -1


    ###################################
    # title (System.Name)
    def get_title(self):
        title_reg = re.compile('.*System\.Name')
        for i in range(self.num):
            if bool(title_reg.match(self.datlines[i])):
                src = self.datlines[i].split()[1]
                self.SYSTEM = re.sub(' *$','',src) 
                break
        return self.SYSTEM


    ###################################
    # natom
    def get_natom(self):
        reg = re.compile('.*Atoms\.Number')
        for i in range(self.num):
            if bool(reg.match(self.datlines[i])):
                self.natom = int(self.datlines[i].split()[1])
                break 
        return self.natom


    ###################################
    # NION
    def get_nion(self):
        reg = re.compile('.*Species\.Number')
        for i in range(self.num):
            if bool(reg.match(self.datlines[i])):
                self.NION = int(self.datlines[i].split()[1])
                break
        return self.NION


    ###################################
    # atoms_index
    def get_atoms_index(self):
        nion = self.get_nion()
        reg0 = re.compile('.*\<Definition\.of\.Atomic\.Species')
        reg1 = re.compile('.*Definition\.of\.Atomic\.Species\>')
        self.atoms_index = []
        for i in range(self.num):
            if bool(reg0.match(self.datlines[i])):
                j = 1
                while not bool(reg1.match(self.datlines[i+j])):
                    self.atoms_index.append(self.datlines[i+j].split()[0])
                    j += 1
                if nion != j -1 :
                    sys.exit("STOP: Atomic.Species Tag Error")
                break
        return self.atoms_index


    ###################################
    # atoms
    def get_atoms(self):
        nion = self.get_nion()
        natom = self.get_natom()
        reg0 = re.compile('.*\<Atoms\.SpeciesAndCoordinates')
        reg1 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')
        self.atoms = np.zeros(nion,dtype=int)
        for i in range(self.num):
            if bool(reg0.match(self.datlines[i])):
                j = 1
                species0 = ''
                types = -1
                while not bool(reg1.match(self.datlines[i+j])):
                    species = self.datlines[i+j].split()[1]
                    if species != species0:
                        types += 1
                    self.atoms[types] += 1
                    species0 = species
                    j += 1
                if natom != j -1 :
                    sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")
                break
        return self.atoms


    ###################################
    ## scale factor
    def get_scale(self):
        return 1.0


    ###################################
    ## Read Translation Vector                                                  
    ##         x   y   z                                                        
    ##   t1 = t11 t21 t31                                                       
    ##   t2 = t12 t22 t32                                                       
    ##   t3 = t13 t23 t33                                                       
    ##
    ##   Unit を調べて AU のときは Ang にして返す
    ##
    def get_t(self):
        BOHR= 0.529177   # Bohr radius in Angstrom

        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg2 = re.compile('.*Atoms\.UnitVectors\.Unit')
        reg3 = re.compile('.*\<Atoms\.UnitVectors ')
        reg4 = re.compile('.*Atoms\.UnitVectors\>')

        # get UNIT
        for i in range(self.num):
            if bool(reg2.match(self.datlines[i])):
                if bool(reg_unit0.match(self.datlines[i].split()[1])):
                   #FLAG_UNIT = True   # 'Atomic Unit'
                   UNIT = BOHR
                elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                   #FLAG_UNIT = False  # 'Ang'
                   UNIT = 1.0
                else:
                    sys.exit("STOP: Unknown Atoms.UnitVectors.Unit")
                break

        # get translation vector
        self.t = np.zeros((3,3))
        for i in range(self.num):
            if bool(reg3.match(self.datlines[i])):
                self.t[0,0] = float(self.datlines[i+1+0].split()[0])*UNIT
                self.t[1,0] = float(self.datlines[i+1+0].split()[1])*UNIT
                self.t[2,0] = float(self.datlines[i+1+0].split()[2])*UNIT

                self.t[0,1] = float(self.datlines[i+1+1].split()[0])*UNIT
                self.t[1,1] = float(self.datlines[i+1+1].split()[1])*UNIT
                self.t[2,1] = float(self.datlines[i+1+1].split()[2])*UNIT

                self.t[0,2] = float(self.datlines[i+1+2].split()[0])*UNIT
                self.t[1,2] = float(self.datlines[i+1+2].split()[1])*UNIT
                self.t[2,2] = float(self.datlines[i+1+2].split()[2])*UNIT

                if not bool(reg4.match(self.datlines[i+1+3])):
                    sys.exit("STOP: Atoms.UnitVectors Error")
                break

        return self.t


    ###################################
    ## selective モードの取得
    def get_selective(self):
        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_md0 = re.compile('.*\<MD\.Fixed\.XYZ')

        self.selective =False
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_md0.match(self.datlines[i])):
                    self.selective=True
                    break

        return self.selective


    ###################################
    # 内部座標のDirect Mode の取得
    def get_direct(self):
        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg_unit2 = re.compile('FRAC',re.IGNORECASE)
        reg3 = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')

        # get UNIT
        for i in range(self.num):
            if bool(reg3.match(self.datlines[i])):
                if bool(reg_unit0.match(self.datlines[i].split()[1])):
                   direct = False
                elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                   direct = False
                elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                   direct = True
                else:
                    sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                break

        return direct


    ###################################
    ##  position
    ##    内部座標の取得 AU --> Ang 変換だけはここでやる
    ##    (カーテシアンとダイレクトの変換はここでは行わない)
    def get_position(self):
        BOHR= 0.529177   # Bohr radius in Angstrom

        comment_reg = re.compile('^#.*',re.IGNORECASE)
        reg_unit0 = re.compile('AU',re.IGNORECASE)
        reg_unit1 = re.compile('Ang',re.IGNORECASE)
        reg_unit2 = re.compile('FRAC',re.IGNORECASE)
        reg_position0 = re.compile('.*Atoms\.SpeciesAndCoordinates\.Unit')
        reg_position1 = re.compile('.*\<Atoms\.SpeciesAndCoordinates ')
        reg_position2 = re.compile('.*Atoms\.SpeciesAndCoordinates\>')

        natom = self.get_natom()

        # get UNIT
        for i in range(self.num):
            if bool(reg_position0.match(self.datlines[i])):
                if bool(reg_unit0.match(self.datlines[i].split()[1])):
                  #direct = False
                   UNIT = BOHR        # 'Atomic Unit'
                elif bool(reg_unit1.match(self.datlines[i].split()[1])):
                  #direct = False
                   UNIT = 1.0 # 'Ang'
                elif bool(reg_unit2.match(self.datlines[i].split()[1])):
                  #direct = True
                   UNIT = 1.0
                else:
                    sys.exit("STOP: Unknown Atoms.SpeciesAndCoordinates.Unit")
                break

        self.p = np.zeros((natom,3))
        for i in range(self.num):
            if not bool(comment_reg.match(self.datlines[i])):
                if bool(reg_position1.match(self.datlines[i])):
                    j = 1
                    while not bool(reg_position2.match(self.datlines[i+j])):
                        self.p[j-1,0] = float(self.datlines[i+j].split()[2])*UNIT
                        self.p[j-1,1] = float(self.datlines[i+j].split()[3])*UNIT
                        self.p[j-1,2] = float(self.datlines[i+j].split()[4])*UNIT
                        j += 1
                    if natom != j -1 :
                        sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")

        return self.p


    ###################################
    ## fixed
    ##  fix の情報は VASP 相当に変更する(F=Fix, T=moving True)
    ##  position の取得と別のmethodにする
    ##
    def get_fix(self):
        natom = self.get_natom()
        selective = self.get_selective()
       #self.fix = []
        self.fix = np.zeros((natom,3),dtype='S')
        if selective:
            comment_reg = re.compile('^#.*',re.IGNORECASE)
            reg_md0 = re.compile('.*\<MD\.Fixed\.XYZ')
            reg_md1 = re.compile('.*MD\.Fixed\.XYZ\>')

            self.selective =False
            for i in range(self.num):
                if not bool(comment_reg.match(self.datlines[i])):
                    if bool(reg_md0.match(self.datlines[i])):
                        self.selective=True
                        j = 1
                        while not bool(reg_md1.match(self.datlines[i+j])):
                            fix_x = int(self.datlines[i+j].split()[1])
                            fix_y = int(self.datlines[i+j].split()[2])
                            fix_z = int(self.datlines[i+j].split()[3])

                            if fix_x == 1:
                                fix_x = 'F'  # Moving False ( Fixed )
                            elif fix_x == 0:
                                fix_x = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_y == 1:
                                fix_y = 'F'  # Moving False ( Fixed )
                            elif fix_y == 0:
                                fix_y = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                            if fix_z == 1:
                                fix_z = 'F'  # Moving False ( Fixed )
                            elif fix_z == 0:
                                fix_z = 'T'  # Moving True  ( non Fixed )
                            else:
                                sys.exit("STOP: unknown Fixed Parameter")

                           #self.fix.append([fix_x, fix_y, fix_z])
                            self.fix[j-1,0] = fix_x
                            self.fix[j-1,1] = fix_y
                            self.fix[j-1,2] = fix_z
                            j += 1
                        if natom != j -1 :
                            sys.exit("STOP: Atomic.Number and Atoms.SpeciesAndCoordinates Tag Error")
                        break
        return self.fix


################################################################################
if __name__ == '__main__':

    name = 'openmx.dat'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input',
                        dest='INPUT',
                        default=name,
                        )
    options, args = parser.parse_args()
    name = options.INPUT

    dat = ReadDatMx(name)

    title = dat.get_title()
    nion = dat.get_nion()
    natom = dat.get_natom()
    atoms = dat.get_atoms()
    atoms_index = dat.get_atoms_index()
    scale = dat.get_scale()
    t = dat.get_t()
    selective = dat.get_selective()
    direct = dat.get_direct()
    position = dat.get_position()
    fix = dat.get_fix()

    print title
    print " ",scale
    print "  %13.9f %13.9f %13.9f" %( t[0,0],t[1,0],t[2,0] )
    print "  %13.9f %13.9f %13.9f" %( t[0,1],t[1,1],t[2,1] )
    print "  %13.9f %13.9f %13.9f" %( t[0,2],t[1,2],t[2,2] )

    print " ",
    for i in range(nion):
        print atoms_index[i],
    print " "

    print " ",
    for i in range(nion):
        print atoms[i],
    print " "

    if selective:
        print "Selective Dynamics"
    if direct:
        print "Direct"
    else:
        print "Cartesian"

    for i in range(natom):
        print " %13.9f %13.9f %13.9f" \
                % ( position[i,0],position[i,1],position[i,2] ),
        if selective:
            print "",
            print fix[i,0],fix[i,1],fix[i,2],
        print ""

#   for i in range(natom):
#       print fix[i][0], fix[i][1], fix[i][2]

