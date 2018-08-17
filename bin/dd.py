#!/usr/bin/env python                                                                     
# -*- coding: utf-8 -*- 
################################################################################
# K.NAKADA, kengo.nakada@gmail.com, kengo.nakada@spring8.or.jp
#
# [機能]
#   D&D で登録したディレクトリ以下のファイルツリーをまとめて XML 形式で
#   リスト化するスクリプト。
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
# 2018.08.17
#  Python2/3 両対応
#
# 2014.12.09
#   UserID などの各項目を GUI 上から修正できるように改変
#
# 2014.12.04 startup
#   makexml.py (2014.12.04 version )をベースにして
#   D&D でディレクトリ名を取得してリストを作る GUI を実装
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2014, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.1"                                                                  
################################################################################

#import sys
import os
#import optparse
#import re
import wx

import xml.etree.ElementTree as ET
#import numpy as np
#from copy import deepcopy


################################################################################
# default
#
dtype_OTHER    = 'binary'
dtype_PF       = '/home/dspace/PF9809'
destdir_sucess = '/home/dspace/cr/compdir'
destdir_fail   = '/home/dspace/cr/retrydir'

dfile_BASE     = '/storage/data/'       # 最後には / を忘れない

#ID             = '2014T1343'
ID             = '2014S0000 '
#CREATER        = '0001343'
CREATER        = '0011765'
#
#exception      = [ '.DS_Store' ]
exception      = '.DS_Store'
################################################################################

# xml ファイル生成部分
#
# self.ID      = ID
# self.userID  = CREATER
# self.sucess  = destdir_sucess
# self.fail    = destdir_fail
# self.storage = dfile_BASE
#
def makes_xmlfile(dirname,ID,CREATER,destdir_sucess,destdir_fail,dfile_BASE):

    if os.path.isdir(dirname):
        PWD      = dirname               # D&D されたディレクトリの絶対パス
        PWD_BASE = os.path.basename(PWD) # ディレクトリのベース(つまり一つ上のDir)
   
        bl14b2 = ET.Element('BL14B2',{'version':'1.0','newline':'CRLF'})
        
        post   = ET.SubElement(bl14b2, 'postregist')
        sucess = ET.SubElement(post, 'success', {'do':'move','destination':destdir_sucess})
        fail   = ET.SubElement(post, 'fail', {'do':'move','destination':destdir_fail})
        
        proposalID      = ET.SubElement(bl14b2, 'proposalID')
        proposalID.text = ID
        
        dubline      = ET.SubElement(bl14b2, 'dublincore')
        creater      = ET.SubElement(dubline, 'creater')
        creater.text = CREATER
        rights       = ET.SubElement(dubline, 'rights')
        rights.text  = 'close'

        for sfile in fild_all_files(PWD):
            base = os.path.basename(sfile)
            if base != exception:

                root, ext = os.path.splitext(sfile)
                if ext == '.dat':
                    dtype = dtype_PF
                else:
                    dtype = dtype_OTHER

                sfile    = sfile.replace(PWD,'')
                dfile    = dfile_BASE+proposalID.text+sfile
                dtype    = dtype
        
                data     = ET.SubElement(bl14b2, 'data',{'file':dfile,'type':dtype})
                obj      = ET.SubElement(data,'object')
                typ      = ET.SubElement(obj,'type')
                typ.text = 'file'
        
        tree = ET.ElementTree(bl14b2)
#       tree.write('data.xml')
        tree.write(PWD+PWD_BASE+'.xml')


def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
       #yield root
        for i in files:
            yield os.path.join(root,i)
           #yield os.path.join(i)
           #print root,i


class MyFileDropTarget(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window    #ファイルをドロップする対象

    def OnDropFiles(self, x, y, filenames):  #ファイルをドロップするときの処理
        self.filenames = filenames
        for file in filenames:
            self.window.text.SetValue(file)
           #makes_xmlfile(file)


class MyFrame(wx.Frame):

    def __init__(self):

        # set default
        self.ID     = ID
        self.userID = CREATER
        self.sucess = destdir_sucess
        self.fail   = destdir_fail
        self.base   = dfile_BASE

        # makes Frame & Panel
        wx.Frame.__init__(self, None, title="makes XML",size=(420, 430))
        self.panel = wx.Panel(self)                                                            

        # projectID
        self.inpProjectIdLabel   = wx.StaticText(self.panel, -1, "ProjectID:")
        self.inpProjectIdText    = wx.TextCtrl(self.panel, -1, self.ID, size=(200,-1))
        self.inpProjectIdButton  = wx.Button(self.panel)

        self.inpProjectIdButton.SetLabel("submit")
        self.inpProjectIdButton.Bind(wx.EVT_BUTTON,self.projectIdOnSubmit)

        self.inpProjectIdBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inpProjectIdBox.Add(self.inpProjectIdLabel, 0, wx.ALL, 5)
        self.inpProjectIdBox.Add(self.inpProjectIdText, 0, wx.ALL, 5)
        self.inpProjectIdBox.Add(self.inpProjectIdButton, 0, wx.ALL, 5)

        # userID
        self.inpUserIdLabel  = wx.StaticText(self.panel, -1, "UserID:")
        self.inpUserIdText   = wx.TextCtrl(self.panel, -1, self.userID, size=(200,-1))
        self.inpUserIdButton = wx.Button(self.panel)

        self.inpUserIdButton.SetLabel("submit")
        self.inpUserIdButton.Bind(wx.EVT_BUTTON,self.userIdOnSubmit)

        self.inpUserIdBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inpUserIdBox.Add(self.inpUserIdLabel, 0, wx.ALL, 5)
        self.inpUserIdBox.Add(self.inpUserIdText, 0, wx.ALL, 5)
        self.inpUserIdBox.Add(self.inpUserIdButton, 0, wx.ALL, 5)

        # sucess ,destdir (src)
        self.inpSucessLabel  = wx.StaticText(self.panel, -1, "destdir sources:")
        self.inpSucessText   = wx.TextCtrl(self.panel, -1, self.sucess, size=(200,-1))
        self.inpSucessButton = wx.Button(self.panel)

       #self.inpSucessButton.SetLabel("open") # Open
       #self.inpSucessButton.Bind(wx.EVT_BUTTON,self.OnOpen)
        self.inpSucessButton.SetLabel("submit") # Open
        self.inpSucessButton.Bind(wx.EVT_BUTTON,self.sucessOnSubmit)

        self.inpSucessBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inpSucessBox.Add(self.inpSucessLabel, 0, wx.ALL, 5)
        self.inpSucessBox.Add(self.inpSucessText, 0, wx.ALL, 5)
        self.inpSucessBox.Add(self.inpSucessButton, 0, wx.ALL, 5)

        # destdir (fail)
        self.inpFailLabel  = wx.StaticText(self.panel, -1, "destdir fail:") 
        self.inpFailText   = wx.TextCtrl(self.panel, -1, self.fail, size=(200,-1))
        self.inpFailButton = wx.Button(self.panel)

       #self.inpFailButton.SetLabel("open")
       #self.inpFailButton.Bind(wx.EVT_BUTTON,self.OnOpen)
        self.inpFailButton.SetLabel("submit")
        self.inpFailButton.Bind(wx.EVT_BUTTON,self.failOnSubmit)

        self.inpFailBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inpFailBox.Add(self.inpFailLabel, 0, wx.ALL, 5)
        self.inpFailBox.Add(self.inpFailText, 0, wx.ALL, 5)
        self.inpFailBox.Add(self.inpFailButton, 0, wx.ALL, 5)

        # storatg
        self.inpStorageLabel  = wx.StaticText(self.panel, -1, "Storage BASE Path:")
        self.inpStorageText   = wx.TextCtrl(self.panel, -1, self.base, size=(200,-1))
        self.inpStorageButton = wx.Button(self.panel)

       #self.inpStorageButton.SetLabel("open")
       #self.inpStorageButton.Bind(wx.EVT_BUTTON,self.OnOpen)
        self.inpStorageButton.SetLabel("submit")
        self.inpStorageButton.Bind(wx.EVT_BUTTON,self.storageOnSubmit)

        self.inpStorageBox = wx.BoxSizer(wx.HORIZONTAL)
        self.inpStorageBox.Add(self.inpStorageLabel, 0, wx.ALL, 5)
        self.inpStorageBox.Add(self.inpStorageText, 0, wx.ALL, 5)
        self.inpStorageBox.Add(self.inpStorageButton, 0, wx.ALL, 5)

        # D&D area
        self.ddLabel = wx.StaticText(self.panel, -1, "File name:")
        self.text    = wx.TextCtrl(self.panel, -1, "", size=(300,200))

        self.ddBox = wx.BoxSizer(wx.HORIZONTAL)
        self.ddBox.Add(self.ddLabel, 0, wx.ALL, 5)
        self.ddBox.Add(self.text, 0, wx.ALL, 5)

        # Button
        self.startButton = wx.Button(self.panel, -1, "Start")
        self.startButton.Bind(wx.EVT_BUTTON,self.makeXml)

        # メインのsizerに配置
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.inpProjectIdBox, 0, wx.ALIGN_LEFT)  # ProjectID
        self.sizer.Add(self.inpUserIdBox, 0, wx.ALIGN_LEFT)     # UserID
        self.sizer.Add(self.inpSucessBox, 0, wx.ALIGN_LEFT)        # dest-src
        self.sizer.Add(self.inpFailBox, 0, wx.ALIGN_LEFT)       # dest-fail
        self.sizer.Add(self.inpStorageBox, 0, wx.ALIGN_LEFT)    # Storage-BASE
        self.sizer.Add(self.ddBox, 0, wx.ALIGN_CENTER)
        self.sizer.Add(self.startButton, 0, wx.ALIGN_CENTER)

        # Frame にsizerを追加する
        self.panel.SetSizer(self.sizer)
                                                                                          
        self.dt = MyFileDropTarget(self)  #ドロップする対象をこのフレーム全体にする
        self.SetDropTarget(self.dt)

    def makeXml(self, event):
        for name in self.dt.filenames:
           #self.ID      = ID
           #self.userID  = CREATER
           #self.sucess  = destdir_sucess
           #self.fail    = destdir_fail
           #self.storage = dfile_BASE
            makes_xmlfile(name,self.ID,self.userID,self.sucess,self.fail,self.storage)

    def projectIdOnSubmit(self,event):
        self.ID = self.inpProjectIdText.GetValue()
       #print self.ID

    def userIdOnSubmit(self,event):
        self.userID = self.inpUserIdText.GetValue()
       #print self.ID

    def storageOnSubmit(self, event):
        self.storage = self.inpStorageText.GetValue()
        print(self.storage)

    def failOnSubmit(self, event):
        self.fail = self.inpFailText.GetValue()
       #print self.fail

    def sucessOnSubmit(self, event):
        self.sucess = self.inpSucessText.GetValue()
       #print self.sucess

    def OnOpen(self, e):
        self.dirName = ''
        dialog = wx.FileDialog(self, "Choose a directory", self.dirName, "", "*.*", wx.OPEN)
        if dialog.ShowModal() == wx.ID_OK: #OKボタンが押されるまで表示
            self.fileName = dialog.GetFilename()
            self.dirName = dialog.GetDirectory()
           #file = open(os.path.join(self.dirName, self.fileName), 'r')
           ##ファイルデータ読み込み
           #file.close()
        #ダイアログの破棄
        dialog.Destroy()


################################################################################
if __name__ == '__main__':
#   app = wx.PySimpleApp()
    app = wx.App()

    frm = MyFrame()
    frm.Show()
    app.MainLoop()

