#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# find_datfile
#
#  指定suffixのファイルがカレントに一つの時はそのファイル名を返すルーチンへ
#  変更
#
################################################################################
#
# 2015.02.26
#  指定suffixのファイルがカレントに一つの時はそのファイル名を返すルーチンへ
#  変更
#
# 2015.02.26
#   startup
#    openmx.dat ファイルがカレントディレクトリに一つの場合は
#    ファイル名(この場合 openmx ) を取得して返す関数
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
__version__    = "0.0.1"
################################################################################

#import sys
#import os
#import gzip

import re
import glob


################################################################################
def find_datfile(suffix):

    filelist = glob.glob("*."+suffix)
    if len(filelist) == 1:
        datname = re.sub('.'+suffix,'',filelist[0])
    else:
        pass

    return datname

################################################################################
if __name__ == '__main__':
    try:
        datname = find_datfile('dat')
        print datname
    except:
        pass

