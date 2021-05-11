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
try:
    from .copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"
##########################################################################

import sys
import os
import gzip

##########################################################################

def read_dataline(name):

    if os.path.exists(name):
        GZIP = False
    elif os.path.exists(name + ".gz"):
        # print("=== GZIP mode is TRUE")
        GZIP = True
    else:
        sys.exit("STOP(read_dataline): " + name + " or " + name + ".gz file not found")

    try:
        if GZIP:
            tmp = gzip.open(name + ".gz")
        else:
            tmp = open(name)
        # datfile = tmp.read().replace('\r','')
        datfile = tmp.read()
        if isinstance(datfile, bytes):
            # for Python 3.x ? (modified 2021.05.10)
            datfile = datfile.decode('ascii')
    except:
        tmp.close()
        sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
    finally:
        tmp.close()

    datlines = datfile.split('\n')
    num = len(datlines) - 1

    # 配列の各要素から CR を削除
#   for i in range(num):
#       print datlines[i]
#      #datlines[i] = datlines[i].rstrip('r')

    return datlines, num


##########################################################################
# read_dataline1
# コメントアウト対応版
#
def read_dataline1(name):

    import re
    comment0_reg = re.compile('^#.*', re.IGNORECASE)
    comment1_reg = re.compile('^!.*', re.IGNORECASE)

    if os.path.exists(name):
        GZIP = False
    elif os.path.exists(name + ".gz"):
        GZIP = True
    else:
        sys.exit(
            "STOP(read_dataline): " + name + " or " + name + ".gz file not found")

    try:
        if GZIP:
            tmp = gzip.open(name + ".gz")
        else:
            tmp = open(name)
#       datfile = tmp.read().replace('\r','')
        datfile = tmp.read()
    except:
        tmp.close()
        sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
    finally:
        tmp.close()

    datalines0 = datfile.split('\n')
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
    return datalines, num

##########################################################################
