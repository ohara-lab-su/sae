#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# DAT_DATA13/PAO ディレクトリの PAO ファイル検索支援
#
# -a オプションで元素名を指定するとその元素名を持っている PAO ファイルを探す
#
# DATA_PATH はある程度自動検索
#
################################################################################
#
# 2015.03.11
#  DATA_PATH の検索関係を少し整備しなおし
#
# 2015.02.09 1st
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.2"
################################################################################

import sys
import os
import re
import dircache
import optparse
#import numpy as np
#import glob

#import re
#from copy import deepcopy

#import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    # default value
    defaultatom='C'
    defaultpot='PBE'
    defaultver='13'

    defaultcut='5.0'

    # オプション処理
    parser = optparse.OptionParser()
    parser.add_option( '-a','--atom',
                        dest='ATOM',
                        default=defaultatom,
                        )
    parser.add_option( '-p','--potential',
                        dest='POT',
                        default=defaultpot
                        )
    parser.add_option( '-v','--version',
                        dest='VER',
                        default=defaultver,
                        )

    parser.add_option( '-c','--cut',
                        dest='CUT',
                        default=defaultcut,
                        )
    options, args = parser.parse_args()

    # default data path
    DFT_DATA_BASE='DFT_DATA'
    DFT_DATA=DFT_DATA_BASE+options.VER
    DFT_DATAPATH= '../'+DFT_DATA

    HOMEPATH=os.environ.get('HOME',"")
    DATAPATH=os.environ.get('OPENMXDATAPATH',"")  # OpenMX DATA 環境変数

    # DFT_DATA path が存在しない時は 環境変数 DATAPATH を選択
    if not os.path.exists(DFT_DATAPATH):             # カレントより一つ上検索
        if os.path.exists('./'+DFT_DATA):            # カレントを検索
            DFT_DATAPATH='./'+DFT_DATA
        elif DATAPATH:                               # 環境変数検索
            DFT_DATAPATH=DATAPATH
        elif os.path.exists(HOMEPATH+'/'+DFT_DATA):  # ホーム直下検索
            DFT_DATAPATH=HOMEPATH+'/'+DFT_DATA
        elif os.path.exists('../'+DFT_DATAPATH):     # カレントより２つ上検索
            DFT_DATAPATH='../'+DFT_DATAPATH
        else:
            sys.exit("STOP: "+DFT_DATA+" directory not found")

#   filename=options.ATOM+'_'+options.POT+options.VER
    filename=options.ATOM+options.CUT

    if len(args) > 0:
        filename=args[0]

    return [DFT_DATAPATH,\
            options.ATOM,options.POT,options.VER,options.CUT,filename]

#   data = '../DFT_DATA13'
#   atom = 'C'
#   pot  = 'PBE'
#   ver  = '13'
#   name = 'C_PBE13'

################################################################################
if __name__ == '__main__':

    opts = options()
    data,atom,pot,ver,cut,name = opts

    fullname = data+'/PAO/'+name+'.pao'

    SUFFIX=''
    if not os.path.exists(fullname):
        SUFFIX='S'
        fullname = data+'/PAO/'+name+SUFFIX+'.pao'
        if not os.path.exists(fullname):
            SUFFIX='H'
            fullname = data+'/PAO/'+name+SUFFIX+'.pao'

            if not os.path.exists(fullname):
                # 正規表現でPAOディレクトリ内の検索
                SUFFIX='dir'
                paolist = []
                pao_txt = atom+'[0-9].*'+'\.pao'
                pao_reg = re.compile( pao_txt )
                for file in dircache.listdir(data+'/PAO/'):
                    if pao_reg.search(file):
                        paolist.append(file)
    if SUFFIX != 'dir':
        print 'CUT  :',cut
        print 'PATH :',fullname
        print 'PAO  :',name
    else:
        for i in range(len(paolist)):
            print paolist[i]

#   vps = SAE.ReadMxVps(fullname)
#   electron = vps.get_valence_electron()


################################################################################

