#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# convert from RMC_POT cfg file to VASP POSCAR file
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.07.16
#    関数版を駆逐(class版を使う)
#
# 2014.10.31
#    関数化 & ライブラリ分離
#
# 2014.10.08
#    Rvasp2cfg.py に仕様を合わせる
#    --> オプション関係を追加
#
# 2014.10.01
#    1st version
#
################################################################################
from __future__ import print_function

################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.3"

################################################################################

import sys
import os
import optparse

# import numpy as np

# try:
#    sys.path.append('../../')
#    import StructureAnalysisEnvironment as SAE
# except ImportError:
#    import StructureAnalysisEnvironment as SAE

import StructureAnalysisEnvironment as SAE

# import SpaceGroupEnvironment as SGE


################################################################################
def options():
    cname = "igzo"  # INPUT BASE filename

    parser = optparse.OptionParser()
    parser.add_option(
        "-i",
        "--input",
        dest="INPUT",
    )
    parser.add_option("--atoms_index")
    options, args = parser.parse_args()
    if options.INPUT:
        cname = options.INPUT

    if len(args) > 0:
        cname = args[0]

    if cname:
        print("INPUT file name : %s" % cname + ".cfg")
        print("OUTPUT file name: %s" % cname + ".vasp")
        print("atoms_index = %s" % options.atoms_index)

    # if not os.path.exists(cname + ".cfg"):
    #     sys.exit(cname + ".cfg file not found")

    return cname, options.atoms_index


################################################################################
if __name__ == "__main__":
    """
    usage:
    V と O 原子の時
    LVOF.cfg ファイルに対するアプローチとしては
       ./Rcfg2vasp.py --atoms_index=V,O LVOF.cfg
    """
    cname, atoms_index0 = options()

    #
    # Usage:
    #  Rcfg2vasp.py <name> --atoms_index=A,B,C,Da
    #
    # atoms_index = ['In', 'Ga', 'Zn', 'O']
    # atoms_index0 = 'V,O'

    atoms_index = []
    if atoms_index0 == None:
        # 原子の種類指定がない時
        # cfg からの変換だとatoms_index を使わないので関係ない
        pass
    else:
        for i in atoms_index0.split(","):
            print(i)
            atoms_index.append(i)

    name_, ext_ = os.path.splitext(cname)
    print("name = %s" % name_)
    print("ext = %s" % ext_)
    if ext_ == "":
        filename = cname + ".cfg"
    else:
        filename = cname
    if not os.path.exists(filename):
        sys.exit(filename + " file not found")

    outname = name_

    print(f"atoms_index = {atoms_index}")

    cell = SAE.io.Read(filename=filename, code="RMC", atoms_index=atoms_index)
    cell.write(outname=outname, code="VASP")
