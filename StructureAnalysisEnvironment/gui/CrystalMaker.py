#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_Bader.py および Vplot_Crystal*.py シリーズで使われる
# Crystal 関係の Class
#
#
################################################################################
#
# 2015.07.08
#   Vplot_Barder.py から branch (単独化) --> CrystalMaker.py
#
# 2015.07.08
#   スーパーセル表示対応
#
# 2015.07.06 1st
#   Vplot_Crysta.py から branch -> Vplot_Bader.py
#   Vplot_Bader.py の高度化
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

import sys

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#from crystal_make_unit import *

import numpy as np
import visual as vp
import wx
#import time

#import Image
#import ImageGrab

import os
#import re
#import optparse
#from copy import deepcopy


################################################################################
class CrystalMaker(object):

    ############################################################################
    def __init__(self,cell,\
            code='VASP',\
            origin=[-0.5,-0.5,0],\
            background=[0.5,0.5,0.5],\
            times=[1,1,1]):

        self.origin = origin
        self.code = code
        self.cell = cell
        self.times = times

#       background=(0.5,0.5,0.5)

        vp.display(title="structrue window",width=500 , height=500, background=background)
        self.crystalframe = vp.frame()

    ############################################################################
    ## 原子の描画
    ##  (super cell 対応版)
    def plot_atoms(self,cell=None,times=None):

        if cell is not None: self.cell = cell
        if times is not None: self.times = times

        # スーパーセル化
        self.cell.conv_supercell(times=(self.times[0],self.times[1],self.times[2]))

        # 原子座標系のCartesian to Direct 変換
        if self.cell.direct:
            ABS=False
            self.cell.scale,self.cell.direct = SAE.conv_direct2car0(ABS,\
                    self.cell.scale,\
                    self.cell.t,\
                    self.cell.natom,\
                    self.cell.direct,\
                    self.cell.position)

        # 絶対座標系へ変換( cartesian and scale=1.0 )
        self.cell.scale = SAE.conv_car2carABS(\
                self.cell.scale,\
                self.cell.t,\
                self.cell.natom,\
                self.cell.direct,\
                self.cell.position)

        self.ratio=0.3

        for i in range(self.cell.natom):

            # 描画の原点位置修正
            xp = self.cell.position[i,0] + self.origin[0]
            yp = self.cell.position[i,1] + self.origin[1]
            zp = self.cell.position[i,2] + self.origin[2]

            # 原子の種類を取得(記号)
            atom_type = str(self.cell.atoms_index[int(self.cell.ion[i])])

            # 原子半径を取得
            radius = SAE.get_atomic_radius1(atom_type)
            R = radius*self.ratio

            # 原子番号を取得
            num = SAE.get_atomic_number1(atom_type)

            # 原子の描画
            atom = vp.sphere(frame=self.crystalframe,pos=(xp,yp,zp), radius=R)

            # 原子の色設定(RGB)を適当に自動化,マジで適当(いい加減)
            atom.red   = 0.5*num*num
            atom.green = 0.1*num
            atom.blue  = 1/num

    ############################################################################
    # 単位胞描画
    def plot_unit_cell(self,cell=None,radius=0.05,color=[255,255,255]):

        if cell is not None: self.cell = cell

        SAE.crystal_make_unit(self.cell.t,\
                origin=self.origin,\
                radius=radius,\
                color=color)


    ############################################################################
    # Bondの描画
    def plot_bonds(self,cell=None,bondradious=0.08,code=None,bondlog=False):

        if cell is not None: self.cell = cell
        if code is not None: self.code = code

        # ボンド情報の獲得
        if os.path.exists('bond.dat'):
            try:
                bondfile = open('bond.dat').read().split('\n')
            except:
                bondfile.close()

#           nline = len(bondfile) -1
            nbond = int(bondfile[0])

            atom1 = np.zeros(nbond)
            atom2 = np.zeros(nbond)
            dist = np.zeros(nbond)

            for i in range(nbond):
                atom1[i] = int(bondfile[1+i].split()[0])
                atom2[i] = int(bondfile[1+i].split()[1])
                dist[i] = float(bondfile[1+i].split()[2])

        else:
            # デフォルトのボンド設定
            nbond = 1
            atom1 = np.zeros(1)
            atom2 = np.zeros(1)
            dist = np.zeros(1)
            atom1[0] = 1
            atom2[0] = 1
            dist[0] = 2.8

        # ボンドの数だけループする
        for j in range(nbond):

            print "------------- bond "+str(j+1)+" ------------"
            print "atom1=",atom1[0]
            print "atom2=",atom2[0]
            print "distance=",dist[0]
            if atom1[0] >  self.cell.nion or atom2[0] > self.cell.nion:
                print "set bond_FLAG=False : aotm1 >  nion or atom2 >  nion"

            # VASP の場合はVASP5以上の書式が必要(原子番号情報が必要)
            if self.code == 'VASP':
                if self.cell.vasp_version < 5:
                    sys.exit("STOP: VASP version < 5 ")

            # bond 情報の取得
            bondnum = \
                    SAE.get_bond_info_param(atom1[j],atom2[j],dist[j],\
                            self.cell.nion,\
                            self.cell.atoms,\
                            self.cell.position)

            print "NUMBER OF BOND     :",bondnum

            bondr = np.zeros((bondnum))
            bond1 = np.zeros((bondnum),dtype=int)
            bond2 = np.zeros((bondnum),dtype=int)

            SAE.get_bond_info(atom1[j],atom2[j],dist[j],\
                    self.cell.nion,\
                    self.cell.atoms,\
                    self.cell.atoms_index,\
                    self.cell.position,\
                    bondr,bond1,bond2)

            # ボンドの太さ
            BR = bondradious

            for num in range(bondnum):

                x1 = self.cell.position[bond1[num],0]
                y1 = self.cell.position[bond1[num],1]
                z1 = self.cell.position[bond1[num],2]

                x2 = self.cell.position[bond2[num],0]
                y2 = self.cell.position[bond2[num],1]
                z2 = self.cell.position[bond2[num],2]

                x12 =  x2 - x1
                y12 =  y2 - y1
                z12 =  z2 - z1

                x0 = x1 + self.origin[0]
                y0 = y1 + self.origin[1]
                z0 = z1 + self.origin[2]

                r1 = bondr[num]

                vp.cylinder( frame=self.crystalframe, \
                        pos=(x0,y0,z0), \
                        axis=(x12,y12,z12), \
                        radius =BR )

                if bondlog:
                    print "-------------------- bond "+str(j)+" ---------------"
                    print num, bond1[num],"("+str(self.cell.atoms_index[int(self.cell.ion[bond1[num]])])+") -",\
                               bond2[num],"("+str(self.cell.atoms_index[int(self.cell.ion[bond2[num]])])+")"  ,\
                               " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f" \
                               % ( r1, x1,y1,z1, x2,y2,z2)

    ############################################################################
    # 画像保存
#   def plot_save(self):
#       im = ImageGrab.grab(0,0,600,600)
#       im.save('filename.jpg')

    ############################################################################
    ## Bader Charge の描画(色で区別する)
    ## 一度 plot_crystal を読んだことがあるのが前提(cell情報の変換等)
    def plot_bader(self,acf,mode='ABS',cmax=None,cmin=None):

        if not isinstance(acf, SAE.ReadVaspAcf):
            sys.exit("STOP: acf does'nt instance")

        acf.get_min_bader()
        acf.get_max_bader()

        for i in range(self.cell.natom):

            xp = self.cell.position[i,0] + self.origin[0]
            yp = self.cell.position[i,1] + self.origin[1]
            zp = self.cell.position[i,2] + self.origin[2]

            atom_type = str(self.cell.atoms_index[int(self.cell.ion[i])])
            radius = SAE.get_atomic_radius1(atom_type)
            R = radius*self.ratio

            if mode != 'ABS':
                if abs(acf.max_bader) >= abs(acf.min_bader):
                    charge_max = abs(acf.max_bader)
                else:
                    charge_max = abs(acf.min_bader)

            # 原子の描画
            atom = vp.sphere(frame=self.crystalframe,pos=(xp,yp,zp), radius=R)

            # 原子の色設定(RGB)を適当に自動化
            if mode == 'ABS':
                if cmax:
                    bader_abs_color  = abs(acf.bader[int(self.cell.sp_j[i])])/abs(float(cmax))
                else:
                    bader_abs_color  = abs(acf.bader[int(self.cell.sp_j[i])])/abs(acf.max_bader)
                atom.red   = bader_abs_color
                atom.green = 0
                atom.blue  = 0
            else:
                if 0 < acf.bader[self.cell.sp_j[i]]: # 電荷が正(増える): 負の価数
                    if cmax:
                        bader_abs_color = abs(acf.bader[int(self.cell.sp_j[i])])/abs(float(cmax))
                    else:
                        bader_abs_color = abs(acf.bader[int(self.cell.sp_j[i])])/charge_max
                    atom.red   = bader_abs_color
                    atom.green = 0
                    atom.blue  = 0
                elif 0 > acf.bader[self.cell.sp_j[i]]: # 電荷が負(減る) : 正の価数
                    if cmin:
                        bader_abs_color = abs(acf.bader[int(self.cell.sp_j[i])])/abs(float(cmin))
                    else:
                        bader_abs_color = abs(acf.bader[int(self.cell.sp_j[i])])/charge_max
                    atom.red   = 0
                    atom.green = 0
                    atom.blue  = bader_abs_color

            # 非スーパセル
           #print "%s %7.3f %7.3f" %( acf.atoms_index_j[i], acf.bader[i], bader_abs_color)

            # スーパーセルインデックスに対応
            print "%s %7.3f %7.3f"\
                    %( acf.atoms_index_j[int(self.cell.sp_j[i])], \
                               acf.bader[int(self.cell.sp_j[i])], bader_abs_color)


################################################################################
if __name__ == '__main__':


    readfile = 'POSCAR'

#   app = wx.App(True,None)
    app = wx.PySimpleApp()

    poscar = SAE.ReadPoscar(readfile)

    potcar = SAE.ReadVaspPotcar()
    acf = SAE.ReadVaspAcf(poscar=poscar,potcar=potcar)

    crystal = CrystalMaker(poscar,origin=[-0.5,-0.5,0])
#   crystal = CrystalMaker(poscar,origin=[-0.5,-0.5,0],times=[2,2,2])
    crystal.plot_atoms()

#   crystal.plot_bader(acf,mode='CHARGE',cmax=CMAX,cmin=CMIN)
#   crystal.plot_bader(acf,cmax=CMAX,cmin=CMIN)
#   crystal.plot_bader(acf)
    crystal.plot_bader(acf,mode='CHARGE')

    crystal.plot_bonds()
    crystal.plot_unit_cell()

