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
################################################################################
#
# 2015.07.08
#  VmakeSuperCell2.py の一層の抽象化、クラス化を念頭したの試験コード
#  VmakeSuperCell2.py (last comment 2015.02.7, last timstanp 2015.03.23) から
#
################################################################################
#
# 2015.07.08
#   現バージョンの開発終了( ReadPoscar クラスを用いたバージョンへブランチ )
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
#
# 2014.11.04
#   bag fix
#      conv_car2directa(scale,t,natom,direct,sp) ルーチンにバグ(修正)
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
#    ---> car モード対応(+微修正) VmakeSuperCell1.py = VmakeSuperCell2.py
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
__version__    = "0.3.0"
################################################################################

import sys
import os
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#import re
#from copy import deepcopy

################################################################################
def options():

    inpname = 'POSCAR'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    options, args = parser.parse_args()

    if options.INPUT : inpname = options.INPUT

    if not os.path.exists(inpname):
        if os.path.exists(inpname+".vasp"):
            POSCAR="POSCAR.vasp"
        else:
            sys.exit(POSCAR+" file not found")

    if len(args) < 3:
        sys.exit("Error: args < 3")
    else:
        super_x = args[0]
        super_y = args[1]
        super_z = args[2]
        print "Super Cell         : [",super_x,",",super_y,",",super_z,"]"

    outname = inpname+'_super_'+str(super_x)+'x'+str(super_y)+'x'+str(super_z)
    if options.OUTPUT : outname = options.OUTPUT

    print "INPUT file name    :",inpname
    print "OUTPUT file name   :",outname+".vasp"

    return inpname,outname,super_x,super_y,super_z

################################################################################
if __name__ == '__main__':

    inpname,outname,super_x,super_y,super_z = options()
    poscar = SAE.ReadVaspPoscar(inpname)
    poscar.conv_supercell(times=(super_x,super_y,super_z))
    poscar.print_poscar(outname,STD=True)
    poscar.print_poscar(outname,STD=False)

