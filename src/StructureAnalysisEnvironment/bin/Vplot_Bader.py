#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_Bader.py の電荷数描画プログラム
#
#  デフォルトではChargeの変化量（絶対値）変化を示す。
#  モードを変えて(-cオプション) で Charge の正負で色の濃淡モードに変更
#
# 基本的にコマンドラインオプションで制御。
# GUI は表示だけ
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.07.08
#  CrystalMaker クラスを分離
#
# 2015.07.08
#   スーパーセル表示対応
#
# 2015.07.06 1st
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

import StructureAnalysisEnvironment as SAE
import StructureAnalysisEnvironment.gui as SAEG
#import SpaceGroupEnvironment as SGE

#from crystal_make_unit import *

#import numpy as np
#import visual as vp
import wx # wxpython-3.x0 までは python2 専用なので注意 (python3 対応は wxpython4.0)
#import time

#import Image
#import ImageGrab

import os
#import re
import optparse
#from copy import deepcopy

################################################################################
def options():

    inpname = 'POSCAR'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-b','--bond',action='store_true',default=False)
    parser.add_option( '-l','--log',action='store_true',default=False)
    parser.add_option( '-c','--charge',action='store_true',default=False)
    parser.add_option( '-n','--noncell',action='store_true',default=False)
    parser.add_option( '--cmax',)
    parser.add_option( '--cmin',)
    options, args = parser.parse_args()

    if options.INPUT: inpname = options.INPUT

    if not os.path.exists(inpname):
        inpname0 = 'CONTCAR'
        if not os.path.exists(inpname0):
            sys.exit("STOP: "+inpname+" and "+inpname0+" file not found")
        else:
            inpname = inpname0


    if len(args) < 3:
        super_x = 1
        super_y = 1
        super_z = 1
    else:
        super_x = int(args[0])
        super_y = int(args[1])
        super_z = int(args[2])
       #print "Super Cell         : [",super_x,",",super_y,",",super_z,"]"
        print("Super Cell         : [%s, %s, %s]" % (str(super_x), str(super_y), str(super_z)))

    return inpname,\
            options.bond,\
            options.log,\
            options.charge,\
            options.noncell,\
            options.cmax,options.cmin,\
            super_x,super_y,super_z

################################################################################
if __name__ == '__main__':

    #####################################
    # オプション処理
    #
    readfile,OPT_BOND,OPT_LOG,OPT_CHARGE,OPT_CELL,CMAX,CMIN,\
            super_x,super_y,super_z = options()


    #####################################
    # wxPython の基本インスタンスの生成
    #
#   app = wx.App(True,None)
    app = wx.PySimpleApp()


    #####################################
    # 入出力&モード確認
    #
    print("INPUT file name    : %s" % str(readfile))
    print("plot BOND Mode     : %s" % str(OPT_BOND))
    print("plot without cell  : %s" % str(OPT_CELL))
    if OPT_CHARGE:
        print("plot charge        : charge")
    else:
        print("plot charge        : ABS(charge)")
    if CMAX: print("charge MAX         : %s" % str(CMAX))
    if CMIN: print("charge MIN         : %s" % str(CMIN))
    print("-----------------------------------")


    #####################################
    # POSCAR/CONTCAR 読み込み
    #
    poscar = SAE.io.ReadVaspPoscar(readfile)
    potcar = SAE.io.ReadVaspPotcar()
    acf = SAE.io.ReadVaspAcf(poscar=poscar,potcar=potcar)


    #####################################
    # 結晶描画フレーム(vpython)インスタンス作成
    #
    crystal = SAEG.CrystalMaker(poscar,origin=[-0.5,-0.5,0],\
            times=[super_x,super_y,super_z])

    #####################################
    # 描画メッソド
    #
    crystal.plot_atoms()
    if OPT_CHARGE:     crystal.plot_bader(acf,mode='CHARGE',cmax=CMAX,cmin=CMIN)
    if not OPT_CHARGE: crystal.plot_bader(acf,cmax=CMAX,cmin=CMIN)
    if OPT_BOND:       crystal.plot_bonds()
    if not OPT_CELL:   crystal.plot_unit_cell()


#   time.sleep(1)
#   os.system("screencapture screen.png")
#   app.MainLoop()
