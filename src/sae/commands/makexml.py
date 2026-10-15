#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# [機能]
#   実行したディレクトリ以下のファイルツリーをまとめて XML 形式で
#   リスト化するスクリプト。
#
# [Note]
#   ElementTree を使うと、アトリビュートは勝手にソートされるので注意
#   XML の仕様としてアトリビュート(プロパティ)の順番はどうでもよい。
#   のでXMLの仕様を満たしているリーダーで読んでいる限りは問題はない
#
#   ファイルパス区切りは Unix/mac では / だが、Windows では \ となる
#   Python はどっちでも（混ざっても）勝手に認識するので問題はない(はず)
#
################################################################################
#
# 2015.02.12
#   Element Tree からlxml へスイッチ
#   xml 出力改行有り(pretty_print)
#
# 2014.12.04
#    startup & complete
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import os
import lxml.etree as ET

#
################################################################################
#import sys
#import optparse
#import re
## ElementTree から lxml へスイッチ (name space は互換のため ET とする)
#import xml.etree.ElementTree as ET
#import numpy as np
#from copy import deepcopy
################################################################################
#
#/home/dspace/cr/
# ConverterRegister.xml
# compdir
# data    <------ XMLファイルのパスに合わせてこの下に課題番号をつけてファイルを入れる
# data_for_analysis
# recover.sh
# retrydir
# srcdir  <--- XMLファイルを入れる
#
#
#/usr/local/SPring8/ConverterRegister.sh を実行する
#
################################################################################
dtype_OTHER = "binary"
dtype_PF = "/home/dspace/PF9809"
destdir_sucess = "/home/dspace/cr/compdir"
destdir_fail = "/home/dspace/cr/retrydir"
# 最後には / を忘れない
dfile_BASE = "/storage/data/"
# dfile_BASE/CREATE/PLUS の順番で追加される (先頭に / を忘れない)
#PLUS           = '/test20150120/Cu-foil'
#PLUS           = '/test20150122/Cu-foil'
#PLUS           = '/test20150122/Cu-foil-2'
#PLUS           = '/test20150312/Zn-foil'
PLUS = "/test20150325/Ni-foil"
#ID             = '2014T1343'
# 標準試料
ID = "2014S0000"
#CREATER        = '0001343'      # 高垣
# 中田
CREATER = "0011765"
#RIGHTS_TAG = 'close'    # 個人用(close)
# 標準試料DATABASE
RIGHTS_TAG = "standard"


################################################################################
def fild_all_files(directory):
    #yield root
    for root, dirs, files in os.walk(directory):
        for i in files:
            yield os.path.join(root, i)


#yield os.path.join(i)
#SCRIPT = PWD+os.path.basename(__file__)
#   creater = ET.SubElement(dubline, 'creater')   # create タグはなくてもOK
#   creater.text = CREATER
# for debug
#   ET.dump(bl14b2)
#   tree.write('data.xml')
#   tree.write(OUTFILE+'.xml')
# for lxml
#   tree.write(OUTFILE+'.xml', pretty_print=True)
# for element tree
def makes_xmlfile(name):
    if os.path.isdir(name):
        OUTFILE = os.path.basename(name)
    else:
        root, ext = os.path.splitext(name)
        OUTFILE = os.path.basename(root)
    bl14b2 = ET.Element("BL14B2", {"version": "1.0", "newline": "CRLF"})
    post = ET.SubElement(bl14b2, "postregist")
    sucess = ET.SubElement(
        post, "success", {"do": "move", "destination": destdir_sucess}
    )
    fail = ET.SubElement(post, "fail", {"do": "move", "destination": destdir_fail})
    proposalID = ET.SubElement(bl14b2, "proposalID")
    proposalID.text = ID
    dubline = ET.SubElement(bl14b2, "dublincore")
    rights = ET.SubElement(dubline, "rights")
    rights.text = RIGHTS_TAG
    ###############################################
    ###############################################
    for sfile in fild_all_files(PWD):
        root, ext = os.path.splitext(sfile)
        if ext == ".dat":
            dtype = dtype_PF
        else:
            dtype = dtype_OTHER
        sfile = sfile.replace(PWD, "")
        dfile = dfile_BASE + proposalID.text + PLUS + sfile
        dtype = dtype
        data = ET.SubElement(bl14b2, "data", {"file": dfile, "type": dtype})
        obj = ET.SubElement(data, "object")
        typ = ET.SubElement(obj, "type")
        typ.text = "file"
    tree = ET.ElementTree(bl14b2)
    tree.write(OUTFILE + ".xml")


################################################################################
if __name__ == "__main__":
    PWD = os.getcwd()
    makes_xmlfile(PWD)
