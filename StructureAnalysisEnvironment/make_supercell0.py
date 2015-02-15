################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# make_supercell0
# スーパーセル作成ルーチン[内部座標作成]
#
# [in]      super_x
# [in]      super_y
# [in]      super_z
#
# [in/out]  sp [natom*super,3]          : SuPer cell position 保存用のverctor
# [in/out]  ion_sp [natom*super]        : SPセルの通し番号に対する原子種番号保存index
# [in/out]  ion_local_sp [natom*super]   : ion_local[j] の super cel index 対応版
# [in/out]  sp_j [natom*super]          : 通し番号の対応( 元のセル <---> SPセル )
#
################################################################################
#
# 2014.10.31
#   Vmake_SuperCell2.py ベース
#   1st version
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
import optparse
from numpy import *
from copy import deepcopy


def make_supercell0(super_x,super_y,super_z,\
                    t,natom,nion,atoms,ion,ion_local,position,\
                    sv,ion_sp,ion_local_sp,sp_j,sp):

    t1_x = t[0,0]
    t1_y = t[1,0]
    t1_z = t[2,0]

    t2_x = t[0,1]
    t2_y = t[1,1]
    t2_z = t[2,1]

    t3_x = t[0,2]
    t3_y = t[1,2]
    t3_z = t[2,2]

    ###############################################
    ## スーパーセル作成用の準備
    ## super index
    ##
    super= int(super_x)*int(super_y)*int(super_z)
    
    ###############################################
    ## super cell 作成用のベクトルを作る
    ##
   #sv = zeros((super,3)) # super cell vector
    nsv = 0
    for n in range((super_x)):
        for l in range((super_y)):
            for m in range((super_z)):
                sv[nsv,0] = t1_x*n + t2_x*l + t3_x*m
                sv[nsv,1] = t1_y*n + t2_y*l + t3_y*m
                sv[nsv,2] = t1_z*n + t2_z*l + t3_z*m
               #print nsv, " ", n,l,m," ",sv[nsv,0]
               #print nsv, " ", n,l,m," ",sv[nsv,1]
               #print nsv, " ", n,l,m," ",sv[nsv,2]
                nsv += 1
    
    
    ###############################################
    ## スーパーセルの内部座標作成
    ##
   #sp = zeros((natom*super,3)) # super cell position 保存用のvector
   #ion_sp= zeros(natom*super)  # super cell 通し番号に対する原子種番号保存index
   #ion_local_sp = zeros(natom*super) # ion_local[j] の super cell index 対応版
    
    # super cell の内部座標を作る
    j=-1
    nsp=-1
    for k in range(nion):
        for kk in range(int(atoms[k])):
    
            j += 1
    
            for nsv in range(super):
                nsp += 1
                nsp_ = natom*nsv+j
    
                sp[nsp,0] = position[j,0] + sv[nsv,0]
                sp[nsp,1] = position[j,1] + sv[nsv,1]
                sp[nsp,2] = position[j,2] + sv[nsv,2]
    
                # 元セルの通し番号を与えると、原子種番号を返す
                ion_sp[nsp] = ion[j]
                ion_local_sp[nsp] = ion_local[j]

                sp_j[nsp] = j
   
               ## for TEST print
               #x=sp[nsp,0]
               #y=sp[nsp,1]
               #z=sp[nsp,2]
               #print " %d,%d,  %d,%d,%s, %d,%d, %d  %s %12.8f %12.8f %12.8f" \
               #        %(j,nsp, k,ion_local_sp[nsp],atoms_index[k],  ion[j],ion_sp[nsp], kk,"  ",x,y,z)
    
    
    ## 元index と super index の対応を見る(テストプリント)
    #for k in range(nsp):
    #    print int(k), int(sp_j[k])
    #


    ################################################
    ### TEST: print super cell (VASP POSCAR, cartesian MODE)
    ###
    #print  " Makes Super Cell"
    #print  " 1.0"
    #print  "   %16.12f %16.12f %16.12f" %(t1_x*super_x, t1_y*super_y, t1_z*super_z)
    #print  "   %16.12f %16.12f %16.12f" %(t2_x*super_x, t2_y*super_y, t2_z*super_z)
    #print  "   %16.12f %16.12f %16.12f" %(t3_x*super_x, t3_y*super_y, t3_z*super_z)
    #if VASP > 4:
    #    for j in range(nion):
    #        print atoms_index[j],
    #    print ""
    #for j in range(nion):
    #    tmp = int(atoms[j])*int(super_x)*int(super_y)*int(super_z)
    #    print int(tmp),
    #print  ""
    #print  "Car"
    #
    #for j in range(natom*super):
    #    print "  %12.8f  %12.8f  %12.8f "  %(sp[j,0], sp[j,1], sp[j,2])


    #################################################
    ### TEST: write original cell
    ###
    #for j in range(natom):
    #    print "  %12.8f  %12.8f  %12.8f "  %(s[j,0], s[j,1], s[j,2])
