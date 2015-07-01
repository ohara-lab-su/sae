#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#
################################################################################
#
# 2015.07.01
#  平均化ルーチンで重み(平均する際に割る数)を引数に追加
#
# 2015.07.01
#   absorber 複数のファイル結合モードを追加
#
# 2015.05.21
#   startup (スピン未対応)
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import gzip
#import os
#import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadFdmSd(object):

    def __init__(self,sdname,bavname=None,\
            suffix='_sd0.txt',inpname='read_pdb.inp',absorber=None,weight=None):

        if bavname is None:
            bavname = sdname

        ############################## self.datlines ###########################
        if absorber is None:
            print "---- ReadFdmSd ----"
            print "sdname + suffix = ",sdname+suffix
            print "bavname_bav.txt = ",bavname+'_bav.txt'
            print "inpname         = ",inpname
            print "-------------------"
            self.datlines,self.num = SAE.read_dataline(sdname+suffix)
        else:
            print "--- ReadFdmSd ------"
            print "    average mode ---"
            sdname0 = bavname+'_'+str(absorber[0])+suffix
            row,num = SAE.read_row(sdname0,column=1)
            if weight is None:
                n_site = float(len(absorber))
            else:
                print "    weight = "+str(weight)
                n_site = float(weight)

            # アホな合計->平均->元の要素が結合したリスト形式への変換
            dsum  = np.zeros((num,row))
            dtmp = np.zeros((num,row))
            numdata = np.zeros((num,row))
            for i in range(len(absorber)):
                sdname = bavname+'_'+str(absorber[i])+suffix
                print "sum : ",sdname
                datatmp,num0 = SAE.read_dataline(sdname)
                for i in range(1,num):
                    for r in range(row):
                        dtmp[i,r] = datatmp[i].split()[r]
                dsum = dtmp + dsum
            numdata = dsum/n_site  # 平均値を出す

            # 元々の self.datlines 形式に合わせて配列を作りなおす(互換性維持)
            listdata = list(numdata)
            self.datlines = []
            self.datlines.append('') # dummy '1st-line'
            for i in range(1,num):
                self.datlines.append(''.join(str(listdata[i])).\
                        replace('\n','').replace('[','').replace(']',''))
            self.num = num
        ############################## self.datlines ###########################

        bav = SAE.ReadFdmBav(bavname)
        inp = SAE.ReadFdmInp(inpname)

        self.lmax = int(bav.get_lmax())
        self.ispin = int(inp.get_ispin())
        mmax = 2*self.lmax+1
#       print "mmax=",mmax

        mmax = 0
        for l in range(self.lmax+1):
            mmax += 2*l+1

        total_orbit = mmax
        total_line = 2 + total_orbit*2 + (l+1)*2

        # _sd0.txt の一行目のチェック
        if absorber is None:
            if len(self.datlines[0].split()) != total_line:
                sys.exit("STOP: unknown type "+name+"_sd0.txt")

        # 各l軌道ごとのデーターが収納されている行数の番号を取得(非スピン)
        lnum = []
        line = 2
        for ll in range(self.lmax+1):
            for m in range(-ll,ll+1):
                line += 2
            lnum.append(line)
            line += 2
#       for l in range(lmax+1):
#           print lnum[l]
#       print "s",lnum[0]
#       print "p",lnum[1]
#       print "d",lnum[2]


        # DOS & TDOS を軌道ごとに読み込む
        ## for non-spin Cu
        #  0     Energy
        #  1,    Int_t
        #
        #  2, 3  n(0,0)    Intn(0,0)
        #
        #  4, 5  n_l(0)    Intn_l(0) ---> s
        #
        #  6, 7  n(1,-1)   Intn(1,-1)
        #  8, 9  n(1,0)    Intn(1,0)
        # 10,11  n(1,1)    Intn(1,1)
        #
        # 12,13  n_l(1)    Intn_l(1) ---> p
        #
        # 14,15  n(2,-2)   Intn(2,-2)
        # 16,17  n(2,-1)   Intn(2,-1)
        # 18,19  n(2,0)    Intn(2,0)
        # 20,21  n(2,1)    Intn(2,1)
        # 22,23  n(2,2)    Intn(2,2)
        #
        # 24,25  n_l(2)    Intn_l(2) --->  d

        self.dos = np.zeros((self.num-1,self.lmax+1,self.ispin))
        self.tdos = np.zeros((self.num-1,self.lmax+1,self.ispin))
        self.eng = []
        self.intt = []
        spin = 0
        for i in range(1,self.num):
            self.eng.append(float(self.datlines[i].split()[0]))
            self.intt.append(float(self.datlines[i].split()[1]))
            self.intt.append(float(self.datlines[i].split()[1]))
            for l in range(self.lmax+1):
                self.dos[i-1,l,spin] = float(self.datlines[i].split()[lnum[l]])
                self.tdos[i-1,l,spin] = float(self.datlines[i].split()[lnum[l]+1])

#       self.eng = np.zeros(self.num-1)
#       self.xas = np.zeros(self.num-1)

#       for i in range(1,self.num):
#           self.eng[i-1] = float(self.datlines[i].split()[0])
#           self.xas[i-1] = float(self.datlines[i].split()[1])


    # LDOS(NEDOS,L,SPIN)
    def get_ldos(self,l=0,spin=0):

        if isinstance(l,str):
            if l == 's' and self.lmax >= 0: l = 0
            if l == 'p' and self.lmax >= 1: l = 1
            if l == 'd' and self.lmax >= 2: l = 2
            if l == 'f' and self.lmax >= 3: l = 3

        self.ldos = self.dos[:,l,spin]
        return self.ldos

    def get_eng(self):
        return self.eng


################################################################################
def options():

    name = 'Cu'
    suffix = '_sd0.txt'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name,suffix

################################################################################
if __name__ == '__main__':

    name,suffix = options()
    conv = ReadFdmSd(name,suffix)

#   eng = conv.get_eng()
#   xas = conv.get_xas()


#   print "NAME",name


