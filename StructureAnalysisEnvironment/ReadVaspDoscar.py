#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# ReadDoscar.py
#
#  DOSCAR 読み込みクラス
#   SPIN 情報対応の DOSCAR 読み込みには かならず DOSCAR or vasprun.xml が
#   必要となる
#
#  dos = ReadDoscar(filename)
#
#  [Method]
#
#   ISPIN = dos.get_ispin()
#   LORBIT = dos.get_lorbit()
#   NATOM = dos.get_natom()
#   TITLE =  dos.get_title()
#   EMAX = dos.get_emax()
#   EMIN = dos.get_emin()
#   NEDOS = dos.get_nedos()
#   EFERMI = dos.get_efermi()
#
#   ENG = dos.get_eng()
#   TDOS = dos.get_tdos(spin=0)
#   INTTDOS = dos.get_inttdos(spin=0)
#   PDOS = dos.get_pdos(lm=0,spin=0)
#   LDOS = dos.get_ldos(l=0,spin=0)   # LORIBT=11 の時は自動で要素をsumする
#
#   get_ldos_all
#   get_pdos_all
#
#   get_tdos_spd
#   get_ldos_ion
#
#  Vldos.py のための準備
#
#  拙作 Vldos.pl と同等の機能を python で実装するためのあれこれ
#  Vldos.pl 機能は単品と言うよりは vplot_DOS 関係で matplotlib を
#  使いたいのが目的で、そのための実装とする
#
# 関連クラス)
#  ReadEigenval.py
#  ReadOutcar.py
#
################################################################################
#
# 2015.06.24
#  if statement を少し書き直し
#
# 2015.06.15
#  get_ldos(orbit.atom,spin)
#  にて、orbit に s,p,d 記号でも入力が出来るようにした
#
# 2015.02.25
#  get_emin() で用いているインスタンス変数名を変更
#
# 2015.01.28
#  title の取得における末尾までの空白削除を追加
#
# 2015.01.14
#    PDOS, PDOS_ALL まわりのバグ修正
#
# 2015.01.14
#    get_pdos_all と作成
#    get_pdos におけるループ構造をシンプル化(高速化)
#
# 2015.01.14
#    高速化のために LDOS(get_ldos) と LDOS_ALL(get_ldos_all) の構造を変えた
#    LDOS での無駄な LDOS_ALL 相当のループを排除
#    (ATOM非対応版のときと似たような構造に戻す)
#
# 2015.01.14
#    spin 有りの時に関して致命的なバグ(データー構造そのものの勘違い)
#    を発見したので抜本的に修正
#    正) spin は交互に並ぶ==> s-up,s-down,p-up,p-down の並びになる
#    拙作、Vldos.pl とほぼ同じアルゴリズムに変更
#
# 2015.01.13
#    get_ldos_ion(self,oname,l,spin) Method 追加
#    oname='OUTCAR' を読んでパラメーターをゲットして
#    原子の種類ごとの ldos を取る
#
# 2015.01.13
#
#    dos = ReadDoscar(name)
#    dos.get_LDOS()
#    --> このMethod呼び出し処理がとてつもなく遅いのに気がつく
#        おそらく私のコーディングがアホな（python OOP の理解が足りない）せい
#        多数の原子で毎回呼び出すと信じられないくらい遅い
#        暫定的にプロットの方のルーチンで全原子の描画をしないように変更
#
#    メッソッド名に get_ を追加(変数名との住み分けの容易化のため)
#
#    get_ldos_all メッソッドを追加(メッソド名と戻り値が異なるだけ)
#
#
# 2015.01.11 (sun)
#    細かい修正,まったりと作成
#    全種類の ATOM に対応
#
# 2015.01.10 (sat)
#    基本機能はほぼ完成,まったりと作成
#    ATOM =1 のみ対応
#
# 2015.01.09 1st
#    テスト用テストプログラム(所信表明+ひな形作り始め)
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
__version__    = "0.0.11"
################################################################################

import sys
import os
import gzip
import re
import numpy as np

#from copy import deepcopy

#import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadVaspDoscar(object):

    def __init__(self,name):

        if os.path.exists(name):
            GZIP=False
        elif os.path.exists(name+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+name+" or "+name+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(name+".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+name+" or "+name+".gz does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')

    # DOSCAR のTOTAL-DOS 情報列からspin情報を推測する
    def get_ispin(self):
        tmp = self.datlines[7].split()
        if len(tmp) >= 4: # 4列以上だと SPIN ありは確実
            self.NSPIN = 2
        else:
            self.NSPIN = 1
        return self.NSPIN

    def get_natom(self): # VASP 的には NSIONS に相当
        tmp = self.datlines[0].split()      # NATOM
        self.N_ATOM = int(tmp[0])
        return self.N_ATOM

    def get_title(self): # VASP 的には SYSTEM に相当かと
        src = str(self.datlines[4])  # SYSTEM
        self.SYSTEM = re.sub(' *$','',src)
        return self.SYSTEM

    # EMAX をゲット
    def get_emax(self):
        tmp = self.datlines[5].split()
        self.EMAX = float(tmp[0])  # EMAX
        return self.EMAX

    # EMIN をゲット
    def get_emin(self):
        tmp = self.datlines[5].split()
        self.EMIN = float(tmp[1])  # EMIN
        return self.EMIN

    # NEDOS をゲット
    def get_nedos(self):
        tmp = self.datlines[5].split()
        self.NEDOS = int(tmp[2])  # NEDOS
        return self.NEDOS

    # EFERMI をゲット
    def get_efermi(self):
        tmp = self.datlines[5].split()
        self.efermi = float(tmp[3])  # EFERMI
        return self.efermi

    # LORBIT ( 10 or 11 を返す: 0 は 10 , 1 は 11 を仮定)
    def get_lorbit(self):
        NEDOS = self.get_nedos()
        tmp = self.datlines[6+NEDOS+1].split()
        if len(tmp) >= 10:
            self.LORBIT = 11  # or 1
        else:
            self.LORBIT = 10  # or 0

        return self.LORBIT

    # ENG ( by TDOS )
    def get_eng(self):
        NEDOS = self.get_nedos()
        eng = np.zeros((NEDOS))
        for i in range(NEDOS):
            dos_line = self.datlines[6+i].split()
            eng[i] = float(dos_line[0])

        self.ENG = eng[:]
        return self.ENG

    ############################################################################
    # TOTAL-DOS
    # 注意) spin=0 --> up-spin
    def get_tdos(self,spin=0):

        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            dos_line = self.datlines[6+i].split()

            eng[i] = float(dos_line[0])
            if NSPIN >= 2:
                dos[i,0]    = float(dos_line[1])  # up-sin
                dos[i,1]    = float(dos_line[2])  # down-spin
                intdos[i,0] = float(dos_line[3])
                intdos[i,1] = float(dos_line[4])
            else:
                dos[i,0]    = float(dos_line[1])
                intdos[i,0] = float(dos_line[2])

        self.TDOS = dos[:,spin]
        return self.TDOS

    ############################################################################
    # INT-TOTAL-DOS
    # 注意) spin=0 --> up-spin
    def get_inttdos(self,spin=0):

        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()

        eng = np.zeros((NEDOS))
        dos = np.zeros((NEDOS,NSPIN))
        intdos = np.zeros((NEDOS,NSPIN))

        for i in range(NEDOS):
            dos_line = self.datlines[6+i].split()

            eng[i] = float(dos_line[0])
            if NSPIN >= 2:
                pass
                dos[i,0]    = float(dos_line[1])
                dos[i,1]    = float(dos_line[2])
                intdos[i,0] = float(dos_line[3])
                intdos[i,1] = float(dos_line[4])
            else:
                dos[i,0]    = float(dos_line[1])
                intdos[i,0] = float(dos_line[2])

        self.INTTDOS = intdos[:,spin]
        return self.INTTDOS

    ############################################################################
    # PDOS
    # 注意) atom と spin は 0 から始める(spin=0 --> up-spin)
    # 注意) LDOS までしか計算してなくてもエラーは吐かずに LDOS を返す
    def get_pdos(self,lm=0,atom=0,spin=0):

        NEDOS = self.get_nedos()
        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()

        if LORBIT >= 11:
            lm_max = 9
        else:
            lm_max = 3

        pdos = np.zeros((NEDOS,lm_max,NSPIN))
        eng = np.zeros((NEDOS))

        for i in range(NEDOS):
            tmp = self.datlines[6+NEDOS*(atom+1)+1+i+atom].split()
            eng[i] = float(tmp[0])
            if LORBIT >= 11:
               f = 1
               for lm_local in range(lm_max):
                   # 0: eng
                   # 1: lm=0 s
                   # 2: lm=1 p_y
                   # 3: lm=2 p_z
                   # 4: lm=3 p_x
                   # 5: lm=4 d_xy
                   # 6: lm=5 d_yz
                   # 7: lm=6 d_3z2-r2
                   # 8: lm=7 d_xz
                   # 9: lm=8 d_x2-y2
                   for ispin in range(NSPIN):
                       pdos[i,lm_local,ispin] = float(tmp[f])
                       f += 1
            else:
               f = 1
               for lm_local in range(lm_max):
                   # 0:eng
                   # 1:lm=0: s
                   # 2:lm=1: p
                   # 3:lm=2: d
                   for ispin in range(NSPIN):
                       pdos[i,lm_local,ispin] = float(tmp[f])
                       f += 1

        self.PDOS = pdos[:,lm,spin]
        return self.PDOS

    ############################################################################
    # PDOS_ALL
    # 注意) atom と spin は 0 から始める(spin=0 --> up-spin)
    # 注意) LDOS までしか計算してなくてもエラーは吐かずに LDOS を返す
    def get_pdos_all(self):

        NEDOS = self.get_nedos()
        NATOM = self.get_natom()
        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()

        if LORBIT >= 11:
            lm_max = 9
        else:
            lm_max = 3

        pdos = np.zeros((NEDOS,lm_max,NATOM,NSPIN))
        eng = np.zeros((NEDOS,NATOM))

        for atom0 in range(NATOM):
           for i in range(NEDOS):
               tmp = self.datlines[6+NEDOS*(atom0+1)+1+i+atom0].split()
               eng[i] = float(tmp[0])
               if LORBIT >= 11:
                  f = 1
                  for lm in range(lm_max):
                      # 0:eng
                      # 1:lm=0: s
                      # 2:lm=1: p_y
                      # 3:lm=2: p_z
                      # 4:lm=3: p_x
                      # 5:lm=4: d_xy
                      # 6:lm=5: d_yz
                      # 7:lm=6: d_3z2-r2
                      # 8:lm=7: d_xz
                      # 9:lm=8: d_x2-y2
                      for ispin in range(NSPIN):
                          pdos[i,lm,atom0,ispin] = float(tmp[f])
                          f += 1
               else:
                  f = 1
                  for lm in range(lm_max):
                      # 0:eng
                      # 1:lm=0: s
                      # 2:lm=1: p
                      # 3:lm=2: d
                      for ispin in range(NSPIN):
                          pdos[i,lm,atom0,ispin] = float(tmp[f])
                          f += 1

        self.PDOS = pdos
        return self.PDOS

    ############################################################################
    # LDOS
    # 注意) atom と spin は 0 から始める(spin=0 --> up-spin)
    # 注意) PDOS で計算していても、PDOS から LDOS を算出して返す
    def get_ldos(self,l=0,atom=0,spin=0):

        if isinstance(l, str):
            if l == 's': l=0
            if l == 'p': l=1
            if l == 'd': l=2

        NEDOS = self.get_nedos()
        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()

        l_max = 3
        ldos = np.zeros((NEDOS,l_max,NSPIN))
        eng = np.zeros((NEDOS))

        for i in range(NEDOS):
            tmp = self.datlines[6+NEDOS*(atom+1)+1+i+atom].split()
            eng[i] = float(tmp[0])
            if LORBIT >= 11:
                f = 1
                ### 0:s
                for lm in range(0,1):
                    for ispin in range(NSPIN):
                        ldos[i,0,ispin] = float(tmp[f])
                        f += 1
                ### 1:p_y,2:p_z,3:p_x
                for lm in range(1,4):
                    for ispin in range(NSPIN):
                        ldos[i,1,ispin] = ldos[i,1,ispin] + float(tmp[f])
                        f += 1
                ### 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                for lm in range(4,9):
                    for ispin in range(NSPIN):
                        ldos[i,2,ispin] = ldos[i,2,ispin] + float(tmp[f])
                        f += 1
            else:
                f = 1
                for l in range(l_max):
                    for ispin in range(NSPIN):
                        ldos[i,l,ispin] = float(tmp[f])
                        f += 1

        self.LDOS = ldos[:,l,spin]
        return self.LDOS

    ############################################################################
    # LDOS_ALL
    # spin と l は読んでいるが意味は無い
    # 注意) atom と spin は 0 から始める(spin=0 --> up-spin)
    def get_ldos_all(self):

        NEDOS = self.get_nedos()
        NATOM = self.get_natom()
        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()

        l_max = 3
        ldos = np.zeros((NEDOS,l_max,NATOM,NSPIN))
        eng = np.zeros((NEDOS,NATOM))

        for atom0 in range(NATOM):
            for i in range(NEDOS):
                tmp = self.datlines[6+NEDOS*(atom0+1)+1+i+atom0].split()
                eng[i] = float(tmp[0])
                if LORBIT >= 11:
                    f = 1
                    ### 0:s
                    for lm in range(0,1):
                        for ispin in range(NSPIN):
                            ldos[i,0,atom0,ispin] = \
                                    ldos[i,0,atom0,ispin] + float(tmp[f])
                            f += 1
                    ### 1:p_y,2:p_z,3:p_x
                    for lm in range(1,4):
                        for ispin in range(NSPIN):
                            ldos[i,1,atom0,ispin] = \
                                    ldos[i,1,atom0,ispin] + float(tmp[f])
                            f += 1
                    ### 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                    for lm in range(4,9):
                        for ispin in range(NSPIN):
                            ldos[i,2,atom0,ispin] = \
                                    ldos[i,2,atom0,ispin] + float(tmp[f])
                            f += 1
                else:
                    f = 1
                    for l in range(l_max):
                        for ispin in range(NSPIN):
                            ldos[i,l,atom0,ispin] = tmp[f] # 0:s
                            f += 1

        self.LDOS = ldos
        return self.LDOS

    ############################################################################
    # TDOS_spd, (すべての原子種のs,p,d を足し合わせる,物理的にはほとんど意味が無い解析)
    # 注意) spin は 0 から始める (spin=0 --> up-spin)
    def get_tdos_spd(self,l=0,spin=0):

        NEDOS = self.get_nedos()
        NATOM = self.get_natom()
        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()

        l_max = 3

        tdos_spd = np.zeros((NEDOS,l_max,NSPIN))
        eng = np.zeros((NEDOS,NATOM))

        for atom0 in range(NATOM):
            for i in range(NEDOS):
                tmp = self.datlines[6+NEDOS*(atom0+1)+1+i+atom0].split()
                eng[i] = float(tmp[0])
                if LORBIT >= 11:
                    f = 1
                    ### 0:s
                    for lm in range(0,1):
                        for ispin in range(NSPIN):
                            tdos_spd[i,0,ispin] = \
                                    tdos_spd[i,0,ispin] + float(tmp[f])
                            f += 1
                    ### 1:p_y,2:p_z,3:p_x
                    for lm in range(1,4):
                        for ispin in range(NSPIN):
                            tdos_spd[i,1,ispin] = \
                                    tdos_spd[i,1,ispin] + float(tmp[f])
                            f += 1
                    ### 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                    for lm in range(4,9):
                        for ispin in range(NSPIN):
                            tdos_spd[i,2,ispin] = \
                                    tdos_spd[i,2,ispin] + float(tmp[f])
                            f += 1
                else:
                    f = 1
                    for l in range(l_max):
                        for ispin in range(NSPIN):
                            tdos_spd[i,l,ispin] = \
                                    tdos_spd[i,l,ispin] + float(tmp[f])
                            f += 1

        self.TDOS_SPD = tdos_spd[:,l,spin]
        return self.TDOS_SPD

    ############################################################################
    # LDOS_ion (サイトごとのLDOSを取る), ReadOutcar.py を読む
    # atom の情報を ion の情報へ落としているので atom の loop は必須
    # 注意) ion は 0,1,2,,,,n
    #       spin は 0 から始める (spin=0 --> up-spin)
    def get_ldos_ion(self,l=0,ion=0,spin=0):

        oname='OUTCAR'

        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()
        NEDOS = self.get_nedos()

        import StructureAnalysisEnvironment as SAE
        outcar = SAE.ReadOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()

        l_max = 3
        ldos_ion = np.zeros((NEDOS,l_max,NION,NSPIN))
        eng = np.zeros((NEDOS,NATOM))

        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            for i in range(NEDOS):
                tmp = self.datlines[6+NEDOS*(atom+1)+1+i+atom].split()
                eng[i] = float(tmp[0])
                if LORBIT >= 11:
                    f = 1
                    ### 0:s
                    for lm in range(0,1):
                        for ispin in range(NSPIN):
                            ldos_ion[i,0,ion1,ispin] = \
                                    ldos_ion[i,0,ion1,ispin] + float(tmp[f])
                            f += 1
                    ### 1:p_y,2:p_z,3:p_x
                    for lm in range(1,4):
                        for ispin in range(NSPIN):
                            ldos_ion[i,1,ion1,ispin] = \
                                    ldos_ion[i,1,ion1,ispin] + float(tmp[f])
                            f += 1
                    ### 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                    for lm in range(4,9):
                        for ispin in range(NSPIN):
                            ldos_ion[i,2,ion1,ispin] = \
                                    ldos_ion[i,2,ion1,ispin] + float(tmp[f])
                            f += 1
                else:
                    f = 1
                    for l in range(l_max):
                        for ispin in range(NSPIN):
                            ldos_ion[i,l,ion1,ispin] = \
                                    ldos_ion[i,l,ion1,ispin] + float(tmp[f])
                            f += 1

        self.LDOS_ION = ldos_ion[:,l,ion,spin]
        return self.LDOS_ION

    ############################################################################
    # LDOS_ion (サイトごとのLDOSを取る), ReadOutcar.py を読む
    # LDOS_ion とくらべて method 名と、戻り値だけが異なる
    # atom の情報を ion の情報へ落としているので atom の loop は必須
    # 注意) ion は 0,1,2,,,,n
    #       spin は 0 から始める (spin=0 --> up-spin)
    def get_ldos_ion_all(self):

        oname='OUTCAR'

        NSPIN = self.get_ispin()
        LORBIT = self.get_lorbit()
        NEDOS = self.get_nedos()

        import StructureAnalysisEnvironment as SAE
        outcar = SAE.ReadOutcar(oname)
        NATOM = outcar.get_natom()
        NION = outcar.get_nion()
        ATOMS_J = outcar.get_atoms_j()

        l_max = 3
        ldos_ion = np.zeros((NEDOS,l_max,NION,NSPIN))
        eng = np.zeros((NEDOS,NATOM))

        for atom in range(NATOM):
            ion1 = ATOMS_J[atom]
            for i in range(NEDOS):
                tmp = self.datlines[6+NEDOS*(atom+1)+1+i+atom].split()
                eng[i] = float(tmp[0])
                if LORBIT >= 11:
                    f = 1
                    ### 0:s
                    for lm in range(0,1):
                        for ispin in range(NSPIN):
                            ldos_ion[i,0,ion1,ispin] = \
                                    ldos_ion[i,0,ion1,ispin] + float(tmp[f])
                            f += 1
                    ### 1:p_y,2:p_z,3:p_x
                    for lm in range(1,4):
                        for ispin in range(NSPIN):
                            ldos_ion[i,1,ion1,ispin] = \
                                    ldos_ion[i,1,ion1,ispin] + float(tmp[f])
                            f += 1
                    ### 4:d_xy,5:d_yz,6:d_3z2-r2,7:d_xz,8:d_x2-y2
                    for lm in range(4,9):
                        for ispin in range(NSPIN):
                            ldos_ion[i,2,ion1,ispin] = \
                                    ldos_ion[i,2,ion1,ispin] + float(tmp[f])
                            f += 1
                else:
                    f = 1
                    for l in range(l_max):
                        for ispin in range(NSPIN):
                            ldos_ion[i,l,ion1,ispin] = \
                                    ldos_ion[i,l,ion1,ispin] + float(tmp[f])
                            f += 1

        self.LDOS_ION_ALL = ldos_ion
        return self.LDOS_ION_ALL


################################################################################
if __name__ == '__main__':

    import optparse
    name = 'DOSCAR'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
    )
    options,  args = parser.parse_args()

    if options.INPUT:
        name=options.INPUT

    if len(args) > 0:
        name=args[0]

    dos = ReadVaspDoscar(name)

    NSPIN = dos.get_ispin()
    LORBIT = dos.get_lorbit()
    NATOM = dos.get_natom()
    TITLE =  dos.get_title()
    EMAX = dos.get_emax()
    EMIN = dos.get_emin()
    NEDOS = dos.get_nedos()
    EFERMI = dos.get_efermi()

    print "ISPIN  = ",NSPIN
    print "LORBIT = ",LORBIT
    print "NATOM  = ",NATOM
    print "TITLE  = ",TITLE
    print "EMAX   = ",EMAX
    print "EMIN   = ",EMIN
    print "NEDOS  = ",NEDOS
    print "EFERMI = ",EFERMI


    ENG = dos.get_eng()
   #TDOS = dos.get_tdos(0)                   # spin=0 (up-spin)
    TDOS = dos.get_tdos(spin=0)              # spin=0 (up-spin)

   #INTTDOS = dos.get_inttdos(0)             # spin=0 (up-spin)
    INTTDOS = dos.get_inttdos(spin=0)        # spin=0 (up-spin)


#   LDOS_ION = dos.get_ldos_ion(l=0,ion=4,spin=1)
#   for i in range(NEDOS):
#       print "%12.8f %12.8f" %( ENG[i],LDOS_ION[i] )

#   lm=0
#   atom=0
#   spin=0
#  #spin=1
#   PDOS = dos.get_pdos(lm=lm,atom=atom,spin=spin)
#   for i in range(NEDOS):
#       print "%12.8f %12.8f" %( ENG[i]-EFERMI,PDOS[i] )



################################################################################

