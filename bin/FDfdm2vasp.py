#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 統合テスト兼、FDMNES --> VASP 変換
#
################################################################################
# History
#
# 2015.08.20
#  startup
#  既知の問題: 分子系の変換時のunit-cellのスケールがおかしい
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015 Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.5"
################################################################################

#import sys
import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE


################################################################################
if __name__ == '__main__':

    import optparse
    name = 'read_pdb.inp'
    parser = optparse.OptionParser()
    parser.add_option( '-i','--input', dest='INPUT')
    options, args = parser.parse_args()

    if options.INPUT: name = options.INPUT
    if len(args)>0: name = args[0]

    print "INPUT :",name
    print "OUTPUT:",name+".vasp"

    cell = SAEnv.Read(filename=name,code='FDMNES')
    cell.write(code='VASP',outname=name,STD=True)
    cell.write(code='VASP',outname=name)

#   SAEnv.write(cell, outname='test.vasp',code='VASP')
#   SAEnv.write(cell, outname='test.vasp',code='VASP',STD=False)

