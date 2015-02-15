#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OUTCAR 読み込み, ION-LOOP 毎の原子位置(&力)読み込み専用
#   
# [in]     canme  : OUTCARの名前
# [in]     natom  : 総原子数
# [return] nloop  : LOOP数
#
################################################################################
#
# 2015.01.09
#   圧縮ファイル対応版へ
#
# 2014.?? startup
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
__version__    = "0.0.2"                                                                  
################################################################################

import sys
import gzip
import os
import re
from numpy import *

################################################################################
def read_outcar_position(cname,natom,nloop,position_loop,force_loop):

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

    datlines = datfile.split('\n')

    num = len(datlines) -1

    nion_reg    = re.compile('.*NIONS = '        ,re.IGNORECASE)    
    tforce_reg  = re.compile('.*TOTAL-FORCE'     ,re.IGNORECASE)
    tvector_reg = re.compile('.*Lattice vectors:',re.IGNORECASE)
    a_reg       = re.compile('.*ALAT       ='    ,re.IGNORECASE)
    potcar_reg  = re.compile('.*POTCAR:'         ,re.IGNORECASE)

    # POSCAR を読み込むのと同等の情報＋アルファを OUTCAR から読み込む
    n_local = 0 
    for i in range(num):

        # 原子の種類数NION*2
        if bool(potcar_reg.match(datlines[i])):
           #print datlines[i]
            n_local += 1

        # 原子の総数 (NATOM)
        if bool(nion_reg.match(datlines[i])):
            lines = datlines[i].split()
            natom_local=int(lines[11])

        # スケールファクター
        if bool(a_reg.match(datlines[i])):
            tmp = datlines[i].split()
            scale_local=float(tmp[2])
           #print scale_local

        # 基本並進ベクトル
        if bool(tvector_reg.match(datlines[i])):
            t1_local = filter(lambda w: len(w) > 0, re.split(r'\s|"|,|\)|\(|=', datlines[i+2]))
            t1_x_local=float(t1_local[1])/scale_local
            t1_y_local=float(t1_local[2])/scale_local
            t1_z_local=float(t1_local[3])/scale_local
            t2_local = filter(lambda w: len(w) > 0, re.split(r'\s|"|,|\)|\(|=', datlines[i+3]))
            t2_x_local=float(t2_local[1])/scale_local
            t2_y_local=float(t2_local[2])/scale_local
            t2_z_local=float(t2_local[3])/scale_local
            t3_local = filter(lambda w: len(w) > 0, re.split(r'\s|"|,|\)|\(|=', datlines[i+4]))
            t3_x_local=float(t3_local[1])/scale_local
            t3_y_local=float(t3_local[2])/scale_local
            t3_z_local=float(t3_local[3])/scale_local
           #print t1_x,t1_y,t1_z
           #print t2_x,t2_y,t2_z
           #print t3_x,t3_y,t3_z

    if natom != natom_local:
        sys.exit("OUTCAR is inconsistent with POSCAR")

    # 原子に働く力(およびステップごとの座標の読み込み
    loop = 0
    for i in range(num):
        if bool(tforce_reg.match(datlines[i])):
            for j in range(natom):
                tmp = datlines[i+j+2].split()
                position_loop[loop,j,0] = float(tmp[0])
                position_loop[loop,j,1] = float(tmp[1])
                position_loop[loop,j,2] = float(tmp[2])
                force_loop[loop,j,0]    = float(tmp[3])
                force_loop[loop,j,1]    = float(tmp[4])
                force_loop[loop,j,2]    = float(tmp[5])
            loop += 1

################################################################################
     
