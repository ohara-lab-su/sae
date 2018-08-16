#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム+アニメーション
#  VplotCrystalMD.py
#
################################################################################
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
#
# 2014.11.21
#   bond と原子の色と大きさの自動対応
#
# 2014.11.21
#   まともに動いていなかったのを、取りあえず動くように
#
# 2014.11.18
#   xyz(MD)形式ファイルを読み込んでプロットする形に VplotCrystal.py を改変
#   改変というよりは簡略化
#
# 2014.11.16 1st (VplotCrystal.py)
#    vpython,wxpython 利用
#
################################################################################
from __future__ import print_function
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

import sys
import os
from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import numpy as np
import visual as vp

from crystal_make_unit import *

#import re
#import optparse
#import wx


################################################################################
if __name__ == '__main__':

    ############################################
#   app = wx.App(True,None)
#   frame0 = wx.Frame(None,-1,'Plot_Crystal')
#   frame0.Show()

    ###########################################
    cname = 'igzo_coll'
    ###########################################

    print "INPUT file name   :",cname

    ############################################
    # ボンドを描くか否か？
    bond_FLAG = True
    atom1 = 1
    atom2 = 4
    distance = 2.4

    # Default & OptionParser
#   cname = options()
    ############################################

    ############################################
    # *_coll.cfg (RMC_POT) ファイル読み込み準備
    #
    nloop,natom,nion = SAE.read_cfg_coll_param(cname)

    ############################################
    # *_coll.cfg (RMC_POT) ファイル読み込み準備
    #
    t             = np.zeros((3,3),dtype=float) # 基本並進ベクトル
    atoms         = np.zeros((nion),dtype=int)  # 原子種毎の原子の数の保存
    ion_site      = np.zeros((natom),dtype=int) # 原子の通し番号に対してのサイト番号の保存
    position_loop = np.zeros((nloop,natom,3))   # 原子位置(loop,全原子のインデックス)

    ############################################
    # *_coll.cfg (RMC_POT) ファイル読み込み
    #
    header,comment,scale,direct = \
            SAE.read_cfg_coll(cname,nloop,t,natom,nion,atoms,ion_site,position_loop)


    ############################################
    # atoms_index のダミー作成
    #
    #   *.cfg 形式は原子種の情報が存在しないので、
    #   dummy の atoms list を読み込んで、原子種の情報を配列に放り込む
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


    ############################################################################
    # 結晶描画の基礎プログラム

    # 複数のオブジェクトをまとめるためにフレームを作る
    f  = vp.frame()

    # 結晶描画の単位胞の座標原点
    O = [ -3,-3,0 ]
    RC = 0.03
    C = [ 255,255,2555 ] # white


    RATIO=0.3

    t0      = deepcopy(t)
    scale0  = scale
    direct0 = direct

    for loop in range(nloop):

        ########################################################################
        # loop 毎の座標変換
        #
        #   CFG形式に変換するときに t行列を倍にしているので、LOOP の度にt行列を
        #   毎回変換すると基本並進ベクトルがどんどん大きくなるので注意
        #   座標系は loop の度に loop 毎の座標系を呼び出すので問題はない
        #
        t        = deepcopy(t0)
        scale    = scale0
        direct   = direct0
        position = np.zeros((natom,3))

        for i in range(natom):
            # loop毎の位置座標をローカルに代入(アホ)
            position[i,0] = position_loop[loop,i,0]
            position[i,1] = position_loop[loop,i,1]
            position[i,2] = position_loop[loop,i,2]

        ############################################
        # *.cfg 形式を VASP形式(=通常の基本並進+内部座標形式)へ変換 ( by loop)
        #
        scale,direct = SAE.conv_cfg2vaspa(scale,t,natom,direct,position) # 引数版

        ############################################
        # Direc to Cartesian 変換 (RMC_POT *.cfg は Direct形式) (by loop)
        # 引数版
        #
        if direct:
            ABS = False
            scale,direct = \
                    SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

        ############################################
        # 絶対座標系へ変換 ( cartesian --> cartesian and scale=1.0 ) ( by loop)
        # 引数版
        #
        scale = SAE.conv_car2carABSa(scale,t,natom,direct,position)

       #print "==========LOOP: "+str(loop)
       #print t[0,0], t[1,0], t[2,0]
       #print t[0,1], t[1,1], t[2,1]
       #print t[0,2], t[1,2], t[2,2]
       #for ion in range(natom):
       #    print " %2d %2d  %20.11f %20.11f %20.11f" \
       #            % (loop,ion, position[ion,0], position[ion,1], position[ion,2])


        ############################################
        # bond 情報の取得
        #
        if bond_FLAG:

            bondnum = \
                    SAE.get_bond_info_param(atom1,atom2,distance,nion,atoms,position)
           #print "NUMBER OF BOND     :",bondnum

            bondr = np.zeros((bondnum))
            bond1 = np.zeros((bondnum),dtype=int)
            bond2 = np.zeros((bondnum),dtype=int)

            SAE.get_bond_info(atom1,atom2,distance,nion,\
                              atoms,atoms_index,position,bondr,bond1,bond2)


        ########################################################################

        # 単位胞の描画ルーチン
        if loop == 0 :
            crystal_make_unit(t,O,RC,C)

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


        # bond の描画
        if bond_FLAG:

            BR = 0.08 # ボンドの太さ
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

                bond = vp.cylinder (frame=f, pos=(x0,y0,z0), \
                                    axis=(x12,y12,z12), radius =BR )

#                   print num, bond1[num],"("+str(ion_site[num])+") -",\
#                              bond2[num],"("+str(ion_site[num])+")"  ,\
#                              " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
#                              % ( r1, x1,y1,z1, x2,y2,z2)

        # アニメーション速度の設定(loop 内のatomの描画が終わったらアニメ)
        vp.rate(5)
        # 描画が終わったら前回の画像をクリア(これをしないとアニメが残像になる)
        for obj in f.objects:
            obj.visible=0

################################################################################

