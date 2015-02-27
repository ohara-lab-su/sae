################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の基本並進ベクトルのスケーリングを 1.0 にする
#    1) VASP の car mode はスケールしてないので内部座標には影響を受けない
#    2) direce mode ではそもそもスケールファクターに内部座標は影響は受けない
#
#      --> 並進ベクトルだけスケールする
#
#
# [in]     scale0         : 基本並進にかかるスケール(変換前)
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [return] scale          : 一応 scale = 1.0 を返しておく
#                           そもそもこのルーチンの使用前提が scale 1.0 を返すことある
#
################################################################################
#
# 2015.02.27
#  conv_scale21  (旧バージョン,そのまま)
#  conv_scale21r (新バージョン,戻り値版)
#
# 2015.02.27
#  引数ではなく戻り値で値を返す同名の関数を作成
#   引数/戻り値を conv_direct2car_return と同一のものにする
#   ただし、ABS は外す
#
# 2014.11.04 1st
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014-2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.2"
################################################################################

#import sys
#import os
#import re
#from copy import deepcopy

#import numpy as np

################################################################################
# 引数版
def conv_scale21(scale0,t):

    ##
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
    ## 基本並進ベクトルをスケールしておく
    ## --> scale=1.0 とするため
    ##
    t1_x = t1_x*scale0
    t1_y = t1_y*scale0
    t1_z = t1_z*scale0
    
    t2_x = t2_x*scale0
    t2_y = t2_y*scale0
    t2_z = t2_z*scale0
    
    t3_x = t3_x*scale0
    t3_y = t3_y*scale0
    t3_z = t3_z*scale0


    t[0,0] = t1_x
    t[1,0] = t1_y
    t[2,0] = t1_z

    t[0,1] = t2_x
    t[1,1] = t2_y
    t[2,1] = t2_z

    t[0,2] = t3_x
    t[1,2] = t3_y
    t[2,2] = t3_z

    scale = 1.0

    return scale


################################################################################
# 戻り値版
#  戻り値は conv_direct2car_return とほぼ同一
#
def conv_scale21r(scale0,t,natom,direct,position):

    t = t*scale0
    scale = 1.0

    poscar =  [scale,t,natom,direct,position]
    return poscar

