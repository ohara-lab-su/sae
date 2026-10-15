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
import lxml.etree as ET

dtype_OTHER = "binary"
dtype_PF = "/home/dspace/PF9809"
destdir_sucess = "/home/dspace/cr/compdir"
destdir_fail = "/home/dspace/cr/retrydir"
dfile_BASE = "/storage/data/"
PLUS = "/test20150325/Ni-foil"
ID = "2014S0000"
CREATER = "0011765"
RIGHTS_TAG = "standard"


def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for i in files:
            yield os.path.join(root, i)


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


if __name__ == "__main__":
    PWD = os.getcwd()
    makes_xmlfile(PWD)
