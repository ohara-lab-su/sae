#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import os
import wx
import xml.etree.ElementTree as ET

dtype_OTHER = "binary"
dtype_PF = "/home/dspace/PF9809"
destdir_sucess = "/home/dspace/cr/compdir"
destdir_fail = "/home/dspace/cr/retrydir"
dfile_BASE = "/storage/data/"
ID = "2014T1343"
CREATER = "0001343"
exception = ".DS_Store"


def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for i in files:
            yield os.path.join(root, i)


def makes_xmlfile(dirname):
    if os.path.isdir(dirname):
        PWD = dirname
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


class MyFileDropTarget(wx.FileDropTarget):

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, filenames):
        for file in filenames:
            self.window.text.SetValue(file)
            makes_xmlfile(file)


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
        dt = MyFileDropTarget(self)
        self.SetDropTarget(dt)


if __name__ == "__main__":
    app = wx.PySimpleApp()
    frm = MyFrame()
    frm.Show()
    app.MainLoop()
