#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
## ASE version
#   atoms = read_vasp(name)
#   SAE.print_fdmnes0(atoms=atoms,MOL=MOL)
#   SAE.print_fdmnes0(outname=outname,atoms=atoms,STD=False,MOL=MOL)
#   SAE.print_fdmnes_inp0(atoms=atoms,MOL=MOL)
### SAE version
#   cell = SAE.Read(filename = name, code = 'VASP')
#   SAE.print_fdmnes1(outname=outname,cell=cell,MOL=MOL)
#   SAE.print_fdmnes1(outname=outname,cell=cell,STD=False,MOL=MOL)
#   SAE.print_fdmnes_inp1(cell=cell,MOL=MOL)
from __future__ import print_function

#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# VASP to FDMNES crystal 情報
#
# using ASE version
#
# (注意)
#  1) ASE のルーチン(cellconst) を使っている
#  2) ASE のmodule を呼び出している
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2016.01.16
#  自分でASEのルーチンを置き換えた（完全分離させた)バージョンに致命的な
#  バグを発見。旧バージョンを復帰させる
#  --> 現在のバージョンを凍結
#
#   08.18 でバグが混入したと思われる。
#    このバージョンのブランチは 11.25 までつづく
#
# 2015.08.18
#  ASE で読み込む構造を止めて、拙作 SAE を用いる様にした
#    注意) scale ファクターは 1 を要求
#
# 2015.05.18 startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import os
import sys
import optparse
from ase.io.vasp import *


#
################################################################################
#
#from ase.io.xyz import *
#from ase import Atoms
#from ase.io import read,write
#from ase.io.vasp import *
#from ase.io.wien2k import *  ## using cellconst
#import numpy as np
################################################################################
def options():
    name = "POSCAR"
    outname = "read_pdb.inp"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ipput", dest="INPUT")
    parser.add_option("-o", "--outname")
    parser.add_option("-m", "--mol", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        name = options.INPUT
    if options.outname:
        outname = options.outname
    if len(args) > 0:
        name = str(args[0])
    if options.mol:
        MOL = True
    else:
        MOL = False
    if not os.path.exists(name):
        if os.path.exists(name + ".vasp"):
            name = name + ".vasp"
        elif os.path.exists("CONTCAR"):
            name = "CONTCAR"
        else:
            sys.exit("STOP: " + name + " file not found")
    return (name, outname, MOL)


################################################################################
### bug-version につきコメントアウト
#   cell = SAE.Read(filename=name,code='VASP')
#   cell.write(code='FDMNES',outname=outname,STD=True,MOL=MOL)
#   cell.write(code='FDMNES',outname=outname,MOL=MOL)
if __name__ == "__main__":
    name, outname, MOL = options()
    print("gug version")
