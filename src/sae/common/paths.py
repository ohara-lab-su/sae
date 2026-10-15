#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
# 2018.08.15
#  Python2/3 両対応
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
################################################################################
# import sys
# import os
# import gzip
################################################################################
# suffix が dot 付きだったときは dot を削除してから *.suffix を探す
# 複数見つけた時および見つけなかった時は None を返す
#
################################################################################
# suffix に対しての事後処理をせずに *suffix を探す
#
################################################################################
#  *.suffix を探す（複数ファイルを返す)
#
################################################################################
#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# find_suffix(name)
#
# 基本仕様
#    find_datfile.py の逆
#    特定のファイル名を引いたら suffix いろいろを探してくれる
#
#    >ls case.dos*
#    case.dos1
#    case.dos2
#      .
#      .
#    find_datfile() と異なり、こちらは最初から複数ファイルが前提
#
# find_suffix1(name)              # ls name*
# find_suffix2(head,tail)         # ls head*tail
# find_suffix3(head,tail,delete)  # ls head* | sed 's/delete//'
#                                 # tail が None のときは tail を delete として動作
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.03.27
#  spin + ev のときに suffix3 が正しく動いていないバグを修正
#
# 2015.03.25
#  tail が None のときの処理を追加
#
# 2015.03.24
#   startup
#
################################################################################
################################################################################
# import sys
# import os
# import gzip
################################################################################
# ls name*
#
################################################################################
# ls head*tail
#
################################################################################
# ls head* | sed 's/tail//'
#
################################################################################
#   tail = 'None'
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import re
import glob
import optparse


class FileDiscovery:

    def find_datfile(self, suffix):
        suffix0 = re.sub("^\\.", "", suffix)
        filelist = glob.glob("*." + suffix0)
        datname = None
        if len(filelist) == 1:
            datname = re.sub("." + suffix0, "", filelist[0])
        return datname

    def find_datfile1(self, tail):
        filelist = glob.glob("*" + tail)
        datname = None
        if len(filelist) == 1:
            datname = filelist[0]
        return datname

    def find_datfiles(self, suffix):
        filelist = glob.glob("*." + str(suffix))
        datnames = None
        datnames = []
        for i in filelist:
            datnames.append(re.sub("." + str(suffix), "", i))
        return datnames

    def find_suffix1(self, name):
        files = glob.glob(str(name) + "*")
        return files

    def find_suffix2(self, head, tail):
        filelist = glob.glob(str(head) + "*" + str(tail))
        return filelist

    def find_suffix3(self, head="case", tail="ev", delete="ev"):
        if not tail == "None":
            filelist = glob.glob(str(head) + "*" + str(tail) + "*")
        else:
            files = glob.glob(str(head) + "*")
            filelist = []
            for i in files:
                filelist.append(re.sub(delete, "", i))
            filelist = sorted(set(filelist), key=filelist.index)
        return filelist
