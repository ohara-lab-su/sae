#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# read_list.py の class 化 (および openmx の vps データに特化)
#  *) 引数で配列を返す仕様
#
# 4列のリストをひたすら split して配列に読み込むだけのアホ仕様
#
################################################################################
#
# 2015.02.10 1st
#
################################################################################
__author__     = "Kengo NAKADA"                                                           
__maintainer__ = "Kengo NAKADA"                                                           
__credits__    = ["Kengo NAKADA"]                                                         
__email__      = "kengo.nakada@gmail.com"                                                 
__copyright__  = "Copyright 2014, Kengo NAKADA"                                           
__license__    = "MIT"                                                                    
#                                                                                         
__status__     = "alpha"                                                                  
__version__    = "0.0.1"                                                                  
################################################################################

import sys
import os
import re
#import numpy as np
#from copy import deepcopy


################################################################################
class ReadVpsList(object):

    def __init__(self,name):

        if not os.path.exists(name):
            sys.exit("STOP: "+name+" not found")
   
        try:
            tmp = open(name)
            datalist = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+name+" does'nt open")
        finally:
            tmp.close()

        self.datalines = datalist.split('\n')
        self.nlist0=int(len(self.datalines)) -1


    ################################################
    # リストを読み込む
    # read_list.py とほぼ同等機能
    def get_list(self):

        comment_reg = re.compile('^#.*',re.IGNORECASE)

        self.list_data = []
        j = 0
        for i in range(self.nlist0):
            if not bool(comment_reg.match(self.datalines[i])):
                tmp = self.datalines[i].split()
                if not int(len(tmp)) >= 4:
                    sys.exit(self.name+" Format Error: datalines < 4 ") 
    
                self.list_data.append([tmp[0],tmp[1],tmp[2],tmp[3]])
                j += 1
        self.nlist = j

        return [self.nlist,self.list_data]


    ################################################
    # 元素記号に対応する情報を抜き出す
    # 注意) 同名の元素記号があるときは先頭行のみ吸い出し
    def get_vps_name(self,atom):
        nlist,list_data = self.get_list()

        for i in range(nlist):
            if list_data[i][1] == atom:
                num = list_data[i][0]
                symbol = list_data[i][1]
                cutoff = list_data[i][2]
                vps_orbit = list_data[i][3]
                break

        return [num,symbol,cutoff,vps_orbit]

################################################################################
if __name__ == '__main__':

    VPSLIST = 'openmx_defaults_vpsdata'
    DFT_DATA = 'DFT_DATA13'

    data = '../'+DFT_DATA
    pot = 'PBE'
    ver = '13'

    # VPS 及び PAO のパス設定
    vpspath = data+'/VPS/'
    paopath = data+'/PAO/'

    # VPSLIST のファイル場所確認
    HOMEPATH=os.environ.get('HOME',"")
    if os.path.exists(VPSLIST):
        vpslistpath = VPSLIST
    elif os.path.exists(HOMEPATH+'/'+DFT_DATA+'/'+VPSLIST):
        vpslistpath = HOMEPATH+'/openmx1/'+DFT_DATA+'/'+VPSLIST
    elif os.path.exists(HOMEPATH+'/openmx1/'+VPSLIST):
        vpslistpath = HOMEPATH+'/openmx1/'+VPSLIST
    else:
        sys.exit("STOP: "+VPSLIST+" file not found")

    # vps and pao 情報リスト読み込み(OpenMX非公式ファイル)
    vpsdata = ReadVpsList(vpslistpath)

    num,symbol,cutoff,vps_orbit = vpsdata.get_vps_name('C')
    opt = re.sub(r'[0-9\.]+','',cutoff) # cutoff 名から英数文字のみ取り出す

    vps_name = symbol+cutoff+'-'+vps_orbit
    vps_file = vpspath+symbol+'_'+pot+ver+opt+'.vps'
    pao_file = paopath+symbol+cutoff+'.pao'

    if not os.path.exists(pao_file):
        sys.exit("STOP: "+pao_file+" not found")
    if not os.path.exists(vps_file):
        sys.exit("STOP: "+vps_file+" not found")

    print "pao file:",pao_file
    print ""
    print symbol
    print symbol+cutoff+'-'+vps_orbit
    print symbol+'_'+pot+ver+opt


#   nlist,list_data = vpsdata.get_list()
    
#   print nlist
#   for i in range(nlist):
#       print list_data[i]

