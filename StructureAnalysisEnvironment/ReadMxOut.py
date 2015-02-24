#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX3.7
# *.out ファイル 読み込み
#
################################################################################
#
# 2015.02.24
#  1st time
#    とりあえず Utot と Uele の ION ステップごとと SCF 毎の結果を
#    整理して抽出するだけのクラス/メッソドをとりあえず準備
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
import gzip
import os
import re
import optparse
import numpy as np

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadMxOut(object):

    def __init__(self,cname):

        if os.path.exists(cname):
            GZIP=False
        elif os.path.exists(cname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+cname+" or "+cname+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(cname+".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+cname+" or "+cname+".gz does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1

    def get_n_ion_loop(self):
        md_text = '.*SCF.*MD='
        md_reg = re.compile(md_text)
        for i in range(self.num):
            if bool(md_reg.match(self.datlines[i])):
                self.n_ion_loop = int(re.sub(md_text,'',self.datlines[i]))
        return self.n_ion_loop

    # イオンループ毎の Total Energy
    def get_utot(self):
        n_ion_loop = self.get_n_ion_loop()
        self.utot = np.zeros((n_ion_loop))
        tot_reg = re.compile('.*Utot\..*')
        j=0
        for i in range(self.num):
            if bool(tot_reg.match(self.datlines[i])):
                    self.utot[j] =self.datlines[i].split()[1]
                    j += 1
        return self.utot

    # SCFループの最大数
    def get_max_n_scf(self):
        scf_txt = '.*SCF='
        scf_reg = re.compile(scf_txt)
        self.max_n_scf = 0
        for i in range(self.num):
            if bool(scf_reg.match(self.datlines[i])):
                tmp = int(re.sub(scf_txt,'',self.datlines[i]).split()[0])
                if self.max_n_scf < tmp:
                    self.max_n_scf = tmp
        return self.max_n_scf            

    # イオンループ毎のさらにSCFループごとの Uele(bandエネルギー) の抽出
    def get_uele(self):
        md_txt = '.*SCF.*at MD='
        md_end = '.*Total energy.*at MD ='
        scf_txt = '.*SCF=.*Uele='
        scf_reg = re.compile(scf_txt)
        md_reg = re.compile(md_txt)
        md_end_reg = re.compile(md_end)

        n_ion_loop = self.get_n_ion_loop()
        max_n_scf = self.get_max_n_scf()
        self.uele = np.zeros((n_ion_loop,max_n_scf))
        self.uele_index = np.zeros((n_ion_loop),dtype=int)
        i=0
        md=0
        while 1:
            if bool(md_reg.match(self.datlines[i])):
                scf = 0
                while not bool(md_end_reg.match(self.datlines[i])):
                    if bool(scf_reg.match(self.datlines[i])):
                        uele0 = float(re.sub(scf_reg,'',self.datlines[i]))
                       #print md,scf,uele0
                        self.uele[md,scf] = uele0
                        self.uele_index[md] = scf
                        scf +=1
                    i += 1
                md += 1
               #print ''
            i += 1
            if self.num == i: break
        return self.uele,self.uele_index

################################################################################
if __name__ == '__main__':
                                                                                
    name = 'openmx.out'
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        name=options.INPUT
                                                                                
    if len(args) > 0:
        name=args[0]
                                                                                
    out = ReadMxOut(name)
    n_ion_loop = out.get_n_ion_loop()
    max_n_scf = out.get_max_n_scf()
    utot = out.get_utot()
    uele,uele_index = out.get_uele()

    for md in range(n_ion_loop):
        print "***************** md = ",md+1,'**********************'
        for scf in range(uele_index[md]):
            print "    scf=%d, Uele = %14.11f" %(scf+1,uele[md,scf])
        print " Utot = %14.11f" %(utot[md])

#   for i in range(n_ion_loop):


