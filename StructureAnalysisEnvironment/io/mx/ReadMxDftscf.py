#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
# *.DFTSCF ファイル 読み込み
#
#  ReadMxDatMethod -- ReadMxOut -- ReadMxDftscf
#                  -- ReadMxDat
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.30
#   == None --> is None
#
# 2015.03.13
#  get_uele()
#  IONループが途中で終了した時の最後のSCFループの情報を配列に放り込むように変更
#
# 2015.03.13
#  get_uele()
#    MD内の SCF ループが人少なく表示されるバグを発見＆修正
#
# 2015.03.12
#  get_uele()
#   IONループが0のとき（一回目のSCFループの時)
#    結果を途中でも書きだすように修正
#
# 2015.03.12
#   startup
#
#   オーバーライトするもの
#     get_n_ion_loop()
#     get_uele()
#
#   データーが途中で止まっていても MD ループ等の情報を正しく読めるように修正
#
################################################################################
from __future__ import print_function

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
# import gzip
import os
import re
import optparse
import numpy as np

# import SpaceGroupEnvironment as SGE
try:
    sys.path.append('../../')
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.io.mx.ReadMxOut import ReadMxOut
except ImportError:
    import StructureAnalysisEnvironment as SAEnv
    from StructureAnalysisEnvironment.io import *
    from StructureAnalysisEnvironment.io.mx.ReadMxOut import ReadMxOut


################################################################################
class ReadMxDftscf(ReadMxOut):

    ###################################
    def __init__(self, cname):

        self.datlines, self.num = SAEnv.read_dataline(cname)

    ###################################
    # (終了した)イオンループの数
    #  IONループが終了したあとの Total energy 出力の項目をカウントする
    #  SCFループが途中のIONループはカウントしない
    def get_n_ion_loop(self):
        md_text = '.*Total energy.*at MD ='
        md_reg = re.compile(md_text)
        self.n_ion_loop = 0
        for i in range(self.num):
            if bool(md_reg.match(self.datlines[i])):
                tmp = int(re.sub(md_text, '', self.datlines[i]))
                if self.n_ion_loop < tmp:
                    self.n_ion_loop = tmp
            # print self.n_ion_loop, self.datlines[i]
        # print "MAX",self.n_ion_loop
        return self.n_ion_loop

    ###################################
    # イオンループ毎のさらにSCFループごとの Uele(bandエネルギー) の抽出
    # 同一 MD=* 番号が現れた時は最後の SCF ループのみを取り出す
    def get_uele(self):

        md_start_txt = '.*SCF.*at MD='
        md_start_reg = re.compile(md_start_txt)

        scf_txt = '.*SCF=.*Uele='
        scf_reg = re.compile(scf_txt)

        n_ion_loop = self.get_n_ion_loop()
        max_n_scf = self.get_max_n_scf()

        self.uele = np.zeros((n_ion_loop + 1, max_n_scf))
        self.uele_index = np.zeros((n_ion_loop + 1), dtype=int)

        if not n_ion_loop == 0:
            i = 0
            md = 0
            while 1:
                # MD= 行を見つけたらスタート
                if bool(md_start_reg.match(self.datlines[i])):
                    # md = int(re.sub(md_start_txt,'',self.datlines[i])) - 1
                    # SCF行が始まるまでジャンプ
                    while not bool(scf_reg.match(self.datlines[i])): i += 1
                    scf = 0
                    # SCF 行がある間だけ読み込み
                    while bool(scf_reg.match(self.datlines[i])):
                        uele0 = float(re.sub(scf_reg, '', self.datlines[i]))
                        # print " %d %d %15.12f" %( md,scf,uele0 )
                        self.uele[md, scf] = uele0
                        self.uele_index[md] = scf
                        scf += 1
                        i += 1
                    # print ''
                    self.uele_index[md] = scf
                    md += 1
                i += 1
                if md == n_ion_loop:
                    # 最後のMDループで SCF が終了してない途中のSCF情報
                    while 1:
                        if bool(md_start_reg.match(self.datlines[i])):
                            while not bool(scf_reg.match(self.datlines[i])): i += 1
                            scf = 0
                            while bool(scf_reg.match(self.datlines[i])):
                                uele0 = float(re.sub(scf_reg, '', self.datlines[i]))
                                self.uele[md, scf] = uele0
                                self.uele_index[md] = scf
                                # print " %d %d %15.12f" %( md,scf,uele0 )
                                scf += 1
                                i += 1
                            self.uele_index[md] = scf
                            break
                        i += 1
                    break
        else:
            # MD ループが一度も終了したことがないときの処理
            i = 0
            uele0 = []
            while 1:
                if bool(md_start_reg.match(self.datlines[i])):
                    while not bool(scf_reg.match(self.datlines[i])): i += 1
                    while bool(scf_reg.match(self.datlines[i])):
                        uele0.append(float(re.sub(scf_reg, '', self.datlines[i])))
                        i += 1
                    break
                i += 1
            for j in range(len(uele0)):
                self.uele[0, j] = uele0[j]
            self.uele_index[0] = len(uele0)

        return self.uele, self.uele_index


################################################################################
if __name__ == '__main__':

    name = 'openmx'
    suffix = '.out'
    mxname = name + suffix

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    # デフォルト名より最適なデフォルトファイル名の推定ルーチン
    if not os.path.exists(mxname):
        try:
            name0 = SAEnv.find_datfile('dat')  # *.dat はかならずあるのでそれをトリガーに
            if not name0 is None:
                name = name0
                mxname = name + suffix
        except:
            pass

    # オプションでファイル名を入力した時
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub('\.out$', '', mxname)
        mxname = name + suffix

    if len(args) > 0:
        name = args[0]
        name = re.sub('\.out$', '', name)

    mxname = name + suffix

    # 計算途中での DFTSCF ファイル読み込み
    if not os.path.exists(mxname):
        suffix = '.DFTSCF'
        mxname = name + suffix

    dftscf = ReadMxDftscf(mxname)

    n_ion_loop = dftscf.get_n_ion_loop()
    max_n_scf = dftscf.get_max_n_scf()

    utot = dftscf.get_utot()
    uele, uele_index = dftscf.get_uele()

    print("N_ION_LOOP %s" % str(n_ion_loop))
    print("MAX_N_SCF %s" % str(max_n_scf))

    if not n_ion_loop == 0:
        for md in range(n_ion_loop):
            # print "***************** md = ",md+1,'**********************'
            print("***************** md = %s **********************" % md + 1)
            for scf in range(uele_index[md]):
                print("    scf=%d, Uele = %15.12f" % (scf + 1, uele[md, scf]))
        # print " Utot = %15.12f" %(utot[md])
        # 計算途中の最後のSCFループを表示
        md = n_ion_loop
        print("***************** md = %s **********************" % md + 1)
        for scf in range(uele_index[md]):
            print("    scf=%d, Uele = %15.12f" % (scf + 1, uele[md, scf]))
    else:
        print("***************** md = %s **********************" % 1)
        for scf in range(uele_index[0]):
            print("    scf=%d, Uele = %15.12f" % (scf + 1, uele[0, scf]))
