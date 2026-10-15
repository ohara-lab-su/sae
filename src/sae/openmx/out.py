#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
# *.out ファイル 読み込み ReadMxOut
#
#  ReadMxDatMethod
#              ---> ReadMxOut
#              ---> ReadMxDat
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.26
#  sample コードにおいて name と suffix を分離(今後の基本方針)
#
# 2015.02.26  ReadMxOut.get_uele()
#   ReadMxOut.get_uele() のデーター取得方法を変更
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
# ------------------------------- superclass にmethodを移行/継承化
# 2015.02.24
#  *.dat を superclass化したことで *.out (ReadMxOut)の重複 method を整理整頓
#
# 2015.02.24
#  1st time
#    とりあえず Utot と Uele の ION ステップごとと SCF 毎の結果を
#    整理して抽出するだけのクラス/メッソドをとりあえず準備
#
################################################################################
################################################################################
# import SpaceGroupEnvironment as SGE
# sys.path.append('../..')
################################################################################
################################################################################
#   for i in range(n_ion_loop):
#   print nspin
#   print title
#   for i in range(nion):
#       print atoms_j[i]
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.dat_methods import ReadMxDatMethod
from sae.structure.base import Method
import sys
import gzip
import os
import re
import optparse
import numpy as np

try:
    ReadMxDatMethod = ReadMxDatMethod
except ImportError:
    Method = Method
    ReadMxDatMethod = ReadMxDatMethod


###################################
###################################
# イオンループの数
# SCF MD=* 項目の * の最大値を引き抜く
# 同一 MD=* 番号が連続して現れても関係なく * の最大を取る
###################################
# イオンループ毎の Total Energy
###################################
# SCFループの最大数
###################################
# イオンループ毎のさらにSCFループごとの Uele(bandエネルギー) の抽出
# 同一 MD=* 番号が現れた時は最後の SCF ループのみを取り出す
class ReadMxOut(ReadMxDatMethod):

    def __init__(self, cname):
        if os.path.exists(cname):
            GZIP = False
        elif os.path.exists(cname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + cname + " or " + cname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(cname + ".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " or " + cname + ".gz does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    # print self.n_ion_loop, self.datlines[i]
    # print "MAX",self.n_ion_loop
    def get_n_ion_loop(self):
        md_text = ".*SCF.*MD="
        md_reg = re.compile(md_text)
        self.n_ion_loop = 0
        for i in range(self.num):
            if bool(md_reg.match(self.datlines[i])):
                tmp = int(re.sub(md_text, "", self.datlines[i]))
                if self.n_ion_loop < tmp:
                    self.n_ion_loop = tmp
        return self.n_ion_loop

    def get_utot(self):
        n_ion_loop = self.get_n_ion_loop()
        self.utot = np.zeros(n_ion_loop)
        tot_reg = re.compile(".*Utot\\..*")
        j = 0
        for i in range(self.num):
            if bool(tot_reg.match(self.datlines[i])):
                self.utot[j] = self.datlines[i].split()[1]
                j += 1
        return self.utot

    def get_max_n_scf(self):
        scf_txt = ".*SCF="
        scf_reg = re.compile(scf_txt)
        self.max_n_scf = 0
        for i in range(self.num):
            if bool(scf_reg.match(self.datlines[i])):
                tmp = int(re.sub(scf_txt, "", self.datlines[i]).split()[0])
                if self.max_n_scf < tmp:
                    self.max_n_scf = tmp
        return self.max_n_scf

    def get_uele(self):
        md_start_txt = ".*SCF.*at MD="
        md_start_reg = re.compile(md_start_txt)
        scf_txt = ".*SCF=.*Uele="
        scf_reg = re.compile(scf_txt)
        n_ion_loop = self.get_n_ion_loop()
        max_n_scf = self.get_max_n_scf()
        self.uele = np.zeros((n_ion_loop, max_n_scf))
        self.uele_index = np.zeros(n_ion_loop, dtype=int)
        i = 0
        # MD= 行を見つけたらスタート
        # print ''
        while 1:
            # SCF行が始まるまでジャンプ
            # SCF 行がある間だけ読み込み
            if bool(md_start_reg.match(self.datlines[i])):
                md = int(re.sub(md_start_txt, "", self.datlines[i])) - 1
                while not bool(scf_reg.match(self.datlines[i])):
                    i += 1
                scf = 0
                # print md,scf,uele0
                while bool(scf_reg.match(self.datlines[i])):
                    uele0 = float(re.sub(scf_reg, "", self.datlines[i]))
                    self.uele[md, scf] = uele0
                    self.uele_index[md] = scf
                    scf += 1
                    i += 1
            i += 1
            if self.num == i:
                break
        return (self.uele, self.uele_index)
