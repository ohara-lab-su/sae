#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# PWScf (Quantum ESPRESSO 5..x )
# dos 関連出力 ファイル( dos.x projwfc.x 出力ファイル 読み込み)
#
#
################################################################################
#
# 2015.05.08 startup
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
__version__    = "0.1.1"
################################################################################

import sys
#import gzip
import os
import glob
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadPwPdos(object):

    def __init__(self,prefix):

        # cname+'pdos.pdos_tot'
        self.datlines,self.num = SAE.read_dataline(prefix+'.pdos.pdos_tot')
        self.nedos = self.num -1

        if len(self.datlines[1].split()) > 3:
            self.ispin = 2
        else:
            self.ispin = 1

        # 実際に計算している pdos ファイルの取得
        pdos_list = glob.glob(prefix+'.pdos.pdos_atm#*')
        if len(pdos_list) < 1:
            sys.exit("STOP: "+prefix+".pdos.pdos_atm#* file not found")

        # 計算している pdos ファイルの原子の種類番号のみを取得
        atom_ls = []
        for f in pdos_list:
            tmp = re.sub(prefix+'.pdos.pdos_atm#','',f)
            atom = int(re.sub('\(.*','', tmp))
            atom_ls.append(atom)

        # 重複している pdos ファイルの原子種番号を削除(順番は変更しない)
        atom_list = []
        for x in atom_ls:
            if x not in atom_list:
                atom_list.append(x)

        # ユニークは原子種番号の数から全原子数を確保
        self.natom = len(atom_list)

        # 実際に計算している各原子毎に計算しているlの最大値を取得する
        lmax_list = []
        for atom in atom_list:
            tmp = glob.glob(prefix+'.pdos.pdos_atm#'+str(atom)+'(*')
            for g in tmp:
                tmp = re.sub(prefix+'.pdos.pdos_atm#','',g)
                lmax = int(re.sub('\(.*' ,'',re.sub('\d*\(.*#','',tmp) ))
            lmax_list.append(lmax)

       #print len(atom_list), atom_list
       #print len(lmax_list), lmax_list

        ################
        # LDOS 収納に使う配列の確保(原子種毎),配列の l_max は固定にする
        l_max = 4 # s,p,d,f
        self.ldos = np.zeros((self.nedos,l_max,self.natom,self.ispin))

        ################
        # PDOS 収納に使う配列の確保
        lm_max = 1+3+5+7 # s+p+d+f
        self.pdos = np.zeros((self.nedos,lm_max,self.natom,self.ispin))
        self.eng = np.zeros((self.nedos,self.natom))

        ########################################################################
        # 原子種のループ
        i = 0
        for atom in atom_list:

            for orbit in range(lmax_list[i]):

                pfiles = glob.glob(\
                        prefix+'.pdos.pdos_atm#'+str(atom)+'(*_wfc#'+str(orbit+1)+'(*'\
                        )
                if not len(pfiles) == 1:
                    sys.exit("STOP: "+pfiles)
                pname = pfiles[0]

                # 原子種＋軌道におけるデータ読み込み
                data,nline = SAE.read_dataline1(pname)
                if nline != self.nedos:
                    sys.exit("STOP: Contradiction Number of Data Line :"+pname)

                print pname
                if self.ispin == 2:
                    print atom, orbit+1, ( len(data[0].split()) - self.ispin ) / 2
                    for spin in range(self.ispin):
                        for j in range(nline):
                            self.eng[j] = float(data[j].split()[0])

                           #self.ldos[j,0,atom-1,spin] = \
                           #        float(data[j].split()[0+spin]

            i += 1

    def get_nedos(self):
        return self.nedos

    def get_ispin(self):
        return self.ispin

    def get_natom(self):
        return self.natom

################################################################################
def options():

    prefix = 'Fe'
    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input', dest='INPUT',)
    options,args = parser.parse_args()

    if not os.path.exists(prefix+'.pdos.pdos_tot'):
        pdosname = glob.glob('*.pdos.pdos_tot')
        if len(pdosname) == 1:
            prefix = re.sub('.pdos.pdos_tot','',pdosname[0])

    if options.INPUT:
        prefix=options.INPUT

    if len(args) > 0:
        prefix=args[0]

    return prefix

################################################################################
if __name__ == '__main__':

    prefix = options()
    print "PREFIX:",prefix
    dos = ReadPwPdos(prefix)

