#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み --> VASP 形式出力
#
# 必須クラス
#
#  ReadMxDat , ReadMxDatMethod
#
################################################################################
#
# 2015.06.30
#  == None --> is None
#
# 2015.03.11
#  自動ファイル名検索関係のバグを修正
#
# 2015.03.10
#  NEGF モードの時の Left と Right の出力に対応
#
# 2015.03.10
#  基本並進ベクトルが存在しない場合には xyz 形式での出力もする
#  vasp 形式での出力はこの時点ではダミーに近い
#
# 2015.03.09
#  -o オプションでの出力ファイル名に .dat がついてたら自動で削除する
#  .dat を抜いた時のファイル名とinputファイル名が等しい時は処理を止める
#
# 2015.02.27
#  -o オプションが機能してないバグを修正
#
# 2015.02.27
#  変換バグ発覚、再チェック
#   1) IGZO (sc) dat --> vasp direct [OK]
#
# 2015.02.17
#  ReadDatMx --> ReadMxDat へ変更
#
# 2015.02.17
#  基本並進ベクトルが存在しない分子系の*.dat の場合の処理を追加
#
#    position の最大値と最小値の差の絶対値の 1.2 倍をそれぞれ基本並進
#    の対角成分とする
#    ===> 再考の必要はある
#
# 2015.02.12 1st
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014-2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.7"
################################################################################

import sys
import os
import re
#import gzip
#import numpy as np

import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    name ='openmx'
    suffix = '.dat'
    mxname = name+suffix

    poscarname = 'openmx.vasp'
    xyzname = 'openmx.xyz'

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    parser.add_option( '-d','--direct',
                        action='store_true',
                        default=False,
                        dest='DIRECT',
    )
    parser.add_option( '-s','--std',
                        action='store_true',
                        default=False,
                        dest='STDOUT',
    )
    options, args = parser.parse_args()

    # デフォルト名より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(mxname):
        name0 = SAE.find_datfile('dat')
        if not name0 is None:
            name = name0
            mxname = name+suffix
            poscarname = mxname+'.vasp'
            xyzname = mxname+'.xyz'

    if options.INPUT:
        mxname = options.INPUT
        poscarname = mxname+'.vasp'
        xyzname = mxname+'.xyz'

    if options.OUTPUT:
        poscarname = options.OUTPUT
        # もし出力ファイル名のsuffixに .dat がついていたら安全のためにそれを消す
        poscarname=re.sub('\.dat','',poscarname)

    if poscarname == mxname:
        sys.exit("STOP: input-filename = output-filename")

    return [mxname,poscarname,xyzname,options.STDOUT,options.DIRECT]

################################################################################
if __name__ == '__main__':

    mxname,poscarname,xyzname,OPT_STDOUT,OPT_DIRECT = options()

    if not OPT_STDOUT:
        print "STDOUT             =",OPT_STDOUT
        print "INPUT OpenMX File  =",mxname
        print "OUTPUT POSCAR file =",poscarname

        try:
            out_poscar = open(poscarname,'w')
        except:
            out_poscar.close()
            sys.exit("STOP: "+poscarname+" does'nt open")

#       sys.stdout = out_poscar

    # OpenMX 読み込みインスタンス生成
    dat = SAE.ReadMxDat(mxname)

    title = dat.get_title()
    nion = dat.get_nion()
    natom = dat.get_natom()
    atoms = dat.get_atoms()
    atoms_j = dat.get_atoms_j()
    atoms_index = dat.get_atoms_index()
    atoms_index_j = dat.get_atoms_index_j()
    scale = dat.get_scale()
    t = dat.get_t()
    selective = dat.get_selective()
    direct = dat.get_direct()
    position = dat.get_position()
    fix = dat.get_fix()

    position_max = dat.get_position_max()
    position_min = dat.get_position_min()

    left_natom = dat.get_left_natom()
    left_atoms_index_j = dat.get_left_atoms_index_j()
    left_position = dat.get_left_position()
    right_natom = dat.get_right_natom()
    right_atoms_index_j = dat.get_right_atoms_index_j()
    right_position = dat.get_right_position()

    if not dat.FLAG_t:
        print "OUTPUT XYZ file    =",xyzname

        try:
            out_xyz = open(xyzname,'w')
        except:
            out_xyz.close()
            sys.exit("STOP: "+xyzname+" does'nt open")

    ############################################################################
    ## print xyz style
    ##
    if not dat.FLAG_t:
        print >> out_xyz, natom
        print >> out_xyz, ""

        # for Molecule (xyz)
        for i in range(natom):
            print >> out_xyz, " %s %13.9f %13.9f %13.9f" \
                    % ( atoms_index_j[i], position[i,0],position[i,1],position[i,2] )

    if not dat.FLAG_t:
        out_xyz.close()

    ############################################################################
    ## Left print xyz style
    ##
    if dat.FLAG_left:
        left_xyz_name=re.sub('\.xyz','',xyzname)
        left_xyz_outname=left_xyz_name+'.left.xyz'
        try:
            out_left_xyz = open(left_xyz_outname,'w')
        except:
            out_left_xyz.close()
            sys.exit("STOP: "+left_xyz_outname+" does'nt open")

        print "OUTPUT left xyz    =",left_xyz_outname
        print >> out_left_xyz,left_natom
        print >> out_left_xyz,""
        for j in range(left_natom):
            print >> out_left_xyz, " %s %13.9f %13.9f %13.9f" \
                 %( left_atoms_index_j[j],\
                    left_position[j,0],left_position[j,1],left_position[j,2] )
        out_left_xyz.close()

    ############################################################################
    ## Right print xyz style
    ##
    if dat.FLAG_right:
        right_xyz_name=re.sub('\.xyz','',xyzname)
        right_xyz_outname=left_xyz_name+'.right.xyz'
        try:
            out_right_xyz = open(right_xyz_outname,'w')
        except:
            out_right_xyz.close()
            sys.exit("STOP: "+right_xyz_outname+" does'nt open")

        print "OUTPUT right xyz   =",right_xyz_outname
        print >> out_right_xyz,right_natom
        print >> out_right_xyz,""
        for j in range(right_natom):
            print >> out_right_xyz, " %s %13.9f %13.9f %13.9f"\
                 %( right_atoms_index_j[j],\
                    right_position[j,0],right_position[j,1],right_position[j,2] )
        out_right_xyz.close()


    ############################################################################
    if not dat.FLAG_t:
        print "MOLECULE MODE      =",dat.FLAG_t

    if not OPT_STDOUT:
        print "DIRECT MODE        =",OPT_DIRECT


    ############################################################################
    ## Right print POSCAR style
    ##
    if dat.FLAG_t:
        print >> out_poscar, title
    else:
        print >> out_poscar, title+"  (mol-mode: dummy translation vector)"

    # makes scale and translation vector
    if dat.FLAG_t:
        print >> out_poscar, " ",scale
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,0],t[1,0],t[2,0] )
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,1],t[1,1],t[2,1] )
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,2],t[1,2],t[2,2] )
    else:
        ### makes dummy translation vector
        print >> out_poscar, " ",scale
        t[1,0] = 0.0
        t[2,0] = 0.0
        t[0,1] = 0.0
        t[2,1] = 0.0
        t[0,2] = 0.0
        t[1,2] = 0.0
        t[0,0] = abs(position_max[0]-position_min[0])*1.20
        t[1,1] = abs(position_max[1]-position_min[1])*1.20
        t[2,2] = abs(position_max[2]-position_min[2])*1.20
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,0],t[1,0],t[2,0] )
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,1],t[1,1],t[2,1] )
        print >> out_poscar,"  %13.9f %13.9f %13.9f" %( t[0,2],t[1,2],t[2,2] )

    print >> out_poscar," ",
    for i in range(nion):
        print >> out_poscar,atoms_index[i],
    print >> out_poscar," "

    print >> out_poscar," ",
    for i in range(nion):
        print >> out_poscar,atoms[i],
    print >> out_poscar," "

    if selective:
        print >> out_poscar,"Selective Dynamics"
    if direct:
        print >> out_poscar,"Direct"
    else:
        print >> out_poscar,"Cartesian"

    for i in range(natom):
        print >> out_poscar, " %13.9f %13.9f %13.9f" \
                % ( position[i,0],position[i,1],position[i,2] ),
        if selective:
            print >> out_poscar,"",
            print >> out_poscar,fix[i,0],fix[i,1],fix[i,2],
        print >> out_poscar,""

#   for i in range(natom):
#       print fix[i][0], fix[i][1], fix[i][2]

    if not OPT_STDOUT:
        out_poscar.close()


