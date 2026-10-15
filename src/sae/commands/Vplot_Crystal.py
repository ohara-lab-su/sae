#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   os.system("screencapture screen.png")
#   app.MainLoop()
from __future__ import print_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 結晶構造の描画プログラム
#  初の V(大文字)plot 系コード (2014.11.18)
#
#  1) POSCAR/OUTCAR を読み込む
#  2) アニメーションはしない
#  3) wxPython による GUI 作成の機能追加試験
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.27
#   conv_direct2car --> conv_direct2car0
#
# 2014.12.12
#   コントロール系のウィンドウを追加
#   それに合わせて vpython の描画フレーム関係の処理をクラス&メソッド化
#   ラジオボタン系の追加
#   複数のPanelの導入とそれぞれのPanelの別クラス化
#
# 2014.11.21
#    bond 情報を記述できるようにした
#
# 2014.11.16 1st
#    vpython,wxpython 利用
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
from sae.gui.unit_cell import UnitCellDrawing
import numpy as np
import visual as vp
import wx
import time


#
################################################################################
#from __future__ import division
#import SpaceGroupEnvironment as SGE
#import Image
#import ImageGrab
#import os
#import re
#import optparse
#from copy import deepcopy
################################################################################
def options():
    # INPUT (BASE) filename
    POSCAR = "POSCAR"
    print("INPUT file name    :", POSCAR)
    return [POSCAR, cname]


################################################################################
class MyCtrlFrame(wx.Frame):

    # Frame Init
    # status bar init.
    # menu bar init.
    #self.SetMenuBar()
    # makes root panel
    def __init__(self):
        wx.Frame.__init__(self, None, title="control panel", size=(400, 400))
        self.CreateStatusBar()
        self.SetStatusText("K.NAKADA")
        self.GetStatusBar().SetBackgroundColour(None)
        root_panel = wx.Panel(self, wx.ID_ANY)
        radio_panel = RadioPanel(root_panel)
        bond_panel = BondPanel(root_panel)
        root_layout = wx.BoxSizer(wx.VERTICAL)
        root_layout.Add(radio_panel, 0, wx.GROW | wx.ALL, border=10)
        root_layout.Add(bond_panel, 0, wx.GROW | wx.ALL, border=10)
        root_panel.SetSizer(root_layout)
        root_layout.Fit(root_panel)


################################################################################
class RadioPanel(wx.Panel):

    # Frame にパネルを追加
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.bond_off = wx.RadioButton(self, wx.ID_ANY, "no Bond")
        self.bond_on = wx.RadioButton(self, wx.ID_ANY, "Bond")
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.bond_off, 0, wx.ALIGN_LEFT)
        self.box.Add(self.bond_on, 0, wx.ALIGN_LEFT)
        self.SetSizer(self.box)


################################################################################
class BondPanel(wx.Panel):

    # instance variable (set default)
    ################################
    # bond atom の部品を生成
    # bondAtom
    ################################
    # bond box の部品を生成
    # bond box を生成
    ################################
    # 縦方向にパネルを追加
    #self.sizer = wx.BoxSizer(wx.VERTICAL)
    # Frame にパネルを追加
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.atom1 = 1
        self.atom2 = 4
        self.distance = 2.4
        self.bondAtom1Label = wx.StaticText(self, -1, "atom1:")
        self.bondAtom1Text = wx.TextCtrl(self, -1, size=(50, -1))
        self.bondAtom2Label = wx.StaticText(self, -1, "atom2:")
        self.bondAtom2Text = wx.TextCtrl(self, -1, size=(50, -1))
        self.bondAtom = wx.BoxSizer(wx.HORIZONTAL)
        self.bondAtom.Add(self.bondAtom1Label, 0, wx.ALL, 5)
        self.bondAtom.Add(self.bondAtom1Text, 0, wx.ALL, 5)
        self.bondAtom.Add(self.bondAtom2Label, 0, wx.ALL, 5)
        self.bondAtom.Add(self.bondAtom2Text, 0, wx.ALL, 5)
        self.bondDistanceLabel = wx.StaticText(self, -1, "Bond Length:")
        self.bondDistanceText = wx.TextCtrl(self, -1, size=(150, -1))
        self.bondDistanceButton = wx.Button(self)
        self.bondDistanceButton.SetLabel("submit")
        self.bondDistanceButton.Bind(wx.EVT_BUTTON, self.ctrlOnSubmit)
        self.bondDistance = wx.BoxSizer(wx.HORIZONTAL)
        self.bondDistance.Add(self.bondDistanceLabel, 0, wx.ALL, 5)
        self.bondDistance.Add(self.bondDistanceText, 0, wx.ALL, 5)
        self.bondDistance.Add(self.bondDistanceButton, 0, wx.ALL, 5)
        self.box = wx.StaticBox(self, wx.ID_ANY, "bond infomation")
        self.sizer = wx.StaticBoxSizer(self.box, wx.VERTICAL)
        self.sizer.Add(self.bondAtom, 0, wx.ALIGN_LEFT)
        self.sizer.Add(self.bondDistance, 0, wx.ALIGN_LEFT)
        self.SetSizer(self.sizer)

    def ctrlOnSubmit(self, event):
        self.atom1 = self.bondAtom1Text.GetValue()
        self.atom2 = self.bondAtom2Text.GetValue()
        self.distance = self.bondDistanceText.GetValue()
        print("ATOM1:    ", self.atom1)
        print("ATOM2:    ", self.atom2)
        print("DISTANCE: ", self.distance)


################################################################################
class MyLogFrame(wx.Frame):

    # Frame Init
    # stdout & stderror
    def __init_(self, parent, ID, name):
        wx.Frame.__init__(self, parent, ID, name)
        self.tout = wx.TextCtrl(
            self, -1, value="", style=wx.TE_MULTILINE | wx.TE_READONLY
        )
        sys.stdout = sys.stderr = self
        self.Show()

    def write(self, msg):
        self.tout.AppendText(msg)

    def flush(self):
        pass


################################################################################
class MyCrystalFrame:

    ############################################
    # 結晶描画フレーム インスタンスを生成
    #       screen       = display( background=(0.8,0.8,0.8))
    ############################################
    # ボンドを描くか否か？
    ############################################
    # POSCAR の事前読み込み
    # POSCAR 読み込みのための準備
    # atoms       : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
    # atoms_index : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
    # ion         : 通し番号(max=natom)を与えると原子の種類番号を返す
    # ion_local   : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
    # POSCAR の読み込み
    # VASP の場合はVASP5以上の書式が必要(原子番号情報が必要)
    # Cartesian to Direct 変換
    # 絶対座標系へ変換( cartesian and scale=1.0 ),引数版
    ############################################
    # bond 情報の取得
    ########################################################################
    # 結晶描画の基礎プログラム
    ############################################
    # 単位胞の描画
    #
    #   O = [ -3,-3,0 ] # 結晶描画の単位胞の座標原点
    # 単位胞の描画ルーチン
    ############################################
    # 結晶の描画
    ########################################################################
    # bond の描画
    def CrystalMaker(self):
        from sae.geometry.bonds import BondAnalysis
        from sae.geometry.coordinates import CoordinateTransforms
        from sae.structure.elements import ElementTable
        from sae.vasp.poscar_fields import PoscarFields

        screen = vp.display(title="view window", width=500, height=500)
        crystalframe = vp.frame()
        POSCAR = "POSCAR"
        print("INPUT file name    :", POSCAR)
        bond_FLAG = True
        atom1 = 1
        atom2 = 4
        distance = 2.4
        nion, natom, VASP = PoscarFields().read_poscar_param(POSCAR)
        t = np.zeros((3, 3))
        atoms = []
        atoms_index = []
        ion = np.zeros(natom)
        ion_local = np.zeros(natom)
        position = np.zeros((natom, 3))
        fix = np.zeros((natom, 3), dtype="S")
        title, scale, selective, direct = PoscarFields().read_poscar(
            POSCAR, VASP, t, atoms, atoms_index, ion, ion_local, position, fix
        )
        print("nion =", nion)
        print("atom1=", atom1)
        print("atom2=", atom2)
        if atom1 > nion or atom2 > nion:
            print("set bond_FLAG=False : aotm1 >  nion or atom2 >  nion")
            bond_FLAG = False
        if VASP < 5:
            sys.exit("STOP: VASP version < 5 ")
        if direct:
            ABS = False
            scale, direct = CoordinateTransforms().conv_direct2cara(
                ABS, scale, t, natom, direct, position
            )
        scale = CoordinateTransforms().conv_car2carABSa(
            scale, t, natom, direct, position
        )
        #get_bond_info(atom1,atom2,distance,nion,ion,atoms,atoms_index,position,bondr,bond1,bond2)
        if bond_FLAG:
            bondnum = BondAnalysis().get_bond_info_param(
                atom1, atom2, distance, nion, atoms, position
            )
            print("NUMBER OF BOND     :", bondnum)
            bondr = np.zeros(bondnum)
            bond1 = np.zeros(bondnum, dtype=int)
            bond2 = np.zeros(bondnum, dtype=int)
            BondAnalysis().get_bond_info(
                atom1,
                atom2,
                distance,
                nion,
                atoms,
                atoms_index,
                position,
                bondr,
                bond1,
                bond2,
            )
        # 結晶描画の単位胞の座標原点
        O = [-0.5, -0.5, 0]
        R = 0.05
        # white
        C = [255, 255, 2555]
        UnitCellDrawing().crystal_make_unit(t, O, R, C)
        RATIO = 0.3
        # 描画の原点位置修正
        # 原子の種類を取得(記号)
        # 原子半径を取得
        # 原子番号を取得
        # 原子の色設定(RGB)を適当に自動化
        for i in range(natom):
            xp = position[i, 0] + O[0]
            yp = position[i, 1] + O[1]
            zp = position[i, 2] + O[2]
            atom_type = str(atoms_index[int(ion[i])])
            radius = ElementTable().get_atomic_radius1(atom_type)
            R = radius * RATIO
            num = ElementTable().get_atomic_number1(atom_type)
            atom = vp.sphere(frame=crystalframe, pos=(xp, yp, zp), radius=R)
            atom.red = 0.5 * num * num
            atom.green = 0.1 * num
            atom.blue = 1 / num
        # ボンドの太さ
        if bond_FLAG:
            BR = 0.08
            for num in range(bondnum):
                x1 = position[bond1[num], 0]
                y1 = position[bond1[num], 1]
                z1 = position[bond1[num], 2]
                x2 = position[bond2[num], 0]
                y2 = position[bond2[num], 1]
                z2 = position[bond2[num], 2]
                x12 = x2 - x1
                y12 = y2 - y1
                z12 = z2 - z1
                x0 = x1 + O[0]
                y0 = y1 + O[1]
                z0 = z1 + O[2]
                r1 = bondr[num]
                bond = vp.cylinder(
                    frame=crystalframe,
                    pos=(x0, y0, z0),
                    axis=(x12, y12, z12),
                    radius=BR,
                )
                print(
                    num,
                    bond1[num],
                    "(" + str(atoms_index[int(ion[bond1[num]])]) + ") -",
                    bond2[num],
                    "(" + str(atoms_index[int(ion[bond2[num]])]) + ")",
                    " %10.7f   %11.8f %11.8f %11.8f   %11.8f %11.8f %11.8f"
                    % (r1, x1, y1, z1, x2, y2, z2),
                )


########################################################################
# 画像保存
#       im = ImageGrab.grab(0,0,600,600)
#       im.save('filename.jpg')
# for Mac
################################################################################
# wxPython の基本インスタンスの生成
#   app = wx.App(True,None)
#   # ログ出力ウィンドウ
#   t = LogFrame(None, -1, "log out")
#   t.Show(True)
# コントロールフレーム インスタンスを生成
# 結晶描画フレーム(vpython) & 描画メッソド
if __name__ == "__main__":
    app = wx.PySimpleApp()
    ctrlFrame = MyCtrlFrame()
    ctrlFrame.Show()
    crystalFrame = MyCrystalFrame()
    crystalFrame.CrystalMaker()
    time.sleep(1)
