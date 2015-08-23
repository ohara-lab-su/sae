#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Rmove.py がベース
#   基板となる構造入力ファイルは POSCAR 形式
#   LIST に記述した通し番号の原子を動かして新しい *.cfg ファイルを出力する
#
#   原子の移動は z 軸方向で、移動リストはソース中に z_list で記述する
#   汎用性はほぼゼロ
#
#   0) z_list
#      ソース中に記述する原子の移動量(c軸方向)
#
#   1) LIST_bottom  移動原子一覧読み込み( Vextract0.py で事前作成 )
#      LIST_top     移動原子一覧読み込み( Vextract0.py で事前作成 )
#
#   2) 読み込んだ原子の c 軸方向を一定に変化させて *.cfg ファイルを連続出力
#      bottom と top の移動方向の(符号の)違いはソース中に記述
#
# *) !!!!注意!!!!
#
#       LIST_TOP * -1.0* z_list
#       上方向に正に動かすと中心方向へ移動する
#
#
# *) LIST.ext は複数読み込む(メインルーチン中の処理)
#    bottom layer と top layer 用。
#    bottom と top の連携的な動作（距離を詰める、距離を離す)を一気に指定出来る用に
#
#
################################################################################
#
# 2015.02.27
#  conv_direct2car --> conv_direct2car0
#
# 2014.11.25
#  問題が判明。負の値をz_new に与えるとなんだか挙動が変？
#  値が大きすぎると反対側に原子が抜けるだけ・・・っぽい。
#
# 2014.11.25
#   細かい修正(Direct,Car周り)を何度かしていたので、
#   念のための再動作テスト(0.0 と 0.1 動かしてみて、入力が ang として機能しているかのテスト)
#
# 2014.11.13           基板となるツール
#  Rmove1.py     <--- Vextract0.py
#                <--- Rmove.py
#
# 2014.11.05 1st
#   Rmove.py
#        <--- 基本ベースは VmodifyAtomPosition.py (2014.11.05 version)
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

import sys
import os
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy

################################################################################
def options():

    ###############################################
    ## default parameter
    ##
#   cname  = "POSCAR" # OUTPUT BASE filename
    cname  = "igzo"   # OUTPUT BASE filename
    POSCAR = "POSCAR" # INPUT (BASE) filename

    ###############################################
    ## optparse
    ##
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=POSCAR,
    )
    parser.add_option(  '-o','--output',
                        dest='OUTPUT',
                        default=cname,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        POSCAR=options.INPUT

    if options.OUTPUT:
        cname=options.OUTPUT

    #print args,options
    if len(args) > 0:
        #print "script name:",argvs[0]
        cname=args[0]
        POSCAR=args[0]

    if not os.path.exists(POSCAR):
        sys.exit(POSCAR+" file not found")

    if POSCAR:
        print "INPUT file name :",POSCAR

    if cname:
        print "OUTPUT file name:",cname+".cfg"

    return [POSCAR,cname]


################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname = options()

    # POSCAR の事前読み込み
    nion,natom,VASP = SAE.read_poscar_param(POSCAR)

    # POSCAR 読み込みのための準備
    t           = np.zeros((3,3))
    atoms       = []
    atoms_index = []
    ion         = np.zeros(natom)
    ion_local   = np.zeros(natom)
    position    = np.zeros((natom,3))
    fix         = np.zeros((natom,3),dtype='S')

    # POSCAR の読み込み
    title,scale,selective,direct = \
       SAE.read_poscar(POSCAR,VASP,t,atoms,atoms_index,ion,ion_local,position,fix)

    ##########################################################################

#   z_list = [ 0.5, 0.4, 0.0 ]
    z_list = [ 0.0, 0.1 ]
#   z_list = [ 0.1 ]
#   z_list = [ 0.1, 0.2, 0.3, 0.4, 0.5 ]
#   z_list = [ -0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5 ]
#   z_list = [ 0.5, 0.4, 0.3, 0.2, 0.1 ]
#   z_list = [  0.500,
#               0.475,
#               0.450,
#               0.425,
#               0.400,
#               0.375,
#               0.350,
#               0.325,
#               0.300,
#               0.275,
#               0.250,
#               0.225,
#               0.200,
#               0.175,
#               0.150,
#               0.125,
#               0.100,
#               0.000,
#              -0.025,
#              -0.050,
#              -0.075,
#              -0.100,
#              -0.125,
#              -0.150,
#              -0.175,
#              -0.200, ]

    # 移動原子リスト読み込み :一次元情報（原子の通し番号）のみリード
    # 準備(コメントも含めた配列サイズ)
    name='LIST'
    nlist_top    = SAE.read_list_param(name+'_top.ext')
    nlist_bottom = SAE.read_list_param(name+'_bottom.ext')

    list_atoms_top    = np.zeros((nlist_top))
    list_atoms_bottom = np.zeros((nlist_bottom))

    # 実際のデータ読み込み(コメントをスキップした配列サイズ)
    nlist_top    = SAE.read_list1(name+'_top.ext',list_atoms_top)
    nlist_bottom = SAE.read_list1(name+'_bottom.ext',list_atoms_bottom)
    nlist        = nlist_top + nlist_bottom


    ### C軸の移動パラメーター毎のループ ######
    n_z_list = len(z_list)
    ##########################################
    for i in range(n_z_list):

        z_new = z_list[i]
        print "z_new: ",z_new

        ## bottom と top のデーター結合
        list_atoms = np.zeros((nlist,4))
        for i in range(nlist_top):
            list_atoms[i,0] = int(list_atoms_top[i])
            list_atoms[i,1] = 0.0
            list_atoms[i,2] = 0.0
            ############################
            list_atoms[i,3] = -1.0*z_new  # センターに近づける
            ############################

        # 実際に処理したLIST情報のリスト化
        znew = open(name+'_top_z'+str(z_new)+'.list','w')
        for i in range(nlist_top):
            print >> znew, "%3s %14.11f %14.11f %14.11f" \
                            % ( int(list_atoms[i,0]), \
                                    list_atoms[i,1], \
                                    list_atoms[i,2], \
                                    list_atoms[i,3] )
        znew.close()

        for i in range(nlist_bottom):
            list_atoms[i+nlist_top,0] = int(list_atoms_bottom[i])
            list_atoms[i+nlist_top,1] = 0.0
            list_atoms[i+nlist_top,2] = 0.0
            ############################
            list_atoms[i+nlist_top,3] = 1.0*z_new  # センターに近づける
            ############################

        # 実際に処理したLIST情報のリスト化
        znew = open(name+'_bottom_z'+str(z_new)+'.list','w')
        for i in range(nlist_bottom):
            print >> znew, "%3s %14.11f %14.11f %14.11f" \
                            % ( int(list_atoms[i+nlist_top,0]), \
                                    list_atoms[i+nlist_top,1], \
                                    list_atoms[i+nlist_top,2], \
                                    list_atoms[i+nlist_top,3] )
        znew.close()

#       for i in range(nlist):
#           print "%2i %14.11f %14.11f %14.11f " \
#                  % ( int(list_atom[i,0]), list_atom[i,1], list_atom[i,2], list_atom[i,3])

        # Direct to Cartesian
        if direct:
            ABS=False # for VASP
            scale,direct = SAE.conv_direct2cara(ABS,scale,t,natom,direct,position)

        # スケールファクターを 1.0 へ変換
        scale = SAE.conv_scale21a(scale,t)

        # 原子移動(ang) 必要:cartesian-mode
        #    入力list_atom: cartesian-実座標系(ang)
        #        position : cartesian-内部座標系
        #    内部でスケールし直すのでスケールファクターはなんでも良い
        SAE.move_atoms1(scale,t,direct,position,nlist,list_atoms)


        ########################################################################

        # Cartesian to Direct
        if not direct:
            scale,direct = SAE.conv_car2directa(scale,t,natom,direct,position)

    #   # POSCAR のファイル標準出力
    #   STD=False
    #   print_poscar(POSCAR,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)

        # RMC_POT(cfg) 形式への変換 必須:direct-Mode
        scale,direct = SAE.conv_vasp2cfg(scale,t,natom,direct,position)

        outname=str(cname)+'_z'+str(z_new)

        # RMC_POT(cfg) 形式への出力
        STD=False
       #STD=True
        SAE.print_cfg(outname,STD,title,t,natom,nion,atoms,position)


        ########################################################################

        # RMC_POT (*.cfg) 形式から VASP 形式へ変換
        direct = True   # conv_cfg2vasp は direce を想定(in/out)
        scale   = 1.0   # conv_cfg2vasp は scale 1.0 を想定
        scale,direct = SAE.conv_cfg2vaspa(scale,t,natom,direct,position) #引数版

        # 擬似VASP5 設定
        dummy   = "In Ga Zn O"
        PV5FLAG = True  # 擬似VASP5 出力

        # VASP4+擬似VASP5 出力
       #print ""
        STD=False
       #STD=True
        SAE.print_poscar4(outname,STD,title,scale,natom,nion,\
                          direct,PV5FLAG,t,atoms,dummy,position)


    ############################################################################

