#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.structure.document import Read

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7 *.dat 形式ファイル 読み込み --> VASP 形式出力
#
################################################################################
#
# 2018.08.23
#  Python2/3 両対応
#
# 2015.08.25
#  現時点では moulecule モードに対応してない
#  (旧バージョンでは対応済み)
#
# 2015.08.25
#  統合化バージョン
#  旧バージョン(ローカルバージョン) の開発履歴は MXdat2vasp_loca.py の中を見ろ
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014-2015, Kengo NAKADA"
__license__ = "MIT"
import os


#
################################################################################
#import sys
#import re
#import gzip
#import numpy as np
#import SpaceGroupEnvironment as SGE
################################################################################
#   poscarname = 'openmx.vasp'
# デフォルト名より最適なデフォルトファイル名の推定ルーチン
# もし出力ファイル名のsuffixに .dat がついていたら安全のためにそれを消す
#       poscarname=re.sub('\.dat','',poscarname)
#   if poscarname == mxname:
#       sys.exit("STOP: input-filename = output-filename")
def options():
    from sae.common.paths import FileDiscovery
    import optparse

    name = "openmx"
    suffix = ".dat"
    mxname = name + suffix
    poscarname = "openmx"
    xyzname = "openmx.xyz"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    parser.add_option("-o", "--output", dest="OUTPUT")
    parser.add_option(
        "-d", "--direct", action="store_true", default=False, dest="DIRECT"
    )
    parser.add_option("-s", "--std", action="store_true", default=False, dest="STDOUT")
    options, args = parser.parse_args()
    if not os.path.exists(mxname):
        name0 = FileDiscovery().find_datfile("dat")
        #           poscarname = mxname+'.vasp'
        if not name0 is None:
            name = name0
            mxname = name + suffix
            poscarname = mxname
            xyzname = mxname + ".xyz"
    #       poscarname = mxname+'.vasp'
    if options.INPUT:
        mxname = options.INPUT
        poscarname = mxname
        xyzname = mxname + ".xyz"
    if options.OUTPUT:
        poscarname = options.OUTPUT
    return [mxname, poscarname, xyzname, options.STDOUT, options.DIRECT]


################################################################################
if __name__ == "__main__":
    mxname, poscarname, xyzname, STD, DIRECT = options()
    print("INPUT", mxname)
    print("OUTPUT", poscarname + ".vasp")
    cell = Read(filename=mxname, code="OpenMX")
    cell.write(outname=poscarname, code="VASP", STD=STD)
