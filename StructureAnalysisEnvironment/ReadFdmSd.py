#!/usr/bin/env python
# -*- coding: utf-8 -*
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_sd*.txt ファイル( pw.x 入力ファイル 読み込み)
#
################################################################################
#
# 2015.07.02
#  spin,ylm,intt,等の全出力の対応を含めた一般化
#
# 2015.07.01
#  spin対応版 startup
#
# 2015.07.01
#  平均化ルーチンで重み(平均する際に割る数)を引数に追加
#  --> 平均化ルーチンはコンストラクタで処理
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

    def __init__(self,sdname,\
            suffix='_sd0.txt',inpname='read_pdb.inp',\
            bavname=None,absorber=None,weight=None):

        if bavname is None:
            bavname = sdname

        ############################## self.datlines ###########################
        # sum
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
                for i in range(1,num):     # 一行目は除く
                    for r in range(1,row): # Energy は除く
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

        # オービタルの情報(bav) とスピンの情報(inp) を入手
        bav = SAE.ReadFdmBav(bavname)
        inp = SAE.ReadFdmInp(inpname)

        self.lmax = int(bav.get_lmax())
        self.ispin = int(inp.get_ispin())
        self.mmax = int(2*self.lmax+1)

        # トータルのオービタル数を計算
        tmmax = 0
        for l in range(self.lmax+1):
            tmmax += (2*l+1)*self.ispin
        total_orbit = tmmax

        # _sd0.txt で出力される列数
        total_row = 1 + self.ispin + total_orbit*2 + (l+1)*2*self.ispin

        # _sd0.txt の一行目のチェック
        if absorber is None:
            if len(self.datlines[0].split()) != total_row:
                sys.exit("STOP: unknown type "+name+"_sd0.txt")

        # すべての row 成分の情報を配列に叩きこむ
        self.ylm   = np.zeros((self.num-1,self.lmax+1,self.mmax,self.ispin))
        self.intylm= np.zeros((self.num-1,self.lmax+1,self.mmax,self.ispin))
        self.dos   = np.zeros((self.num-1,self.lmax+1,self.ispin))
        self.tdos  = np.zeros((self.num-1,self.lmax+1,self.ispin))
        self.intt  = np.zeros((self.num-1,self.ispin))
        self.eng   = np.zeros(self.num-1)

        for i in range(1,self.num):
            row = 0
            self.eng[i-1] = float(self.datlines[i].split()[row])
            row += 1

            for s in range(self.ispin):
                self.intt[i-1,s] = float(self.datlines[i].split()[row])
                row += 1

            for ll in range(self.lmax+1):
                m0=0
                for m in range(-ll,ll+1): # m,s成分分解
                    for s in range(self.ispin):
                        # 成分 and 積分
                        self.ylm[i-1,ll,m0,s] = float(self.datlines[i].split()[row])
                        row += 1
                        self.intylm[i-1,ll,m0,s] = float(self.datlines[i].split()[row])
                        row += 1
                    m0 += 1
                for s in range(self.ispin): # l軌道のsum
                    self.dos[i-1,ll,s] = float(self.datlines[i].split()[row])
                    row +=1
                    self.tdos[i-1,ll,s] = float(self.datlines[i].split()[row])
                    row +=1


    # LDOS(NEDOS,L,SPIN)
    def get_ldos(self,l=0,spin=0):

        if isinstance(l,str):
            if l == 's' and self.lmax >= 0: l = 0
            if l == 'p' and self.lmax >= 1: l = 1
            if l == 'd' and self.lmax >= 2: l = 2
            if l == 'f' and self.lmax >= 3: l = 3

        if isinstance(spin,str):
            if spin == 'up': spin = 0
            if spin == 'dn': spin = 1
            if spin == 'down': spin = 1

        self.ldos = self.dos[:,l,spin]
        return self.ldos

    def get_eng(self):
        return self.eng


################################################################################
def options():

#   name = 'Cu'
    name = 'Fe'
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


