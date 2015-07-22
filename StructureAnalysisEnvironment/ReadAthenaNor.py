#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Read Athena Normalize Data ( *.txt.nor )
#
#
################################################################################
#
# 2015.06.30
#   == Noneo --> is None
#
# 2015.05.21
#  ファイル名の自動取得&基本プロットのサンプル追加
#
# 2015.03.30
#  startup
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
__version__    = "0.0.1"
################################################################################

#import sys
import os
import re
#import gzip
import numpy as np

#import optparse

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadAthenaNor(object):

    def __init__(self,name='case.txt.nor'):

        self.datlines,self.num = SAE.read_dataline(name)
        comment_reg = re.compile('^#.*')
        E0_reg = re.compile('^#.*E0.*')

        self.eng = []
        self.nor = []
        self.ndata = 0
        for i in range(self.num):
            line = self.datlines[i]

            if bool(E0_reg.match(line)):
                self.e0 = float(re.sub('E0=','',line.split()[2]))

            if not bool(comment_reg.match(line)):
                self.eng.append(float(line.split()[0]))
                self.nor.append(float(line.split()[1]))
                self.ndata += 1

        self.nor = np.array(self.nor)
        self.eng = np.array(self.eng)

    def get_nor(self):
        return self.nor

    def get_eng(self):
        return self.eng

    def get_ndata(self):
        return self.ndata

    def get_e0(self):
        return self.e0

################################################################################
def plot_athena_nor(eng,nor):

    import matplotlib.pyplot as plt


    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.010
    xsize = 0.75
    ysize = 0.83/2.

    plt.axes([orgx,orgy,xsize,ysize])

    plt.plot(eng,nor,linewidth=2,label='XAS')

    plt.xlabel("E")
    plt.ylabel(" chi mu (E)")
#   plt.axvline(x=0,color='black',linewidth=1)

    leg = plt.legend(fontsize=12,loc='lower right')
    leg.get_frame().set_alpha(0.5)

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

################################################################################
def options():
    import optparse

    name = 'Cu_foil_10ms.txt.nor'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    options, args = parser.parse_args()

    if not os.path.exists(name):
        name0 = SAE.find_datfile1('.txt.nor')
        if name0 is None:
            name0 = name
    name = name0

    if options.INPUT: name = options.INPUT
    if len(args) > 0: name = args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()

    spec = ReadAthenaNor(name)
    print spec.get_e0()
#   plot_athena_nor(spec.eng,spec.nor)

#   for i in range(ndata):
#       print eng[i],nor[i]

