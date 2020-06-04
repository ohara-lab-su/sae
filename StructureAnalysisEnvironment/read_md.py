#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
#  MD(xyz) 形式の読み込み
#   def read_md3(): 座標(x,y,z) + フォース(x,y,z) + Energy 形式に対応
#   def read_md2(): 座標(x,y,z) + フォース(x,y,z) 形式に対応
#   def read_md():  xyz 情報の読み込み
#
#
# [in]     cname         : MD ファイル( xyz 形式 ) ファイル名
# [in]     nloop         : トータルのループ数
# [in/out] atoms_index_j : atoms_index (サイト番号で元素記号を返す) の全原子番号版
#                        : 全通し番号から元素名を返す
# [in/out] position_loop : ループごとの原子位置
# [in/out] force_loop    : ループごとのフォース
#
# [return] natom : (セル内)トータルの原子数
# [return] nlist : xyz+フォースの行数 (フォースの有無の判定用)
#
################################################################################
#
# 2015.01.08
#   OpenMX で吐出される md 形式 座標(xyz) + フォース(xyz) + Energy
#   に対応した read_md3() を用意
#
#   read_md3()
#      natom だけではなく nion 及び atoms atoms_index 情報も取得する
#
#      基本方針として
#      nion は(仮)なので、同じ元素記号が続いてたら同一type としてくくる
#      同じ元素記号が連続していて 別 type の場合は原理的に区別する情報が
#      MDファイルには存在してないので、諦める
#
#      --> nion 作成
#      --> atoms (イオン(type)毎の原子数
#      --> atoms_index (イオン(type)毎の元素記号)
#
#   read_md(), read_md1() で戻り値 nloop を廃止した
#   read_md(), read_md1() で引数 natom を廃止した
#
# 2015.01.07
#   read_md2(): 座標(x,y,z) + フォース(x,y,z) 形式に対応
#
# 2014.11.18 1st
#   read_md():  xyz 情報の読み込み
#
################################################################################
from __future__ import print_function

try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.3"

################################################################################

import sys
import optparse
import os
# import re
# from numpy import *
import numpy as np

import StructureAnalysisEnvironment as SAE


# import SpaceGroupEnvironment as SGE


################################################################################
def read_md(cname, nloop, atoms_index_j, position_loop):
    ###############################################
    ## Open POSCAR file
    ##
    if not os.path.exists(cname):
        sys.exit(cname + " file not found")

    try:
        tmp = open(cname)
    except:
        tmp.close()
        sys.exit("STOP: " + cname + " does'nt open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    #   total_line=len(datlines)-1   # トータルの行数
    natom = int(datlines[0])  # 総原子数

    ###############################################
    # データー読み込み
    i = 0
    for l in range(nloop):
        i = i + 2
        # print "------- LOOP "+str(l)+" ------"
        for j in range(natom):
            # print i,j,datlines[i]
            tmp = datlines[i].split()
            atoms_index_j[j] = str(tmp[0])
            position_loop[l, j, 0] = float(tmp[1])
            position_loop[l, j, 1] = float(tmp[2])
            position_loop[l, j, 2] = float(tmp[3])
            i += 1

    return [natom]


################################################################################
def read_md2(cname, nloop, atoms_index_j, position_loop, force_loop):
    ###############################################
    ## Open POSCAR file
    ##
    if not os.path.exists(cname):
        sys.exit(cname + " file not found")

    try:
        tmp = open(cname)
    except:
        tmp.close()
        sys.exit("STOP: " + cname + " does'nt open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    #   total_line=len(datlines)-1   # トータルの行数
    natom = int(datlines[0])  # 総原子数

    ###############################################
    # データー読み込み
    i = 0
    for l in range(nloop):
        i = i + 2
        # print "------- LOOP "+str(l)+" ------"
        for j in range(natom):
            # print i,j,datlines[i]
            tmp = datlines[i].split()
            nlist = len(tmp)
            atoms_index_j[j] = str(tmp[0])
            position_loop[l, j, 0] = float(tmp[1])
            position_loop[l, j, 1] = float(tmp[2])
            position_loop[l, j, 2] = float(tmp[3])
            if nlist >= 7:
                force_loop[l, j, 0] = float(tmp[4])
                force_loop[l, j, 1] = float(tmp[5])
                force_loop[l, j, 2] = float(tmp[6])
            i += 1

    return [natom, nlist]


################################################################################
def read_md3(cname, nloop, atoms_index_j, position_loop, force_loop):
    ###############################################
    ## Open POSCAR file
    ##
    if not os.path.exists(cname):
        sys.exit(cname + " file not found")

    try:
        tmp = open(cname)
    except:
        tmp.close()
        sys.exit("STOP: " + cname + " does'nt open")

    datfile = tmp.read()
    tmp.close()
    datlines = datfile.split('\n')

    #   total_line=len(datlines)-1   # トータルの行数
    natom = int(datlines[0])  # 総原子数

    ###############################################
    # データー読み込み
    i = 0
    energy_loop = np.zeros(nloop)
    atoms_index = []
    for l in range(nloop):

        # get Energy
        tmp = datlines[i + 1].split()
        elist = len(tmp)
        if len(tmp) >= 5:
            energy_loop[l] = tmp[4]
        # print energy_loop[l]

        i = i + 2

        atoms_tmp = ''
        nion = 0
        # print "------- LOOP "+str(l)+" ------"
        for j in range(natom):

            tmp = datlines[i].split()
            atoms_index_j[j] = str(tmp[0])

            # makes atoms_index & nion
            if atoms_index_j[j] != atoms_tmp:
                nion += 1
                atoms_tmp = atoms_index_j[j]
                atoms_index.append(atoms_index_j[j])

            position_loop[l, j, 0] = float(tmp[1])
            position_loop[l, j, 1] = float(tmp[2])
            position_loop[l, j, 2] = float(tmp[3])

            nlist = len(tmp)
            if nlist >= 7:
                force_loop[l, j, 0] = float(tmp[4])
                force_loop[l, j, 1] = float(tmp[5])
                force_loop[l, j, 2] = float(tmp[6])
            i += 1

    ## makes atoms[nion]
    i = 0
    atoms = np.zeros(nion, dtype=int)
    for l in range(nloop):
        i = i + 2
        atoms_tmp = ''
        nion = 0
        local = 0
        for j in range(natom):
            tmp = datlines[i].split()
            atoms_index_j[j] = str(tmp[0])

            # makes atoms[ion]
            if atoms_index_j[j] != atoms_tmp:
                local = 0
                nion += 1
                atoms_tmp = atoms_index_j[j]
            if atoms_index_j[j] == atoms_tmp:
                local += 1
                atoms[nion - 1] = local
            i += 1

    #   print "nion = ",nion
    #   for i in range(nion):
    #       print atoms_index[i], atoms[i]

    return [natom, nlist, elist, nion, atoms, atoms_index, energy_loop]


################################################################################
if __name__ == '__main__':

    MD = "co.md"  # default name
    #   MD = "C60_position.xyz"

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input',
                      dest='INPUT',
                      default=MD,
                      )
    options, args = parser.parse_args()

    if options.INPUT:
        MD = options.INPUT

    if len(args) > 0:
        MD = args[0]

    # MD(xyz) ファイルの事前読み込み
    nloop, natom = SAE.read_md_param(MD)

    # MD(xyz) ファイルの事前準備
    atoms_index_j = np.zeros((natom), dtype='S2')  # 通し番号(max=atom)で元素名(記号)を保存する
    position_loop = np.zeros((nloop, natom, 3))
    force_loop = np.zeros((nloop, natom, 3))

    print("READFILE:%s" % str(MD))
    print("NLOOP   :%s" % str(nloop))
    print("NATOM   :%s" % str(natom))

    natom, nlist, elist, nion, atoms, atoms_index, energy_loop = \
        read_md3(MD, nloop, atoms_index_j, position_loop, force_loop)

    print("NION    :%s" % str(nion))
    for i in range(nion):
        print("%s %s" % (str(atoms_index[i]), str(atoms[i])))

    if nlist >= 7:
        for l in range(nloop):
            print("%s" % str(natom))
            if elist >= 5:
                # print("   setp=",l,"   ","Energy=",energy_loop[l])
                print("   setp=%s   Energy=%s" % (str(l), str(energy_loop[l])))
            else:
                # print "   setp=",l
                print("   setp=%s" % str(l))

            for j in range(natom):
                print(" %3s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f"
                      % (atoms_index_j[j],
                         position_loop[l, j, 0],
                         position_loop[l, j, 1],
                         position_loop[l, j, 2],
                         force_loop[l, j, 0],
                         force_loop[l, j, 1],
                         force_loop[l, j, 2]))
    else:
        for l in range(nloop):
            print("%s" % str(natom))
            print("   setp=%s" % str(l))
            for j in range(natom):
                print(" %3s %12.8f %12.8f %12.8f "
                      % (atoms_index_j[j],
                         position_loop[l, j, 0],
                         position_loop[l, j, 1],
                         position_loop[l, j, 2]))

## for read_md2
#
#   # MD(xyz) ファイル読み込み + Force 対応
#   natom,nlist = \
#           read_md2(MD,nloop,atoms_index_j,position_loop,force_loop)

#   if nlist >= 7:
#       for l in range(nloop):
#           print "------- LOOP "+str(l)+" ------"
#           for j in range(natom):
#               print " %3s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f" \
#                     % ( atoms_index_j[j],\
#                         position_loop[l,j,0],\
#                         position_loop[l,j,1],\
#                         position_loop[l,j,2],\
#                         force_loop[l,j,0],\
#                         force_loop[l,j,1],\
#                         force_loop[l,j,2] )
#   else:
#       for l in range(nloop):
#           print "------- LOOP "+str(l)+" ------"
#           for j in range(natom):
#               print " %3s %12.8f %12.8f %12.8f " \
#                     % ( atoms_index_j[j],\
#                         position_loop[l,j,0],\
#                         position_loop[l,j,1],\
#                         position_loop[l,j,2] )
#
