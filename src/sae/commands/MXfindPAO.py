#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#   vps = SAE.ReadMxVps(fullname)
#   electron = vps.get_valence_electron()
################################################################################
from __future__ import print_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# DAT_DATA13/PAO ディレクトリの PAO ファイル検索支援
#
# -a オプションで元素名を指定するとその元素名を持っている PAO ファイルを探す
#
# DATA_PATH はある程度自動検索
#
################################################################################
#
# 2018.08.23
#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#  Python2/3 両対応
#   dircache(python2) モジュール代理で使っている glob(python3) の部分のテストはしてない
#  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# 2015.03.11
#  DATA_PATH の検索関係を少し整備しなおし
#
# 2015.02.09 1st
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import re

#
################################################################################
# for Python2.x module
try:
    import dircache
except:
    import glob

    pass
import optparse


#import numpy as np
#import glob
#import re
#from copy import deepcopy
#import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE
################################################################################
# default value
# オプション処理
# default data path
# DFT_DATA path が存在しない時は 環境変数 DATAPATH を選択
#   filename=options.ATOM+'_'+options.POT+options.VER
def options():
    defaultatom = "C"
    defaultpot = "PBE"
    defaultver = "13"
    defaultcut = "5.0"
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom", dest="ATOM", default=defaultatom)
    parser.add_option("-p", "--potential", dest="POT", default=defaultpot)
    parser.add_option("-v", "--version", dest="VER", default=defaultver)
    parser.add_option("-c", "--cut", dest="CUT", default=defaultcut)
    options, args = parser.parse_args()
    DFT_DATA_BASE = "DFT_DATA"
    DFT_DATA = DFT_DATA_BASE + options.VER
    DFT_DATAPATH = "../" + DFT_DATA
    HOMEPATH = os.environ.get("HOME", "")
    # OpenMX DATA 環境変数
    DATAPATH = os.environ.get("OPENMXDATAPATH", "")
    # カレントより一つ上検索
    if not os.path.exists(DFT_DATAPATH):
        # カレントを検索
        if os.path.exists("./" + DFT_DATA):
            DFT_DATAPATH = "./" + DFT_DATA
        # 環境変数検索
        elif DATAPATH:
            DFT_DATAPATH = DATAPATH
        # ホーム直下検索
        elif os.path.exists(HOMEPATH + "/" + DFT_DATA):
            DFT_DATAPATH = HOMEPATH + "/" + DFT_DATA
        # カレントより２つ上検索
        elif os.path.exists("../" + DFT_DATAPATH):
            DFT_DATAPATH = "../" + DFT_DATAPATH
        else:
            sys.exit("STOP: " + DFT_DATA + " directory not found")
    filename = options.ATOM + options.CUT
    if len(args) > 0:
        filename = args[0]
    return [DFT_DATAPATH, options.ATOM, options.POT, options.VER, options.CUT, filename]


#   data = '../DFT_DATA13'
#   atom = 'C'
#   pot  = 'PBE'
#   ver  = '13'
#   name = 'C_PBE13'
################################################################################
if __name__ == "__main__":
    opts = options()
    data, atom, pot, ver, cut, name = opts
    fullname = data + "/PAO/" + name + ".pao"
    SUFFIX = ""
    if not os.path.exists(fullname):
        SUFFIX = "S"
        fullname = data + "/PAO/" + name + SUFFIX + ".pao"
        if not os.path.exists(fullname):
            SUFFIX = "H"
            fullname = data + "/PAO/" + name + SUFFIX + ".pao"
            # 正規表現でPAOディレクトリ内の検索
            if not os.path.exists(fullname):
                SUFFIX = "dir"
                paolist = []
                pao_txt = atom + "[0-9].*" + "\\.pao"
                pao_reg = re.compile(pao_txt)
                ## 未テスト
                try:
                    for file in dircache.listdir(data + "/PAO/"):
                        if pao_reg.search(file):
                            paolist.append(file)
                except:
                    for file in glob.glob(data + "/PAO/*"):
                        if pao_reg.search(file):
                            paolist.append(file)
    if SUFFIX != "dir":
        print("CUT  :", cut)
        print("PATH :", fullname)
        print("PAO  :", name)
    else:
        for i in range(len(paolist)):
            print(paolist[i])
