#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
################################################################################
from __future__ import print_function
from sae.openmx.vps import ReadMxVps

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# DAT_DATA13/VPS ディレクトリからファイル名をゲットして
# ファイル名のVPSから valence の電子数を入手するだけ
#
# 引数は 元素名
# デフォルトモードは PBE
# Higth と default など複数あるときはデフォルトをデフォルトチョイス
#
################################################################################
#
# 2018.08.23
#  Python2/3 両対応
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
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse


#
################################################################################
#import re
#import numpy as np
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE
################################################################################
# default names
# オプション処理
# default data path
# DFT_DATA path が存在しない時は 環境変数 DATAPATH を選択
def options():
    defaultatom = "C"
    defaultpot = "PBE"
    defaultver = "13"
    parser = optparse.OptionParser()
    parser.add_option("-a", "--atom", dest="ATOM", default=defaultatom)
    parser.add_option("-p", "--potential", dest="POT", default=defaultpot)
    parser.add_option("-v", "--version", dest="VER", default=defaultver)
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
    filename = options.ATOM + "_" + options.POT + options.VER
    if len(args) > 0:
        filename = args[0]
    return [DFT_DATAPATH, options.ATOM, options.POT, options.VER, filename]


#   data = '../DFT_DATA13'
#   atom = 'C'
#   pot  = 'PBE'
#   name = 'C_PBE13'
################################################################################
if __name__ == "__main__":
    opts = options()
    data, atom, pot, ver, name = opts
    fullname = data + "/VPS/" + name + ".vps"
    if not os.path.exists(fullname):
        SUFFIX = "S"
        name = name + SUFFIX
        fullname = data + "/VPS/" + name + ".vps"
        if not os.path.exists(fullname):
            SUFFIX = "H"
            name = name + SUFFIX
            fullname = data + "/VPS/" + name + ".vps"
    vps = ReadMxVps(fullname)
    electron = vps.get_valence_electron()
    print("DATAPATH        :", data)
    print("VER             :", ver)
    print("POT             :", pot)
    print("ATOM            :", atom)
    print("VPS             :", name)
    print("PATH            :", fullname)
    print("num of electron :", electron)
