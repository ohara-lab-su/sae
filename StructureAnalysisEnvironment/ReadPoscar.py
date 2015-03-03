#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR 読み込み class
#
#          
# t[3,3]            :  基本並進ベクトル(注意:配列内indexは0から)
#
#                              x   y   z
#                        t1 = a11 a21 a31  ! lattice vector t1
#                        t2 = a12 a22 a32  ! lattice vector t2
#                        t3 = a13 a23 a33  ! lattice vector t3
# 注意) 
#    t(基本並進行列)
#                             t11, t12, t13
#                             t21, t22, t23
#                             t31, t32, t33
#          
# atoms[i]          : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
# ion[j]            : 通し番号(max=natom)を与えると原子の種類番号を返す
# ion_local[j]      : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# position[j,3]     : 通し番号(max=natom)とx,y,z 指定で内部座標
# fix[j,3]          : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
# title             : タイトル
# scale             : 格子定数(スケールファクター)
# selective         : selective mode
# direct            : direct or cartesian
#
################################################################################
#
# 基本構造情報読み込み Method
#
#   get_title()
#   get_scale()
#   get_t()
#   get_vasp_version()
#   get_atoms()
#   get_atoms_index()
#   get_atoms_index_j()
#   get_nion()
#   get_natom()
#   get_ion()
#   get_ion_local()
#   get_selective()
#   get_direct()
#   get_position()
#   get_fix()
#
################################################################################
#
# 2015.02.12
#  get_position() の機能を get_fix() と分離した
#  fix はappend するのではなく numpy で初期化に変更
#
# 2015.02.12
#  get_selective() の機能を get_direct() と分離した
#
# 2015.02.09
#  read_poscar.py ( read_poscar_param.py ) をベースに class 化
#  基本的な method は先行する ReadDoscar や ReadOutcar などと同じくする
#
# 2015.01.20
#  gzip 対応版
#
# 2014.10.30 1st
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#                                                                                         
__status__     = "alpha"
__version__    = "0.0.5"
################################################################################

import sys
import os
import re
import gzip
import numpy as np

import optparse 

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 

################################################################################
class ReadPoscar(object):

    ###############################################
    ## init and Read POSCAR
    def __init__(self,POSCAR):

        if os.path.exists(POSCAR):
            GZIP=False
        elif os.path.exists(POSCAR+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+POSCAR+" or "+POSCAR+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(POSCAR+".gz")
            else:
                tmp = open(POSCAR)

            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+POSCAR+" does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1

    ###############################################
    # TITLE
    def get_title(self):
        self.SYSTEM = self.datlines[0]
        return self.SYSTEM

    ###############################################
    # SCALE
    def get_scale(self):
        self.scale = float(self.datlines[1])
        return self.scale

    ###############################################
    ## Read Translation Vector
    ##         x   y   z
    ##   t1 = t11 t21 t31
    ##   t2 = t12 t22 t32
    ##   t3 = t13 t23 t33
    ##
    def get_t(self):
        v = self.datlines[2].split()
        t1_x = float(v[0])
        t1_y = float(v[1])
        t1_z = float(v[2])
        
        v = self.datlines[3].split()
        t2_x = float(v[0])
        t2_y = float(v[1])
        t2_z = float(v[2])
        
        v = self.datlines[4].split()
        t3_x = float(v[0])
        t3_y = float(v[1])
        t3_z = float(v[2])
        
        self.t = np.zeros((3,3))
        self.t[0,0] = t1_x
        self.t[1,0] = t1_y
        self.t[2,0] = t1_z

        self.t[0,1] = t2_x
        self.t[1,1] = t2_y
        self.t[2,1] = t2_z

        self.t[0,2] = t3_x
        self.t[1,2] = t3_y
        self.t[2,2] = t3_z

        return self.t

    ###############################################
    ## get VASP version
    def get_vasp_version(self):
        i=5
        atoms = self.datlines[i].split()
        if atoms[0].isdigit():
            self.vasp_version = 4
        else:
            self.vasp_version = 5

        return self.vasp_version
        
    ###############################################
    ## get VASP version, atoms
    ## atoms[i]  : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
    def get_atoms(self):
        VASP = int(self.get_vasp_version())
        i=5
        self.atoms = []
        if VASP == 4:
            self.atoms.extend(self.datlines[i].split())
        elif VASP == 5:
            i += 1
            self.atoms.extend(self.datlines[i].split())
        else:
            sys.exit("Error: unknown VASP format")

        return self.atoms
   
    ###############################################
    ## get VASP version, atoma_index
    ## atoms_index[i] : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    def get_atoms_index(self):
        VASP = self.get_vasp_version()
        i=5
        atoms = self.datlines[i].split()
        self.atoms_index = []
        if VASP == 5:
            self.atoms_index=list(atoms)

        return self.atoms_index

    ###############################################
    ## atoms_index の通し番号版
    ##    atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
    ##    atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    ##    ion[j]            : 通し番号(max=natom)を与えると原子の種類番号を返す
    def get_atoms_index_j(self):
        atoms_index = self.get_atoms_index()
        atoms = self.get_atoms()
        nion = self.get_nion()

        self.atoms_index_j = []
        for k in range(nion):
            for l in range(int(atoms[k])):
                self.atoms_index_j.append(str(atoms_index[k]))

        return self.atoms_index_j

    ###############################################
    # NION
    def get_nion(self):
        return len(self.get_atoms())

    ###############################################
    ## get number of atoms
    def get_natom(self):
        atoms = self.get_atoms()
        nion = int(len(atoms))
        self.natom = 0
        for j in range(nion):
            sum = int(atoms[j])
            self.natom = self.natom + sum

       #print "natom= ",self.natom
        return self.natom

    ###############################################
    ## get ion (makes index)
    ## ion[j] : 通し番号(max=natom)を与えると原子の種類番号を返す
    def get_ion(self):
        natom = self.get_natom()
        atoms = self.get_atoms()
        nion = int(len(atoms))
        self.ion = np.zeros(natom)
        tmp = -1
        for j in range(nion):
            local = -1
            for k in range(int(atoms[j])):
                tmp += 1
                local += 1
                self.ion[tmp] = int(j)
               #print tmp, int(ion[tmp])
        return self.ion

    ###############################################
    ## get ion_local (makes index)
    ## ion_local[j]  : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    def get_ion_local(self):
        natom = self.get_natom()
        atoms = self.get_atoms()
        nion = int(len(atoms))
        self.ion_local = np.zeros(natom)
        tmp = -1
        for j in range(nion):
            local = -1
            for k in range(int(atoms[j])):
                tmp += 1
                local += 1
                self.ion_local[tmp] = int(local)
               #print tmp, int(ion[tmp]), int(ion_local[tmp])
        return self.ion_local

    ###############################################
    ## get atomc coordinate mode
    def get_selective(self):
    
        VASP = self.get_vasp_version()
        if VASP == 4:
            i = 5+1
        else:
            i = 6+1

        num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
        selective_reg = re.compile('^S.*',re.IGNORECASE)

        tmp = self.datlines[i].split()
        if bool(num_reg.match(tmp[0])):
            print tmp[0]
            sys.exit("Format Error")
        else:
            if bool(selective_reg.match(tmp[0])):
               #print "selective True"
                i += 1
                tmp = self.datlines[i].split()
                self.selective = True
            else:
               #print "selective False"
                self.selective = False

        return self.selective
    
    ###############################################
    ## 内部座標のモードを取得
    def get_direct(self):

        VASP = self.get_vasp_version()
        if VASP == 4:
            i = 5+1
        else:
            i = 6+1

        selective = self.get_selective()
        if selective:
            i +=1

        num_reg = re.compile('^[+-]?(\d*\.\d+|\d+\.?\d*)([eE][+-]?\d+|)\Z')
        direct_reg = re.compile('^D.*',re.IGNORECASE)
        car_reg = re.compile('^C.*',re.IGNORECASE)

        tmp = self.datlines[i].split()
        if bool(num_reg.match(tmp[0])):
            print tmp[0]
            sys.exit("Format Error")
        if bool(direct_reg.match(tmp[0])):
           #print "Direct Mode"
            self.direct = True
        elif bool(car_reg.match(tmp[0])):
           #print "Cartesian Mode"
            self.direct = False

        return self.direct

    ###############################################
    ## get atomic coordinate position
    ##
    def get_position(self):

        VASP = self.get_vasp_version()
        if VASP == 4:
            i = 5
        else:
            i = 6

        selective = self.get_selective()
        if selective:
            i += 1

        natom = self.get_natom()
        self.position = np.zeros((int(natom),3))
        self.fix= np.zeros((int(natom),3),dtype='S')
    
        i += 2
        for j in range(natom):
            xyz = self.datlines[i+j].split()
            self.position[j,0] = xyz[0]
            self.position[j,1] = xyz[1]
            self.position[j,2] = xyz[2]
            if selective:
                self.fix[j,0] = str(xyz[3])
                self.fix[j,1] = str(xyz[4])
                self.fix[j,2] = str(xyz[5])
           #print j,
           #print " %16.12f %16.12f %16.12f" \
           #        %(self.position[j,0],self.position[j,1],self.position[j,2]),
           #print ""
    
        return self.position

    ###############################################
    ## get atomic coordinate position
    ##
    def get_fix(self):

        natom = self.get_natom()
        selective = self.get_selective()
       #self.fix = np.zeros((natom,3),dtype='S2')
        self.fix = np.zeros((natom,3),dtype='S')

        if selective:
            VASP = self.get_vasp_version()
            if VASP == 4:
                i = 5+1
            else:
                i = 6+1

            i += 2
            for j in range(natom):
                xyz = self.datlines[i+j].split()
                self.fix[j,0] =str(xyz[3])
                self.fix[j,1] =str(xyz[4])
                self.fix[j,2] =str(xyz[5])

        return self.fix


    ###############################################
    # 基本並進ベクトルを、alpha, beta, gamma で回す
    # VASP 表記とは転置した形で t ベクトルに入っているの注意
    # 注意) むしろ VASP 表記が転置している
    # ここでは転置したまま,正しい基本並進ベクトルのまま処理をする
    def conv_rot_euler(self,alpha,beta,gamma):

        R = SAE.rotate_euler(alpha,beta,gamma)

        # 基本並進ベクトルの変換
        t = self.get_t()

        t1 = np.matrix( [ t[0,0],t[0,1],t[0,2] ] )
        t1r = t1 * R

        t2 = np.matrix( [ t[1,0],t[1,1],t[1,2] ] )
        t2r = t2 * R

        t3 = np.matrix( [ t[2,0],t[2,1],t[2,2] ] )
        t3r = t3 * R

        # オイラー角で基本並進ベクトルを回したときの基本並進ベクトル
        R_t = np.matrix([
                [ t1r[0,0],t1r[0,1],t1r[0,2] ],
                [ t2r[0,0],t2r[0,1],t2r[0,2] ],
                [ t3r[0,0],t3r[0,1],t3r[0,2] ]
                ])


        # 内部座標の変換
        position = self.get_position()
        natom = self.get_natom()
        R_position = np.zeros((natom,3))
        for j in range(natom):
            p  = np.matrix( [position[j,0],position[j,1],position[j,2]] )
            pr = p * R
            R_position[j,0] =pr[0,0]
            R_position[j,1] =pr[0,1]
            R_position[j,2] =pr[0,2]

        return R_t,R_position


################################################################################
if __name__ == '__main__':

    name = 'POSCAR'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input',
                        dest='INPUT',
                        default=name,
                        )
    options, args = parser.parse_args()
    name = options.INPUT

    poscar = ReadPoscar(name)

    title = poscar.get_title()
    scale = poscar.get_scale()
    t = poscar.get_t()
    vasp = poscar.get_vasp_version()
    nion = poscar.get_nion()
    atoms = poscar.get_atoms()
    atoms_index = poscar.get_atoms_index()
    natom = poscar.get_natom()
    selective = poscar.get_selective()
    direct = poscar.get_selective()
    position = poscar.get_position()
    fix = poscar.get_fix()

    ion = poscar.get_ion()
    ion_local = poscar.get_ion_local()
    atoms_index_j = poscar.get_atoms_index_j()

#   for i in range(natom):
#       print i, atoms_index_j[i]

    ############################################################################
    out = sys.stdout
    print >> out, title
    print >> out, " ",scale
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,0],t[1,0],t[2,0])              
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,1],t[1,1],t[2,1])              
    print >> out, "  %13.9f %13.9f %13.9f" %(t[0,2],t[1,2],t[2,2])    

    if vasp >= 5:
        print >> out, " ",
        for i in range(nion):
            print >> out,atoms_index[i],
        print >> out, " "

    print >> out, " ",
    for i in range(nion):
        print >> out, atoms[i],
    print >> out, " "

    if selective:
        print >> out, "Selective Dynamics"
    if direct:
        print >> out, "Direct"
    else:
        print >> out, "Cartesian"

    for j in range(natom):
        print >> out, " %13.9f %13.9f %13.9f" \
                %(position[j,0], position[j,1], position[j,2]),
        if selective:
            print >> out, "",
            print >> out, fix[j,0],fix[i,1],fix[i,2],
        print >> out, ""
    ############################################################################

#   print ion
#   print ion_local

