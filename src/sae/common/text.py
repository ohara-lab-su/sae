#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# del_commentout()
# コメントアウト削除ルーチン
#
################################################################################
#
# 2015.06.19 1st
#
################################################################################
################################################################################
# import sys
# import os
# from numpy import *
# from copy import deepcopy
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 汎用データーリード
#   read_list との違いは cut 引数があるか否か
#
# cut 引数
#    データーファイルの読み込みスタート行を指定できる
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2014.11.19 1st
#
################################################################################
################################################################################
########################################
## find_list は (dimension)次元配列
## 好きな次元で利用可能
##
########################################
## find_list は2次元配列
##
########################################
## find_list は5次元配列
##
########################################
# exsample)
# Q
# S(Q) RMC++
# renormalized experimental S(Q)
# original exp. S(Q)
# additive backgroupd
# -*- coding: utf-8 -*-
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# read_dataline(name)
#
#  name ファイル or name.gz ファイルを読み込んで
#  datlines[num] 配列に放り込む関数
#  配列数 num および、datalines 配列を戻り値にする
#
##########################################################################
#
# 2015.08.10
#  CR を削除するようにした
#
# 2015.06.18
#  コメントアウト対応版を複数のコメント(# or !)にアップデート
#
# 2015.05.08
#  コメントアウト対応版 read_datline1 を作成
#    nline をカウント数も、dataline へも放り込みも コメントアウトは除く
#
# 2015.02.25
#   startup
#   わりと多用するので class のコンストラクタ部分から分離
#   関数で呼び出すようにする
#
##########################################################################
##########################################################################
##########################################################################
##########################################################################
# read_dataline1
# コメントアウト対応版
#
##########################################################################
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# コメントアウト(#) 対応のリード(アホ仕様)
#
################################################################################
#
# 2014.11.05 1st
#
################################################################################
################################################################################
########################################
## find_list は1次元配列
##
########################################
## find_list は3次元配列(num,atom,radius)
##
########################################
## find_list は4次元配列(atom,data_x,data_y,data_z)
##
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# list 読み込みの事前準備
#   (注意) コメント行だろうがなんだろうが、一行としてカウントする
#
# [in] cname      : 読み込みファイル名
#
# [return] nlist : リスト数
#
################################################################################
#
# 2014.11.05 1st
#
################################################################################
################################################################################
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# read_rowe(filename,Column)
#
#  filename ファイル の Column 番目の row数を返す
#  結局ファイルまるごと読んでしまうアホ仕様
#
################################################################################
#
# 2015.07.01
#   startup
#
################################################################################
################################################################################
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import re
import sys
import os
from numpy import *
from copy import deepcopy

comment_reg = re.compile("^#.*", re.IGNORECASE)
import gzip

comment_reg = re.compile("^#.*", re.IGNORECASE)


class TextFiles:

    def del_comment(self, data, comment="!"):
        newdata = []
        for i in range(len(data)):
            newdata.append(re.sub(comment + ".*", "", data[i]))
        num = len(newdata)
        return (newdata, num)

    def read_dat(self, name, dimension, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            for k in range(dimension):
                dat[i, k] = tmp[k]
            j += 1
        nlist = j
        return nlist

    def read_dat2(self, name, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            dat[i, 0] = tmp[0]
            dat[i, 1] = tmp[1]
            j += 1
        nlist = j
        return nlist

    def read_dat5(self, name, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            dat[i, 0] = tmp[0]
            dat[i, 1] = tmp[1]
            dat[i, 2] = tmp[2]
            dat[i, 3] = tmp[3]
            dat[i, 4] = tmp[4]
            j += 1
        nlist = j
        return nlist

    def read_dataline(self, name):
        if os.path.exists(name):
            GZIP = False
        # print("=== GZIP mode is TRUE")
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit(
                "STOP(read_dataline): " + name + " or " + name + ".gz file not found"
            )
        # datfile = tmp.read().replace('\r','')
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
            # for Python 3.x ? (modified 2021.05.10)
            if isinstance(datfile, bytes):
                datfile = datfile.decode("ascii")
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        # 配列の各要素から CR を削除
        #   for i in range(num):
        #       print datlines[i]
        #      #datlines[i] = datlines[i].rstrip('r')
        return (datlines, num)

    def read_dataline1(self, name):
        import re

        comment0_reg = re.compile("^#.*", re.IGNORECASE)
        comment1_reg = re.compile("^!.*", re.IGNORECASE)
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit(
                "STOP(read_dataline): " + name + " or " + name + ".gz file not found"
            )
        #       datfile = tmp.read().replace('\r','')
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        datalines0 = datfile.split("\n")
        num0 = len(datalines0) - 1
        #   # 配列の各要素から CR を削除
        #   for i in range(num0):
        #       datalines0[i] = datalines0[i].rstrip('r')
        j = 0
        datalines = []
        for i in range(num0):
            if not bool(comment0_reg.match(datalines0[i])):
                if not bool(comment1_reg.match(datalines0[i])):
                    datalines.append(datalines0[i])
                    j += 1
        num = j
        return (datalines, num)

    def read_list1(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                find_list[j] = tmp[0]
                j += 1
        nlist = j
        return nlist

    def read_list3(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        tmp = open(name)
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                if not int(len(tmp)) >= 3:
                    sys.exit(name + " Format Error: datalines < 3 ")
                find_list[j, 0] = tmp[0]
                find_list[j, 1] = tmp[1]
                find_list[j, 2] = tmp[2]
                j += 1
        nlist = j
        return nlist

    def read_list4(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        tmp = open(name)
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                if not int(len(tmp)) >= 4:
                    sys.exit(name + " Format Error: datalines < 4 ")
                find_list[j, 0] = tmp[0]
                find_list[j, 1] = tmp[1]
                find_list[j, 2] = tmp[2]
                find_list[j, 3] = tmp[3]
                j += 1
        nlist = j
        return nlist

    def read_list_param(self, name):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datlines = datalist.split("\n")
        nlist = int(len(datlines)) - 1
        return nlist

    def read_row(self, name, column=0):
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + name + " or " + name + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        row = len(datlines[column].split())
        return (row, num)
