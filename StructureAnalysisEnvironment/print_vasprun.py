#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# vasprun.xml ファイルを適当な情報から作成するルーチン
#
#  *.md  *.xyz 対応
#
# およびそのテストの __main__ ルーチン
#
################################################################################
#
# 2015.02.12
#  incar タグに IBRION (1以上) がないと p4vasp で Relax モードが現れない
#  無理やり追加
#
#  generator タグは特に必要ないのでダミー情報投入を中止
#
# 2015.02.12
#  これまで全く表示されていなかったバグは atomstype (ミス) --> atomtype へ
#  変更、スペルミスによるものだった
#  もう一つ、position タグの位置が crystal タグの中だったのも間違い
#
#  残る問題は、基本並進(box)と逆格子の基本並進だが、あまり関係ないので
#  当面は放っておく
#
#  とりあえず機能するバージョンが完成
#   *.xyz *.md ファイルを vasprun.xml へコンバート
#
# 2015.02.12
#  xml 出力時に改行を入れるために標準の ElementTree から lxml へ変更
#
# 2015.01.08 16:24
#  意図したものは全て正しく出来たが・・・情報が足りないっぽくて
#  p4vasp では動かない。おそらく、擬ポテンシャルなどの原子のtypes 情報？
#  を p4vasp は読んでいる（原子の色とか大きさとかをそれでチョイスしている？)
#
#  しばらくお蔵粋....
#  一応、MD 形式を限定的には vasprun.xml に正しく変換できる
#
# 2015.01.08 startup
#  print_vasprun.py
#  完全な vasprun.xml ファイルではなく、CONTCAR_ALL FORCE_ALL, CONTCAR, POSCAR
#  に相当する情報のみを書き出す。不完全な vasprun.xml 作成
#
#  read_md3() で読み出せる情報のみから生成する
#
#  A)
#    基本並進ベクトルは ダミーで
#      1 0 0
#      0 1 0
#      0 0 1
#    とする(scale は適時見積もる)
#
#  B)
#    Energy は wiout TS と Free Energy を等しく Energy に置く
#
#  C)
#    SCF ステップごとの結果は全て無視（記述しない)、そもそも情報がない
#
################################################################################
from __future__ import print_function
###############################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.4"
################################################################################

#import sys
#import os
import optparse
#import re

## ElementTree から lxml へスイッチ (name space は互換のため ET とする)
import xml.etree.ElementTree as ET
#import lxml.etree as ET

import numpy as np
import math

#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################

def print_vasprun0(OUTPUT,title,nloop,\
        natom,nion,atoms,atoms_index,atoms_index_j,\
        t,position_loop,force_loop,energy_loop):

    # constant
    PI = math.pi

#   try:
#       out = open(name,'w')
#   except:
#       out.close()
#       sys.exit("STOP:"+name+" can't open")

    SYSTEM = str(title)

    modeling = ET.Element('modeling')

#   # generator
#   generator = ET.SubElement(modeling, 'generator')
#   program = ET.SubElement(generator, 'i', {'name':'program', 'type':'string'})
#   program.text = 'vasp'
#   version = ET.SubElement(generator, 'i', {'name':'version', 'type':'string'})
#   version.text = '4.6.36'

    # incar
    incar = ET.SubElement(modeling, 'incar')
    systemtag = ET.SubElement(incar, 'i', {'name':'SYSTEM', 'type':'string'})
    systemtag.text = SYSTEM
    ibriontag = ET.SubElement(incar, 'i', {'name':'IBRION', 'type':'int'})
    ibriontag.text = '2'

    # kpoint
   #incar = ET.SubElement(modeling, 'kpoints')

    # parameters
    parameters = ET.SubElement(modeling, 'parameters')
    separator = ET.SubElement(parameters,'separator',{'name':'general'})
    systemtag = ET.SubElement(separator, 'i',{'type':'string','name':'SYSTEM'} )
    systemtag.text = SYSTEM

    # atominfo
    atominfo = ET.SubElement(modeling, 'atominfo')
    atomstag = ET.SubElement(atominfo, 'atoms')
    atomstag.text = str(natom)
    typestag = ET.SubElement(atominfo, 'types')
    typestag.text = str(nion)

    # atomsinfo/array[@name='atoms']
    array = ET.SubElement(atominfo, 'array',{'name':'atoms'})
    dimension = ET.SubElement(array, 'dimension',{'dim':'1'})  # 1で良いかは不明
    dimension.text = 'ion'
    field = ET.SubElement(array, 'field',{'type':'string'})
    field.text = 'element'
    field = ET.SubElement(array, 'field',{'type':'int'})
    field.text = 'atomtype'

    # atomsinfo/array[@name='atoms']/set
    settag = ET.SubElement(array,'set')
    for i in range(nion):
        for j in range(atoms[i]):
           #print atoms_index[i],i+1
            rc = ET.SubElement(settag,'rc')
            c = ET.SubElement(rc,'c')
            c.text = str(atoms_index[i])
            c = ET.SubElement(rc,'c')
            c.text = str(i+1)            # !!! 見なおす必要あり !!!

    # atomsinfo/array[@name='atomtype']  (擬ポテンシャルの情報)
    array = ET.SubElement(atominfo, 'array', {'name':'atomtypes'})
    dimension = ET.SubElement(array, 'dimension',{'dim':'1'}) # 1で良いかは不明
    dimension.text = 'type'
    field = ET.SubElement(array, 'field',{'type':'int'})
    field.text = 'atomspertype'
    field = ET.SubElement(array, 'field',{'type':'string'})
    field.text = 'element'
    field = ET.SubElement(array, 'field')
    field.text = 'mass'
    field = ET.SubElement(array, 'field')
    field.text = 'valence'
    field = ET.SubElement(array, 'field',{'type':'string'})
    field.text = 'pseudopotential'

    # atomsinfo/array[@name='atomtype']/set
    settag = ET.SubElement(array,'set')
    for i in range(nion):
        rc = ET.SubElement(settag,'rc')
        c = ET.SubElement(rc,'c')
        c.text = str(atoms[i])
        c = ET.SubElement(rc,'c')
        c.text = str(atoms_index[i])
        c = ET.SubElement(rc,'c')
        c.text = str(1.00000000)  # dummy
        c = ET.SubElement(rc,'c')
        c.text = str(1.00000000)  # dummy
        c = ET.SubElement(rc,'c')
        c.text = str('PAW dummy')  # dummy

    ############################################################################
    # structure[@name='initialpos']
    # initial
    structure = ET.SubElement(modeling, 'structure',{'name':'initialpos'})
    crystal = ET.SubElement(structure, 'crystal')

    # 基本並進ベクトル(initial)の表示
    #  t0 = a00 a10 a20  ! lattice vector t0
    #  t1 = a01 a11 a21  ! lattice vector t1
    #  t2 = a02 a12 a22  ! lattice vector t2
    varray = ET.SubElement(crystal, 'varray', {'name':'basis'})
    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,0])+"   "\
             "{0:.8f}".format(t[1,0])+"   "\
             "{0:.8f}".format(t[2,0])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,1])+"   "\
             "{0:.8f}".format(t[1,1])+"   "\
             "{0:.8f}".format(t[2,1])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,2])+"   "\
             "{0:.8f}".format(t[1,2])+"   "\
             "{0:.8f}".format(t[2,2])

    volume= ET.SubElement(crystal, 'i', {'name':'volume'})
    volume.text = "{0:.8f}".format(t[0,0]*t[1,1]*t[2,2])

    # 基本並進ベクトル(initial)の逆行列の表示
    t_rec = np.linalg.inv(t)*2*PI  # 逆格子の作成
    varray = ET.SubElement(crystal, 'varray', {'name':'rec_basis'})
    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,0])+"   "\
             "{0:.8f}".format(t_rec[1,0])+"   "\
             "{0:.8f}".format(t_rec[2,0])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,1])+"   "\
             "{0:.8f}".format(t_rec[1,1])+"   "\
             "{0:.8f}".format(t_rec[2,1])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,2])+"   "\
             "{0:.8f}".format(t_rec[1,2])+"   "\
             "{0:.8f}".format(t_rec[2,2])

    # 初期原子位置の表示
    varray = ET.SubElement(structure, 'varray', {'name':'positions'})
    for atom in range(natom):
       #print atoms_index_j[atom]
        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(position_loop[0,atom,0])+"   "\
                 "{0:.8f}".format(position_loop[0,atom,1])+"   "\
                 "{0:.8f}".format(position_loop[0,atom,2])


    ############################################################################
    # calculation
    for loop in range(nloop):
        calculation = ET.SubElement(modeling, 'calculation')
        structure = ET.SubElement(calculation, 'structure')

        # calculation/structure/crystal 基本並進ベクトル(loop)
        crystal = ET.SubElement(structure, 'crystal')
        varray = ET.SubElement(crystal, 'varray',{'name':'basis'})
        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t[0,0])+"   "\
                 "{0:.8f}".format(t[1,0])+"   "\
                 "{0:.8f}".format(t[2,0])

        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t[0,1])+"   "\
                 "{0:.8f}".format(t[1,1])+"   "\
                 "{0:.8f}".format(t[2,1])

        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t[0,2])+"   "\
                 "{0:.8f}".format(t[1,2])+"   "\
                 "{0:.8f}".format(t[2,2])

        # calculation/structure/crystal 逆格子(loop)
        t_rec = np.linalg.inv(t)*2*PI  # 逆格子の作成
        varray = ET.SubElement(crystal, 'varray', {'name':'rec_basis'})
        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t_rec[0,0])+"   "\
                 "{0:.8f}".format(t_rec[1,0])+"   "\
                 "{0:.8f}".format(t_rec[2,0])

        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t_rec[0,1])+"   "\
                 "{0:.8f}".format(t_rec[1,1])+"   "\
                 "{0:.8f}".format(t_rec[2,1])

        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(t_rec[0,2])+"   "\
                 "{0:.8f}".format(t_rec[1,2])+"   "\
                 "{0:.8f}".format(t_rec[2,2])

        # calculation/strucute/crystal 原子位置(loop)
        varray = ET.SubElement(structure, 'varray', {'name':'positions'})
        for atom in range(natom):
            v = ET.SubElement(varray, 'v')
            v.text = "{0:.8f}".format(position_loop[loop,atom,0])+"   "\
                     "{0:.8f}".format(position_loop[loop,atom,1])+"   "\
                     "{0:.8f}".format(position_loop[loop,atom,2])

        # calculation/varray フォース(loop)
        varray = ET.SubElement(calculation, 'varray', {'name':'forces'})
        for atom in range(natom):
            v = ET.SubElement(varray, 'v')
            v.text = "{0:.8f}".format(force_loop[loop,atom,0])+"   "\
                     "{0:.8f}".format(force_loop[loop,atom,1])+"   "\
                     "{0:.8f}".format(force_loop[loop,atom,2])

        # calculation/energy エネルギー(loop)
        e0 = 0.0
        energy = ET.SubElement(calculation, 'energy')
        e_fr_energy = ET.SubElement(energy, 'i',{'name':'e_fr_energy'})
        e_fr_energy.text = "{0:.8f}".format(energy_loop[loop])
        e_wo_entrp = ET.SubElement(energy, 'i',{'name':'e_wo_entrp'})
        e_wo_entrp.text = "{0:.8f}".format(energy_loop[loop])
        e_0_energy = ET.SubElement(energy, 'i',{'name':'e_0_energy'})
        e_0_energy.text = "{0:.8f}".format(e0)


    ############################################################################
    # structure[@name='finalpos']
    # final
    structure = ET.SubElement(modeling, 'structure',{'name':'finalpos'})
    crystal = ET.SubElement(structure, 'crystal')

    # 基本並進ベクトル(initial)の表示
    #  t0 = a00 a10 a20  ! lattice vector t0
    #  t1 = a01 a11 a21  ! lattice vector t1
    #  t2 = a02 a12 a22  ! lattice vector t2
    # structure/crystal/varray
    varray = ET.SubElement(crystal, 'varray', {'name':'basis'})
    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,0])+"   "\
             "{0:.8f}".format(t[1,0])+"   "\
             "{0:.8f}".format(t[2,0])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,1])+"   "\
             "{0:.8f}".format(t[1,1])+"   "\
             "{0:.8f}".format(t[2,1])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t[0,2])+"   "\
             "{0:.8f}".format(t[1,2])+"   "\
             "{0:.8f}".format(t[2,2])

    volume= ET.SubElement(crystal, 'i', {'name':'volume'})
    volume.text = "{0:.8f}".format(t[0,0]*t[1,1]*t[2,2])

    # 基本並進ベクトル(initial)の逆行列の表示
    # structure/crystal/varray
    t_rec = np.linalg.inv(t)*2*PI  # 逆格子の作成
    varray = ET.SubElement(crystal, 'varray', {'name':'rec_basis'})
    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,0])+"   "\
             "{0:.8f}".format(t_rec[1,0])+"   "\
             "{0:.8f}".format(t_rec[2,0])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,1])+"   "\
             "{0:.8f}".format(t_rec[1,1])+"   "\
             "{0:.8f}".format(t_rec[2,1])

    v = ET.SubElement(varray, 'v')
    v.text = "{0:.8f}".format(t_rec[0,2])+"   "\
             "{0:.8f}".format(t_rec[1,2])+"   "\
             "{0:.8f}".format(t_rec[2,2])

    # 最終原子位置の表示
    # structure/crystal/varray
    varray = ET.SubElement(structure, 'varray', {'name':'positions'})
    for atom in range(natom):
       #print atoms_index_j[atom]
        v = ET.SubElement(varray, 'v')
        v.text = "{0:.8f}".format(position_loop[nloop-1,atom,0])+"   "\
                 "{0:.8f}".format(position_loop[nloop-1,atom,1])+"   "\
                 "{0:.8f}".format(position_loop[nloop-1,atom,2])



#   ET.dump(modeling)
#   tree = ET.tostring(modeling, method="xml")
#   print tree

    tree = ET.ElementTree(modeling)
#   tree.write(OUTPUT, method="xml")

    # for lxml
#   tree.write(OUTPUT, pretty_print=True, method="xml")  # for lxml

    # for element tree
    tree.write(OUTPUT, method="xml")

################################################################################
if __name__ == '__main__':

    OUTPUT = 'vasprun.xml'
    MD = 'co.md'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=MD,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        MD=options.INPUT

    if len(args) > 0:
        MD=args[0]

    title = MD

    # MX(xyz) ファイルの事前読み込み
    nloop,natom = SAE.read_md_param(MD)

    # MD(xyz) ファイルの事前準備
    atoms_index_j  = np.zeros((natom),dtype='S2')
    position_loop = np.zeros((nloop,natom,3))
    force_loop = np.zeros((nloop,natom,3))

    # MD(xyz) ファイル読み込み + Force 対応
    natom,nlist,elist,nion,atoms,atoms_index,energy_loop = \
                SAE.read_md3(MD,nloop,atoms_index_j,position_loop,force_loop)

    # MD(x,y,z) のそれぞれの x,y,z の最大値を取得
    position_max,position_min = SAE.get_max_md(nloop,natom,position_loop)
    max_range = abs(position_min)+position_max

#   box_size = max_range*2.0
    box_size = 10.0

    # 分子/原子を収納する箱を作る。ダミーの基本並進ベクトル作成(cubic)
    #       t0 = a00 a10 a20  ! lattice vector t0
    #       t1 = a01 a11 a21  ! lattice vector t1
    #       t2 = a02 a12 a22  ! lattice vector t2
    t = np.zeros((3,3))
    t[0,0] = 1.0*box_size
    t[1,1] = 1.0*box_size
    t[2,2] = 1.0*box_size
    scale = 1.0

    # MD(x,y,z) の座標系をcartesian基本並進系に変換する
    # MD(直交系)からVASP(直交系)への変換なのでスケールするだけ
    # using numpy
    # 注意) VASP のデーターから引っ張った時は逆に scale でスケールされてないので
    #       box_size で割ってはいけない
    position_loop = position_loop/box_size
#   position_loop = position_loop/1.0


    # position の initial と final を分けておく
#   for l in range(nloop):
#       print natom
#       print "   setp=",l
#       for j in range(natom):
#           print " %3s %12.8f %12.8f %12.8f " \
#                 % ( atoms_index_j[j],\
#                     position_loop[l,j,0],\
#                     position_loop[l,j,1],\
#                     position_loop[l,j,2] )

    # vasprun.xml の最低出力をする(OpenMX *.md 形式から引き出せる最低の形式)
    print_vasprun0(OUTPUT,title,nloop,\
            natom,nion,atoms,atoms_index,atoms_index_j,\
            t,position_loop,force_loop,energy_loop)


