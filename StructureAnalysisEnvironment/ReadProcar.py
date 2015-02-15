#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# ReadProcar.py
#
#  PROCAR 読み込みクラス
#    Vcom11.pl にほぼ対応する。LORIBT=11 しか考慮してない
#
################################################################################
#
#  s, p_y, p_z, p_x, d_xy, d_yz, d_z2-r2, d_xz, d_x2-y2,                       
#  i.e. (l,-m, ..... l,0, ..... l,+m)                                          
#                                                                              
#           1:s                                                                
#                                                                              
#           2:p_y                                                              
#           3:p_z                                                              
#           4:p_x                                                              
#                                                                              
#           5:d_xy                                                             
#           6:d_yz                                                             
#           7:d_3z2-r2                                                         
#           8:d_xz                                                             
#           9:d-x2-y2                                                          
#                                                                              
#  t2g: 5,6,8
#
################################################################################
#
# 2015.01.29
#   固有値の最大と最小をゲットするmethodを実装
#   一度 get_pro_all を読んでから処理するアホ(低速)処理仕様
#      def get_max_eigenval()  (ReadEigenval.get_max_eigenval() と同様仕様
#      return [eigen_min,eigen_max]
#
# 2015.01.29 startup
#   K点が固定フォーマットで、スペース無しでつながるケースを発見
#   固定フォーマット版へ修正。
#
#   get_pro_all(self)  LORBIT の応じてすべての情報を返す
#   get_pro_spd(self)  LORBIT=10 相当の情報を返す
#
# 2015.01.29 startup
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
import re
import optparse
import numpy as np

#from copy import deepcopy

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadProcar(object):

    def __init__(self,name):

        if os.path.exists(name):
            GZIP=False
        elif os.path.exists(name+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+name+" or "+name+".gz file not found")
    
        try:
            if GZIP:
                tmp = gzip.open(name+".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+name+" or "+name+".gz does'nt open")
        finally:
            tmp.close()
    
        self.datlines = datfile.split('\n')
        self.num = len(self.datlines)

    # PROCAR の k-point 1 のband 1 の OCC が 1 or 2 を確認
    # NCM のときはもっと注意して実装し直す必要がある
    def get_ispin(self):
        band_reg = re.compile('^band')
        for i in range(self.num):                                               
            if bool(band_reg.match(self.datlines[i])): 
                if 'occ.' ==self.datlines[i].split()[6]:
                    occ = float(self.datlines[i].split()[7])
                    if occ > 1.0:
                        self.ISPIN = 1
                    else:
                        self.ISPIN = 2
                break
        return self.ISPIN

    def get_nkpts(self):
        self.NKPTS = 0
        if 'k-points:' == str(self.datlines[1].split()[2]):
            self.NKPTS = int(self.datlines[1].split()[3])
        return self.NKPTS

    def get_nbands(self):
        self.NBANDS = 0
        if 'bands:' == str(self.datlines[1].split()[6]):
            self.NBANDS = int(self.datlines[1].split()[7])
        return self.NBANDS

    # NATOM: VASP 内部(表記) では ions に相当
    def get_natom(self):
        self.NKPTS = 0
        if 'k-points:' == str(self.datlines[1].split()[2]):
            if 'ions:' == str(self.datlines[1].split()[10]):
                self.NATOM = int(self.datlines[1].split()[11])
        return self.NATOM
    
    def get_lorbit(self):
        ion_reg = re.compile('^ion')
        for i in range(self.num):                                               
            if bool(ion_reg.match(self.datlines[i])): 
                if len(self.datlines[i].split()) > 10:
                    self.LORBIT = 11
                else:
                    self.LORBIT = 10
                break
        return self.LORBIT

    ############################################################################
    # PROCAR の情報をまるごと配列で返す(系によっては目盛をモリモリ食うので注意)
    def get_pro_all(self):

        NSPIN = self.get_ispin()
        NKPTS = self.get_nkpts()
        NBANDS = self.get_nbands()
        NATOM = self.get_natom()

        LORBIT = self.get_lorbit()
        if LORBIT > 10:
            LMMAX = 9
        else:
            LMMAX= 3

        kp = np.zeros((NKPTS,4))
        eig = np.zeros((NBANDS,NKPTS,NSPIN))
        occ = np.zeros((NBANDS,NKPTS,NSPIN))
        if NATOM > 1:
            pro = np.zeros((LMMAX+1,NATOM+1,NBANDS,NKPTS,NSPIN))
            pro_ratio = np.zeros((LMMAX+1,NATOM+1,NBANDS,NKPTS,NSPIN))
        else:
            pro = np.zeros((LMMAX+1,NATOM,NBANDS,NKPTS,NSPIN))
            pro_ratio = np.zeros((LMMAX+1,NATOM,NBANDS,NKPTS,NSPIN))

        j=2
        for s in range(NSPIN):
            if s == 1:
                j += 1
            for k in range(NKPTS):
                j += 1
               #print j+1,"  :",self.datlines[j]  # K-point
               #kp[k,0] = float(self.datlines[j].split()[3])  # kx
               #kp[k,1] = float(self.datlines[j].split()[4])  # ky
               #kp[k,2] = float(self.datlines[j].split()[5])  # kx
               #kp[k,3] = float(self.datlines[j].split()[8])  # w
                kp[k,0] = float(self.datlines[j][18:29]) # kx
                kp[k,1] = float(self.datlines[j][29:40]) # ky
                kp[k,2] = float(self.datlines[j][40:51]) # kz
                kp[k,3] = float(self.datlines[j][64:75]) # kz
                j += 1
                for i in range(NBANDS):
                    j += 1
                   #print j+1,"  :",self.datlines[j]  # band_energy
                    eig[i,k,s] = float(self.datlines[j].split()[4]) # eig
                    occ[i,k,s] = float(self.datlines[j].split()[7]) # occ
                    j += 2
                    for a in range(NATOM):
                        j +=1
                       #print j+1,"  :",self.datlines[j]
                        if LORBIT > 10:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # py
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # pz
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # px
                            pro[4,a,i,k,s] = float(self.datlines[j].split()[5]) # dxy
                            pro[5,a,i,k,s] = float(self.datlines[j].split()[6]) # dyz
                            pro[6,a,i,k,s] = float(self.datlines[j].split()[7]) # dz2
                            pro[7,a,i,k,s] = float(self.datlines[j].split()[8]) # dxz
                            pro[8,a,i,k,s] = float(self.datlines[j].split()[9]) # dx2
                            pro[9,a,i,k,s] = float(self.datlines[j].split()[10]) # tot
                            
                        else:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # p
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # d
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # tot
                       ##################
                       #den = 0.0
                       #for m in range(LMMAX): # 全成分を足しあわせてその合計を 1 とみなす
                       #    den = pro[m,a,i,k,s] + den
                       #   #print s,i,a,m,den
                       #for m in range(LMMAX):
                       #    pro_ratio[m,a,i,k,s] = pro[m,a,i,k,s]/den
                       ##################

                    if NATOM > 1: # total
                        j += 1
                        a += 1
                       #print j+1,"  :",self.datlines[j]
                        if LORBIT > 10:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # py
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # pz
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # px
                            pro[4,a,i,k,s] = float(self.datlines[j].split()[5]) # dxy
                            pro[5,a,i,k,s] = float(self.datlines[j].split()[6]) # dyz
                            pro[6,a,i,k,s] = float(self.datlines[j].split()[7]) # dz2
                            pro[7,a,i,k,s] = float(self.datlines[j].split()[8]) # dxz
                            pro[8,a,i,k,s] = float(self.datlines[j].split()[9]) # dx2
                            pro[9,a,i,k,s] = float(self.datlines[j].split()[10]) # tot
                        else:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # p
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # d
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # tot
                       ##################
                       #den = 0.0
                       #for m in range(LMMAX): # 全成分を足しあわせてその合計を 1 とみなす
                       #    den = pro[m,a,i,k,s] + den
                       #   #print s,i,a,m,den
                       #for m in range(LMMAX):
                       #    pro_ratio[m,a,i,k,s] = pro[m,a,i,k,s]/den
                       ##################

                    j += 1
                j += 1

        return [kp,eig,occ,pro,pro_ratio]


    ############################################################################
    # PROCAR の情報をまるごと配列で返す
    # LORBIT=11 のときでも LORBIT=10 相当の情報を返す
    def get_pro_spd(self):

        NSPIN = self.get_ispin()
        NKPTS = self.get_nkpts()
        NBANDS = self.get_nbands()
        NATOM = self.get_natom()
        LORBIT = self.get_lorbit()

        LMMAX= 3

        kp = np.zeros((NKPTS,4))
        eig = np.zeros((NBANDS,NKPTS,NSPIN))
        occ = np.zeros((NBANDS,NKPTS,NSPIN))
        if NATOM > 1:
            pro = np.zeros((LMMAX+1,NATOM+1,NBANDS,NKPTS,NSPIN))
            pro_ratio = np.zeros((LMMAX+1,NATOM+1,NBANDS,NKPTS,NSPIN))
        else:
            pro = np.zeros((LMMAX+1,NATOM,NBANDS,NKPTS,NSPIN))
            pro_ratio = np.zeros((LMMAX+1,NATOM,NBANDS,NKPTS,NSPIN))

        j=2
        for s in range(NSPIN):
            if s == 1:
                j += 1
            for k in range(NKPTS):
                j += 1
               #print j+1,"  :",self.datlines[j]  # K-point
                kp[k,0] = float(self.datlines[j][18:29]) # kx
                kp[k,1] = float(self.datlines[j][29:40]) # ky
                kp[k,2] = float(self.datlines[j][40:51]) # kz
                kp[k,3] = float(self.datlines[j][64:75]) # kz
                j += 1
                for i in range(NBANDS):
                    j += 1
                   #print j+1,"  :",self.datlines[j]  # band_energy
                    eig[i,k,s] = float(self.datlines[j].split()[4]) # eig
                    occ[i,k,s] = float(self.datlines[j].split()[7]) # occ
                    j += 2
                    for a in range(NATOM):
                        j +=1
                       #print j+1,"  :",self.datlines[j]
                        if LORBIT > 10:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1])
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2])+\
                                            +float(self.datlines[j].split()[3])+\
                                            +float(self.datlines[j].split()[4])
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[5])+\
                                            +float(self.datlines[j].split()[6])+\
                                            +float(self.datlines[j].split()[7])+\
                                            +float(self.datlines[j].split()[8])+\
                                            +float(self.datlines[j].split()[9])
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[10]) # tot
                        else:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # p
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # d
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # tot
                       ##################
                       #den = 0.0
                       #for m in range(LMMAX): # 全成分を足しあわせてその合計を 1 とみなす
                       #    den = pro[m,a,i,k,s] + den
                       #   #print s,i,a,m,den
                       #for m in range(LMMAX):
                       #    pro_ratio[m,a,i,k,s] = pro[m,a,i,k,s]/den
                       ##################
 
                    if NATOM > 1: # total
                        j += 1
                        a += 1
                       #print j+1,"  :",self.datlines[j]
                        if LORBIT > 10:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1])
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2])+\
                                            +float(self.datlines[j].split()[3])+\
                                            +float(self.datlines[j].split()[4])
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[5])+\
                                            +float(self.datlines[j].split()[6])+\
                                            +float(self.datlines[j].split()[7])+\
                                            +float(self.datlines[j].split()[8])+\
                                            +float(self.datlines[j].split()[9])
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[10])
                        else:
                            pro[0,a,i,k,s] = float(self.datlines[j].split()[1]) # s
                            pro[1,a,i,k,s] = float(self.datlines[j].split()[2]) # p
                            pro[2,a,i,k,s] = float(self.datlines[j].split()[3]) # d
                            pro[3,a,i,k,s] = float(self.datlines[j].split()[4]) # tot
                       ##################
                       #den = 0.0
                       #for m in range(LMMAX): # 全成分を足しあわせてその合計を 1 とみなす
                       #    den = pro[m,a,i,k,s] + den
                       #   #print s,i,a,m,den
                       #for m in range(LMMAX):
                       #    pro_ratio[m,a,i,k,s] = pro[m,a,i,k,s]/den
                       ##################
                    j += 1
                j += 1

        return [kp,eig,occ,pro,pro_ratio]

    # 全バンドの中から最大の固有値と最小を探す
    def get_max_eigenval(self):
        NSPIN = self.get_ispin()
        NBANDS = self.get_nbands()
        NKPTS = self.get_nkpts()

        kp,eig,occ,pro,pro_ratio = self.get_pro_all() ## ReadEigenval 版と異なる部分
        all_eigen_list = np.zeros((NSPIN*NBANDS*NKPTS))
        i = 0
        for ispin in range(NSPIN):
            for j in range(NBANDS):
                for k in range(NKPTS):
                    all_eigen_list[i] = eig[j,k,ispin]
                    i += 1

        eigen_max = max(all_eigen_list)
        eigen_min = min(all_eigen_list)

        return [eigen_min,eigen_max]

################################################################################
if __name__ == '__main__':

    name = 'PROCAR'
                                                                                
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

    procar = ReadProcar(name)
    NSPIN = procar.get_ispin()
    NKPTS = procar.get_nkpts()
    NBANDS = procar.get_nbands()
    NATOM = procar.get_natom()
    LORBIT = procar.get_lorbit()
    if LORBIT > 10 :
        lmmax = 9
    else:
        lmmax = 3

    print "NSPIN :", NSPIN
    print "NKPTS :", NKPTS
    print "NBANDS:", NBANDS
    print "NATOM :", NATOM
    print "LORBIT:", LORBIT

    pro_all = procar.get_pro_all()
    kp,eig,occ,pro,pro_ratio = pro_all

    for spin in range(NSPIN):
        for k in range(NKPTS):
            print "k-point %d   %12.8f %12.8f %12.8f  w= %12.8f" \
                    % ( k+1, kp[k,0], kp[k,1], kp[k,2], kp[k,3])
            for i in range(NBANDS):
                print "band %d  %12.8f" % ( i+1, eig[i,k,spin] )
                for atom in range(NATOM):
                    for lm in range(lmmax+1):
                        print " %5.3f" % ( pro[lm,atom,i,k,spin] ),
                       #print " %5.3f" % ( pro_ratio[lm,atom,i,k,spin] ),
                    print ""
                if NATOM > 1:
                    for lm in range(lmmax+1):
                        print " %5.3f" % ( pro[lm,NATOM,i,k,spin] ),
                       #print " %5.3f" % ( pro_ratio[lm,NATOM,i,k,spin] ),
                    print ""

    print ""
    eigen_max,eigen_min = procar.get_max_eigenval()
    print eigen_max,eigen_min


