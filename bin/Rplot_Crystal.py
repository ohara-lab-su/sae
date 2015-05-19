#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム+アニメーション
#  RplotCrystal.py
#
#     RMC_POT (*.cfg) 形式を入力とする、変換なしの直接描画ソフト
#  
################################################################################
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
#
# 2014.11.21
#   (1) dummy の atom 情報ファイルによる 原子の色と半径情報取得の自動化
#   (2) bond 情報の描画コード(VplotCrystalと同等のもの)
#
# 2014.11.18
#   VplotCrystal.py の簡略バージョンを元に、RplotCrystal.py の基本を作成
#   RMC_POT (*.cfg) 形式対応
#
# 2014.11.18
#   xyz(MD)形式ファイルを読み込んでプロットする形に VplotCrystal.py を改変
#   改変というよりは簡略化
#
# 2014.11.16 1st (VplotCrystal.py)
#    vpython,wxpython 利用
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
__version__    = "0.0.1"                                                                  
################################################################################

#from __future__ import division

import wx
import sys
import os
import numpy as np
import visual as vp

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 

from  crystal_make_unit import *

#import re
#import optparse
#from copy import deepcopy

#from numpy import *
#from visual import *

#from LIB_vasp.read_cfg_param import *
#from LIB_vasp.read_cfg import *
#from LIB_vasp.conv_direct2car import *
#from LIB_vasp.conv_cfg2vasp import *
#from LIB_vasp.conv_car2carABS import *
#
#from LIB_vasp.get_atomic_radius import *
#from LIB_vasp.get_bond_info import *

#from LIB_vasp.crystal_make_unit import *


################################################################################
if __name__ == '__main__':

    ############################################
    app = wx.App(True,None)
    frame0 = wx.Frame(None,-1,'Plot_Crystal')
    frame0.Show()

    ###########################################
    cname = 'igzo'
    ###########################################

    print "INPUT file name   :",cname

    ############################################
    # ボンドを描くか否か？
    bond_FLAG = True
    atom1 = 1
    atom2 = 4
    distance = 2.4

    # Default & OptionParser
#   POSCAR,cname = options()
    ############################################

    ############################################
    # *.cfg (RMC_POT) ファイル読み込み準備
    #
    natom,nion = SAE.read_cfg_param(cname)

    ############################################
    # *_coll.cfg (RMC_POT) ファイル読み込み準備
    #
    t          = np.zeros((3,3))              # 基本並進ベクトル
    atoms      = np.zeros((nion),dtype=int)   # 原子種毎の原子の数の保存
    ion_site   = np.zeros((natom),dtype=int)  # 原子の通し番号に対してのサイト番号の保存
    position   = np.zeros((natom,3))          # 原子位置(loop,全原子のインデックス)

    ############################################
    # *_coll.cfg (RMC_POT) ファイル読み込み
    #
    header,comment = SAE.read_cfg(cname,t,atoms,ion_site,position)


    ############################################
    # atoms_index のダミー作成
    #
    # *.cfg 形式は原子種の情報が存在しないので、
    # dummy の atoms list を読み込んで、原子種の情報を配列に放り込む
    #
    dummy      = cname+'.atomlist'
    dummy_FLAG = False

    if os.path.exists(dummy):
        dummy_FLAG=True
        print "READ dummy list: "+dummy
        try:
            tmp = open(dummy)
        except:
            sys.exit("STOP: "+dummy+" does'nt open")

        dummyfile = tmp.read()
        tmp.close
        dummylines = dummyfile.split('\n')
        atoms_index = dummylines[0].split()
        nion0 = len(atoms_index)
        if nion0 != nion:
            sys.exit("STOP: nion0 != nion (in dummy list)")

       #for i in range(natom):
       #    print i,ion_site[i], atoms_index[ion_site[i]]


    ############################################
    # RMC_POT (*.cfg) 形式から VASP 形式へ変換
    # 
    #  1) 基本並進を2.0倍して
    #  2)内部座標を0.5倍してから1/2,1/2,1/2並進
    # 
    direct = True   # conv_cfg2vasp は direce を想定(in/out)
    scale   = 1.0   # conv_cfg2vasp は scale 1.0 を想定
    scale,direct = SAE.conv_cfg2vasp(scale,t,natom,direct,position)

    # Direct to Cartesian 変換
    if direct:
        ABS=False
        scale,direct = SAE.conv_direct2car0(ABS,scale,t,natom,direct,position)

    # 絶対座標系へ変換( cartesian and scale=1.0 )
    scale = SAE.conv_car2carABS(scale,t,natom,direct,position)

#   for j in range(natom):
#       print " %14.10f %14.10f %14.10f " \
#             % ( position[j,0],\
#                 position[j,1],\
#                 position[j,2] )


    ############################################
    # bond 情報の取得
    #
    if bond_FLAG:
        bondnum = SAE.get_bond_info_param(atom1,atom2,distance,nion,atoms,position)
        print "NUMBER OF BOND     :",bondnum

        bondr = np.zeros((bondnum))
        bond1 = np.zeros((bondnum),dtype=int)
        bond2 = np.zeros((bondnum),dtype=int)

        SAE.get_bond_info(atom1,atom2,distance,nion,atoms,atoms_index,position,bondr,bond1,bond2)


    ############################################################################
    # 結晶描画の基礎プログラム

    # 複数のオブジェクトをまとめるためにフレームを作る
    f  = vp.frame()

    ############################################
    # 単位胞の描画
    #
    O  = [ -3,-3,0 ] # 結晶描画の単位胞の座標原点
    RC = 0.03
    C  = [ 255,255,2555 ] # white

    # 単位胞の描画ルーチン
    crystal_make_unit(t,O,RC,C)


    ############################################
    # 結晶の描画
    RATIO=0.3

    for i in range(natom):

        # 描画の原点位置修正
        xp = position[i,0] + O[0]
        yp = position[i,1] + O[1]
        zp = position[i,2] + O[2]

        if dummy_FLAG:
            # 原子の種類を取得
            atom_type = atoms_index[int(ion_site[i])]
    
            # 原子半径を取得
            radius = SAE.get_atomic_radius1(atom_type)
            R = radius*RATIO

            # 原子番号を取得
            num = SAE.get_atomic_number1(atom_type)

        else:
            R=0.3
            num=6

        atom = vp.sphere(frame=f,pos=(xp,yp,zp), radius=R)

        # 原子の色設定(RG)を適当に自動化
        atom.red   = 0.5*num*num
        atom.green = 0.1*num
        atom.blue  = 1/num


    ############################################################################
    # bond の描画
    if bond_FLAG:

        # ボンドの太さ
        BR = 0.08

        for num in range(bondnum):

            x1 = position[bond1[num],0]
            y1 = position[bond1[num],1]
            z1 = position[bond1[num],2]

            x2 = position[bond2[num],0]
            y2 = position[bond2[num],1]
            z2 = position[bond2[num],2]

            x12 =  x2 - x1
            y12 =  y2 - y1
            z12 =  z2 - z1

            x0 = x1 +O[0]
            y0 = y1 +O[1]
            z0 = z1 +O[2]

            r1 = bondr[num]

            bond = vp.cylinder (frame=f, pos=(x0,y0,z0), axis=(x12,y12,z12), radius =BR )

            print num, bond1[num],"("+str(ion_site[num])+") -",\
                       bond2[num],"("+str(ion_site[num])+")"  ,\
                       " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
                       % ( r1, x1,y1,z1, x2,y2,z2)


################################################################################
     
