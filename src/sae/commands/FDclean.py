#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.inp import ReadFdmInp

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDclean
# *.in ファイルを読み込んで Filout タグから名前を取得し
# Filout* ファイルを消す
#
################################################################################
#
# 2020.08.11: filout 処理でのセーフティーを導入
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.06.19 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import glob


#
################################################################################
# import gzip
# import re
# import numpy as np
################################################################################
#   name = 'read_pdb.inp'
#   name = 'POSCAR.inp'
###### default inpname
def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.filout
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    if len(args) > 0:
        inpname = args[0]
    return inpname


#   filelist = glob.glob(filout+'*.txt')
#   print ""
if __name__ == "__main__":
    name = options()
    out = ReadFdmInp(name)
    filout = out.get_filout()
    print("fileout :", filout)
    if filout == "":
        print("fileout is None")
        sys.exit(-1)
    filelist = [
        "fdmnes_error.txt",
        filout + ".txt",
        filout + "_bav.txt",
        filout + "_conv.txt",
    ]
    filelist.extend(glob.glob(filout + "_sd*.txt"))
    for i in filelist:
        if os.path.exists(i):
            print("DELETE : " + i)
            os.remove(i)
    if os.path.exists("fdm.out"):
        print("DELETE : fdm.out")
        os.remove("fdm.out")
    if os.path.exists("PBS_log"):
        print("DELETE : PBS_log")
        os.remove("PBS_log")
