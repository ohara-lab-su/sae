#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# find_datfile(suffix)
#
#  指定suffixのファイルがカレントに一つの時はそのファイル名を返すルーチンへ
#  変更
#
#  注意) suffix には . は付かないで入力
#        もし . が付いていたら自動で一度 . を落とす
#
################################################################################
#
# 2015.05.21
#  find_datfile() の超シンプル版 find_datfile1() を追加
#
# 2015.03.16
#  ライブラリとしてではなく実行プログラムとしてみたときに、引数処理を
#  してなかったので修正
#
# 2015.03.10
#  複数ファイルを纏めて返すバージョン find_datfiles() を追加
#
# 2015.03.03
#  拡張子の自動 . 削除＆追加ルーチンにバグを発見したので直した
#
# 2015.03.03
#  複数の suffix ファイルが有るときに return する変数を None で返すようにした
#
# 2015.03.03
#  引数の suffix に . をつけても同じように動作するように改変
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
__version__    = "0.0.6"
################################################################################

#import sys
#import os
#import gzip

import re
import glob
import optparse

################################################################################
def find_datfile(suffix):

    suffix0 = re.sub('^\.','',suffix)
    filelist = glob.glob("*."+suffix0)
    datname=None
    if len(filelist) == 1:
        datname = re.sub('.'+suffix0,'',filelist[0])
    else:
        pass

    return datname

################################################################################
def find_datfile1(tail):

    filelist = glob.glob("*"+tail)
    datname = None
    if len(filelist) == 1:
        datname = filelist[0]

    return datname

################################################################################
def find_datfiles(suffix):

    filelist = glob.glob("*."+str(suffix))
    datnames=None
    datnames = []
    for i in filelist:
        datnames.append(re.sub('.'+str(suffix),'',i))

    return datnames

################################################################################
if __name__ == '__main__':

    suffix = 'dat'
    parser = optparse.OptionParser()
    parser.add_option( '-s','--suffix',)
    options, args = parser.parse_args()

    if len(args) >0:
        suffix = args[0]

    if options.suffix:
        suffix = options.suffix

    try:
        datname = find_datfile(suffix)
        print datname
    except:
        pass

