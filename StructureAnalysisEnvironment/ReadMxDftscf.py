#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
# *.DFTSCF ファイル 読み込み
#
#  ReadMxDatMethod -- ReadMxOut -- ReadMxDftscf
#                  -- ReadMxDat
#
################################################################################
#
# 2015.03.12
#   startup
#
#   オーバーライトするもの
#     get_n_ion_loop()
#     get_uele()
#
#   データーが途中で止まっていても MD ループ等の情報を正しく読めるように修正
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

#import sys
#import gzip
import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadMxDftscf(SAE.ReadMxOut):

    ###################################
    def __init__(self,cname):

        self.datlines, self.num = SAE.read_dataline(cname)

    ###################################
    # イオンループの数
    # SCF MD=* 項目の * の最大値を引き抜く
    # 同一 MD=* 番号が連続して現れても関係なく * の最大を取る
    def get_n_ion_loop(self):
        md_text = '.*Total energy.*at MD ='
        md_reg = re.compile(md_text)
        self.n_ion_loop = 0
        for i in range(self.num):
            if bool(md_reg.match(self.datlines[i])):
                tmp = int(re.sub(md_text,'',self.datlines[i]))
                if self.n_ion_loop < tmp:
                    self.n_ion_loop = tmp
               #print self.n_ion_loop, self.datlines[i]
       #print "MAX",self.n_ion_loop
        return self.n_ion_loop


    ###################################                                         
    # イオンループ毎のさらにSCFループごとの Uele(bandエネルギー) の抽出         
    # 同一 MD=* 番号が現れた時は最後の SCF ループのみを取り出す                 
    def get_uele(self):
                                                                                
        md_start_txt = '.*SCF.*at MD='
        md_start_reg = re.compile(md_start_txt)

        scf_txt = '.*SCF=.*Uele='
        scf_reg = re.compile(scf_txt)

        n_ion_loop = self.get_n_ion_loop()
        max_n_scf = self.get_max_n_scf()

        self.uele = np.zeros((n_ion_loop,max_n_scf))
        self.uele_index = np.zeros((n_ion_loop),dtype=int)

        i=0
        md=0
        while 1:
            # MD= 行を見つけたらスタート
            if bool(md_start_reg.match(self.datlines[i])):
               #md = int(re.sub(md_start_txt,'',self.datlines[i])) - 1
                # SCF行が始まるまでジャンプ
                while not bool(scf_reg.match(self.datlines[i])): i +=1
                scf = 0
                # SCF 行がある間だけ読み込み
                while bool(scf_reg.match(self.datlines[i])):
                    uele0 = float(re.sub(scf_reg,'',self.datlines[i]))
                   #print " %d %d %15.12f" %( md,scf,uele0 )
                    self.uele[md,scf] = uele0
                    self.uele_index[md] = scf
                    scf +=1
                    i += 1
               #print ''
                md += 1
            i += 1
            if md == n_ion_loop: break
        return self.uele,self.uele_index

################################################################################
if __name__ == '__main__':
                                                                                
    name = 'openmx'
    suffix = '.out'
    mxname = name+suffix
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
    )
    options,  args = parser.parse_args()

    # デフォルト名より最適なデフォルトファイル名の推定ルーチン                     
    if not os.path.exists(mxname):
        try:
            name0 = SAE.find_datfile('dat')  # *.dat はかならずあるのでそれをトリガーに
            if not name0 == None:
                name = name0
                mxname = name+suffix
        except:                                                                 
            pass 

    # オプションでファイル名を入力した時
    if options.INPUT:
        mxname = options.INPUT
        name = re.sub('\.out$','',mxname)
        mxname = name+suffix

    if len(args) > 0:
        name=args[0]
        name = re.sub('\.out$','',name)

    mxname = name+suffix

    # 計算途中での DFTSCF ファイル読み込み
    if not os.path.exists(mxname):
        suffix = '.DFTSCF'
        mxname = name+suffix

    dftscf = ReadMxDftscf(mxname) 

    n_ion_loop = dftscf.get_n_ion_loop()
    max_n_scf = dftscf.get_max_n_scf()

    utot = dftscf.get_utot()
    uele,uele_index = dftscf.get_uele()

    print "N_ION_LOOP",n_ion_loop
    print "MAX_N_SCF", max_n_scf

    for md in range(n_ion_loop):
        print "***************** md = ",md+1,'**********************'
        for scf in range(uele_index[md]):
            print "    scf=%d, Uele = %15.12f" %(scf+1,uele[md,scf])
        print " Utot = %15.12f" %(utot[md])

