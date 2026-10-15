#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

#!/usr/bin/env python                                                                     
# -*- coding: utf-8 -*- 
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# [機能]
#   D&D で登録したディレクトリ以下のファイルツリーをまとめて XML 形式で
#   リスト化するスクリプト。改行コードの変更があれば windows でも
#   実行が可能。実行時は Win or Unix/Mac で改行コードを変更せよ
#
#   D&D したディレクトリと同じ階層にディレクトリ名でXMLファイルを生成する
#   複数ディレクトリの(まとめてD&Dした)連続実行可能
#
# [Note(makexml.py)]
#
#   出力ファイルの改行はない。改行コードによる動作の違いを吸収する
#   のには実は XML としては正しい仕様。ただし，素でテキストエディタ
#   でみるとわけがわからん。生成した XML ファイルは、XML を理解する
#   ブラウザやエディタで見るとよい
#
#   ElementTree を使うと、アトリビュートは勝手にソートされるので注意
#   XML の仕様としてアトリビュート(プロパティ)の順番はどうでもよい。
#   のでXMLの仕様を満たしているリーダーで読んでいる限りは問題はない
#
#   ファイルパス区切りは Unix/mac では / だが、Windows では \ となる
#   Python はどっちでも（混ざっても）勝手に認識するので問題はない(はず)
#
################################################################################
#
# 2014.12.04 startup
#   makexml.py (2014.12.04 version )をベースにして
#   D&D でディレクトリ名を取得してリストを作る GUI を実装
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
import wx
import xml.etree.ElementTree as ET

#                                                                                         
################################################################################
#import sys
#import optparse
#import re
#import numpy as np
#from copy import deepcopy
################################################################################
# default
#
dtype_OTHER = "binary"
dtype_PF = "/home/dspace/PF9809"
destdir_sucess = "/home/dspace/cr/compdir"
destdir_fail = "/home/dspace/cr/retrydir"
# 最後には / を忘れない
dfile_BASE = "/storage/data/"
ID = "2014T1343"
CREATER = "0001343"
#
#exception      = [ '.DS_Store' ]
exception = ".DS_Store"


################################################################################
# ディレクトリ内のツリー一覧を取得(ディレクトリのみは除外)
#
def fild_all_files(directory):
    #yield root
    for root, dirs, files in os.walk(directory):
        for i in files:
            yield os.path.join(root, i)


#yield os.path.join(i)
# xml ファイル生成部分
#
def makes_xmlfile(dirname):
    #       tree.write('data.xml')
    if os.path.isdir(dirname):
        # D&D されたディレクトリの絶対パス
        PWD = dirname
        # ディレクトリのベース(つまり一つ上のDir)
        PWD_BASE = os.path.basename(PWD)
        bl14b2 = ET.Element("BL14B2", {"version": "1.0", "newline": "CRLF"})
        post = ET.SubElement(bl14b2, "postregist")
        sucess = ET.SubElement(
            post, "success", {"do": "move", "destination": destdir_sucess}
        )
        fail = ET.SubElement(post, "fail", {"do": "move", "destination": destdir_fail})
        proposalID = ET.SubElement(bl14b2, "proposalID")
        proposalID.text = ID
        dubline = ET.SubElement(bl14b2, "dublincore")
        creater = ET.SubElement(dubline, "creater")
        creater.text = CREATER
        rights = ET.SubElement(dubline, "rights")
        rights.text = "close"
        for sfile in fild_all_files(PWD):
            base = os.path.basename(sfile)
            if base != exception:
                root, ext = os.path.splitext(sfile)
                if ext == ".dat":
                    dtype = dtype_PF
                else:
                    dtype = dtype_OTHER
                sfile = sfile.replace(PWD, "")
                dfile = dfile_BASE + proposalID.text + sfile
                dtype = dtype
                data = ET.SubElement(bl14b2, "data", {"file": dfile, "type": dtype})
                obj = ET.SubElement(data, "object")
                typ = ET.SubElement(obj, "type")
                typ.text = "file"
        tree = ET.ElementTree(bl14b2)
        tree.write(PWD + PWD_BASE + ".xml")


# D&D されたらファイル名を取得するクラス
#
class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        #ファイルをドロップする対象
        self.window = window

    #ファイルをドロップするときの処理
    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.window.text.SetValue(file)
            makes_xmlfile(file)


# メインフレーム
#
class MyFrame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, title="makes XML", size=(500, 200))
        p = wx.Panel(self)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        label = wx.StaticText(p, -1, "File name:")
        self.text = wx.TextCtrl(p, -1, "", size=(400, -1))
        sizer.Add(label, 0, wx.ALL, 5)
        sizer.Add(self.text, 0, wx.ALL, 5)
        p.SetSizer(sizer)
        #ドロップする対象をこのフレーム全体にする
        dt = MyFileDropTarget(self)
        self.SetDropTarget(dt)


#   app = wx.App()
if __name__ == "__main__":
    app = wx.PySimpleApp()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
