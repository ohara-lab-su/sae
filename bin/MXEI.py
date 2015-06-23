#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
#
# MXEI
# VEI と似たようなセンス
#  (イオンステップごとのSCFのEnergy も含めて出力する)
#  OpexnMX だと
#
################################################################################
#
# 2015.06.15
#   計算途中のデータ DFTSCF を読み込むためのルーチンが常時選択状態だったので
#   判別するフラグを導入 ( MXPlot_MXEI.py に準ずる )
#    FLAG_DFTSCF=True
#
# 2015.06.15
#   *.dat ファイル名と systemname が異なるときの自動処理を追加
#
# 2015.03.12
#  get_uele()
#   IONループが0のとき（一回目のSCFループの時)
#    結果を途中でも書きだすように修正
#
# 2015.03.12
#  *.out が出力される前の 計算途中のファイル *.DFTSCF の読み込みに対応
#
# 2015.03.11
#   *.dat ファイル名自動検索ルーチンを導入
#
# 2015.02.26
#    ReadMxOut.get_uele() のデーター取得方法を変更
#
#                   SCF history at MD= 1
# ***********************************************************
# ***********************************************************
#
#    SCF=   1  NormRD=  1.000000000000  Uele= -73.623378509947
#    SCF=   2  NormRD=  1.445903182361  Uele= -72.425357322827
#    SCF=   3  NormRD=  0.721184409476  Uele= -72.919901228322
#    SCF=   4  NormRD=  0.408620444334  Uele= -73.197509246928
#
# ***********************************************************
# ***********************************************************
#                   SCF history at MD= 1
# ***********************************************************
# ***********************************************************
#
#    SCF=   1  NormRD=  1.000000000000  Uele= -73.674913315666
#    SCF=   2  NormRD=  1.399483389381  Uele= -72.777436036187
#
#
#  同じ MD ステップ(MD=1)で SCF ループが複数あるケースが発生した
#  Davi ループと RMM-DIIS ループか？
#
#  この処理の対応のために基本方針として
#
#    (0) ReadMdOut.get_n_ion_loop() のカウント数は変更しない
#        --> MD=1 が二回現れても MD ループは 1 とする(現行)まま
#    (1) 結果的に ReadMdOut.get_uele() の修正で対応する
#        --> MD=1 が二回現れたら 一度目の MD=1 を破棄する
#
# 2015.02.26
#  名前とsuffixを分離、-i での入力は前だけにする(ルール)で統一する方針へ
#
# 2015.02.24
#  startup
#  ReadMxOut クラスを用いる形で作成
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
#import gzip
import os
import re
import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    name = 'openmx'
    suffix = '.out'
    mxname = name+suffix

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
    )
    options,  args = parser.parse_args()

    # デフォルト名より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(mxname):
        try:
            name0 = SAE.find_datfile('dat')  # *.dat はかならずあるのでそれをトリガーに
            if not name0 == None:
                name = name0
                mxname = name+suffix
        except:
            pass

    # オプションでファイル名を入力した時
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub('\.out$','',mxname)
        mxname = name+suffix

    if len(args) > 0:
        name=args[0]
        name = re.sub('\.out$','',name)

    mxname = name+suffix

    # *.out が存在しないとき、かつ *.dat ファイルが存在するとき
    # dat ファイルの中身を読んで systemname (*.out)を検索する
    if not os.path.exists(name+'.out'):
        if os.path.exists(name+'.dat'):
            dat = SAE.ReadMxDat(name+'.dat')
            sysname = dat.get_title()
            name = sysname
            mxname = name+suffix
        else:
            sys.exit("STOP: "+name+'.out and '+name+'.dat file not found.')

    # 計算途中での DFTSCF ファイル読み込み or 通常の *.out ファイル読み込み
    module_name = 'StructureAnalysisEnvironment'
    if not os.path.exists(mxname):
        mxname = name+'.DFTSCF'
        class_name = 'ReadMxDftscf'
        FLAG_DFTSCF=True
    else:
        class_name = 'ReadMxOut'
        FLAG_DFTSCF=False

    # makes instance
    module = __import__(module_name,globals(),locals(),[class_name],-1)
    klass = getattr(module,class_name)
    out = klass(mxname)

    n_ion_loop = out.get_n_ion_loop()
    max_n_scf = out.get_max_n_scf()
    utot = out.get_utot()
    uele,uele_index = out.get_uele()

    if not n_ion_loop == 0:
        for md in range(n_ion_loop):
            print "# md =",md+1
            for scf in range(uele_index[md]):
#               print "    scf=%d, Uele = %14.11f" %(scf+1,uele[md,scf])
                print "    %15.12f" %(uele[md,scf])
        # 計算途中の最後のSCFループを表示
        if FLAG_DFTSCF:
            md = n_ion_loop
            print "# md =",md+1
            for scf in range(uele_index[md]):
                    print "    %15.12f" %(uele[md,scf])
    else:
        print "# md =",1
        for scf in range(uele_index[0]):
            print "    %15.12f" %(uele[0,scf])


