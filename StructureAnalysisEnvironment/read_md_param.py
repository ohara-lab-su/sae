# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 読み込みの事前準備のアホルーチン
#
# [in]     cname : MD ファイル( xyz 形式 ) ファイル名
#
# [return] natom : (セル内)トータルの原子数
# [return] nloop : トータルのループ数
#
################################################################################
#
#
# 2015.02.12
#  細かいバグの修正
#
# 2015.01.07
#  xyz + フォース or xyz の判定のために行数を返す nlist を追加
#  --> したけどすぐにコメントアウトした(必要ない)
#
# 2014.11.18 1st
#
################################################################################
from copyright import *

__status__ = "alpha"
__version__ = "0.0.3"

################################################################################

import sys
import os


# import re
# from numpy import *


def read_md_param(cname):
    ###############################################
    ## Open MD file
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

    ###############################################
    ## DATA のカウント
    ##
    total_line = len(datlines) - 1  # トータルの行数
    natom = int(datlines[0])  # 総原子数

    # loop 数のカウント（アホループ）
    j = 0
    step = natom + 2
    for i in range(0, total_line, step):
        j += 1
    nloop = j

    #   # コメント行をすべてスキップしてリード(テスト,いろいろ確認)
    #   i=0
    #   for l in range(nloop):
    #       i = i+2
    #       for j in range(natom):
    #           print i,datlines[i]
    #           i += 1

    #   tmp = datlines[2].split()  # added 2015.01.07
    #   nlist = len(tmp)           #
    #   return [nloop,natom,nlist] #

    return [nloop, natom]
