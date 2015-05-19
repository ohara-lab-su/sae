#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VmakeSuperCell2.py
#   引数に与えた倍率での super cell 作成
#   VASP の Direct/Car POSCAR からの入力で動作
#   ほぼ独立的に仕事に使えるスクリプトとなっている
#
#    ---> car モード対応(+微修正) VmakeSuperCell1.py = VmakeSuperCell2.py
#
################################################################################
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
#
# 2014.11.04
#   bag fix
#      conv_car2direct(scale,t,natom,direct,sp) ルーチンにバグ(修正)
#
#  2014.10.31
#   スーパーセル変換関数の準備とそのテスト用で VmakeSuperCell2.py を
#   ベースにしたバージョンへ改変する（分離、関数化、一部高度化)
#
#  2014.10.14 17:00
#   元のセルの通し番号 index で対応している atom の種類を Super Cell
#   から呼び出せる index の作成（の必要性が VfindNN1.py) で出来たので
#   慌てて実装
#
#    元セル通しindex  <--(対応index作成)--> スーパーセル通しindex
#
################################################################################
#
#  2014.10.14 15:15
#    VmakeSuperCell2.py
#    VASP の Car 形式入力も対応
#    初期テスト(VmakeSuperCell0.py) 2x2x1 専用のルーチンの削除
#
#  2014.10.14
#    n x l x m super-cell に関しての一般化
#    VmakeSuperCell1.py
#      引数にファイル名をやめて、引数は n*l*m とした
#
#      原子の順番が変わってしまうバグを修正
#      VmakeSuperCell0.py でも実はバグっていた
#
#      !!!!!!!!!!!!!!!!!!!!! 注意 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#      1*1*1 セルに相当する index は自動で n=0,l=0,m=0
#      となるのだが、原子の種類ごとでソートしなおしているので
#      元のセルの内部座標番号は、新しいスーパーセルでは一般には
#      異なる番号に配置される（注意）
#      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
#
#  2014.10.10  (1st version)
#
#     SuperCell 作成（テスト用）
#     2x2x1 cell 専用 (基本並進はなんでもOKのはず)
#     入力は VASP Direct 形式専用
#     出力は VASP Car 形式(Scale=1.0)
#
#     原子の順番テストはまだしてない(2014.10.10 17:22)
#       同一種ならば間違いなく動作する
#       原子酒が複数あるときは、違う原子種とみなされる可能性が
#       すこしだけある（大丈夫だと思うが、未テスト）
#       ただし、構造は完璧に再現する
#
#       ... ここまで到達するのに結構かかった。
#       アホなミス連発で、アホな勘違い連発で泥沼化した
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
    cname  = "POSCAR" # OUTPUT BASE filename
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
    
    if not os.path.exists(POSCAR):
        if os.path.exists(POSCAR+".vasp"):
            POSCAR="POSCAR.vasp"
        else:
            sys.exit(POSCAR+" file not found")
    
    #print args,options
    if len(args) < 3:
        sys.exit("Error: args < 3")
    else:
        super_x = args[0]
        super_y = args[1]
        super_z = args[2]
        print "Super Cell         : [",super_x,",",super_y,",",super_z,"]"
    
    outname = cname+'_super_'+str(super_x)+'x'+str(super_y)+'x'+str(super_z)
    
    print "INPUT file name    :",POSCAR
    print "OUTPUT file name   :",outname+".vasp"

    return [POSCAR,cname,outname,super_x,super_y,super_z]
    

################################################################################
if __name__ == '__main__':

    # Default & OptionParser
    POSCAR,cname,outname,super_x,super_y,super_z = options()
    super_x = int(super_x)
    super_y = int(super_y)
    super_z = int(super_z)

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

    # Direct to Cartesian
    if direct:
       #ABS=False # for VASP
        ABS=True  # for SuperCell
        scale,direct = SAE.conv_direct2car0(ABS,scale,t,natom,direct,position)

#  ## TEST POSCAR の標準出力
#   STD=True
#   print_poscar(outname,STD,title,scale,natom,nion,selective,direct,VASP,t,atoms,atoms_index,position,fix)

    # supercell_zb 作成準備
    super        = super_x*super_y*super_z
    sv           = np.zeros((super,3))
    sp           = np.zeros((natom*super,3))
    ion_sp       = np.zeros(natom*super)
    ion_local_sp = np.zeros(natom*super)
    fix_sp       = np.zeros((natom*super,3),dtype='S')
    sp_j         = np.zeros(natom*super)

#  ## スーパーセル用の[内部座標]を作る(FIX未対応)
#  #make_supercell0(super_x,super_y,super_z,\
#  #               t,natom,nion,atoms,ion,ion_local,position,sv,ion_sp,ion_local_sp,sp_j,sp)

    # スーパーセル用の[内部座標]を作る(FIX対応) for VASP only
    SAE.make_supercell1(super_x,super_y,super_z,\
                        t,natom,nion,atoms,ion,ion_local,position,\
                        sv,ion_sp,ion_local_sp,sp_j,sp, \
                        fix,fix_sp)

    # SuperCell : position ---> sp
    #             atoms (make_supercell_param)
    #             natom --> natom*super
    #             cname --> outname

    # スーパーセル用の[基本並進ベクトル][原子種数]を作る
    SAE.make_supercell_param(super_x,super_y,super_z,nion,atoms,t)
    natom = natom*super

    # Cartesian to Direct
    if not direct:
        scale,direct = SAE.conv_car2direct(scale,t,natom,direct,sp)

    # POSCAR の標準出力
    print ""
   #STD=False
    STD=True
    SAE.print_poscar(outname,STD,title,scale,natom,nion,selective,direct,VASP,\
                     t,atoms,atoms_index,sp,fix_sp)

    # POSCAR のファイル出力
    STD=False
    SAE.print_poscar(outname,STD,title,scale,natom,nion,selective,direct,VASP,\
                     t,atoms,atoms_index,sp,fix_sp)
   
