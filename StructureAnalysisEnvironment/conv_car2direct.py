################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# POSCAR の内部座標を cartesian 系から direct 系へ変換
#
# [in]     scale          : 基本並進にかかるスケール(変換前)
#
# [in/out] t[3,3]         : 基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in]     natom          : number of atom
# [in]     direct         : 入力のモード(入力がdirectならば安全のために止める)
#
# [in/out] position[j,3]  : 通し番号(max=natom)とx,y,z 指定で内部座標
#
# [return] direct         : direct = True (変換をしたので direct は True)
# [return] scale          : なにかやった sale を返す(何かは未実装)
#
################################################################################
#
# 2015.06.17
#  conv_car2direct1() 戻り値が異なるだけのバージョンを追加
#
# 2014.11.04
#   bug fix
#
# 2014.10.31 1st
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
#import os
#import re
#from numpy import *
import numpy as np
#from copy import deepcopy

def conv_car2direct(scale,t,natom,direct,position):

    if direct:
        sys.exit("STOP: curret mode is Direct.")

    a11 = t[0,0]  # t1_x = t[0,0]
    a21 = t[1,0]  # t1_y = t[1,0]
    a31 = t[2,0]  # t1_z = t[2,0]

    a12 = t[0,1]  # t2_x = t[0,1]
    a22 = t[1,1]  # t2_y = t[1,1]
    a32 = t[2,1]  # t2_z = t[2,1]

    a13 = t[0,2]  # t3_x = t[0,2]
    a23 = t[1,2]  # t3_y = t[1,2]
    a33 = t[2,2]  # t3_z = t[2,2]


    det =   a11*a22*a33 + a21*a32*a13 + a31*a12*a23 \
          - a11*a32*a23 - a31*a22*a13 - a21*a12*a33

    t11 = (a22*a33 - a23*a32)/det;
    t21 = (a23*a31 - a21*a33)/det;
    t31 = (a21*a32 - a22*a31)/det;

    t12 = (a13*a32 - a12*a33)/det;
    t22 = (a11*a33 - a13*a31)/det;
    t32 = (a12*a31 - a11*a32)/det;

    t13 = (a12*a23 - a13*a22)/det;
    t23 = (a13*a21 - a11*a23)/det;
    t33 = (a11*a22 - a12*a21)/det;

    dp = np.zeros((natom,3))
    for j in range(natom):
        dp[j,0] = t11*position[j,0] + t12*position[j,1] + t13*position[j,2]
        dp[j,1] = t21*position[j,0] + t22*position[j,1] + t23*position[j,2]
        dp[j,2] = t31*position[j,0] + t32*position[j,1] + t33*position[j,2]

#   position = deepcopy(dp)
    for j in range(natom):
        position[j,0] = dp[j,0]
        position[j,1] = dp[j,1]
        position[j,2] = dp[j,2]

    direct = True
    return [scale,direct]


# conv_car2direct() と同じで、戻り値が異なるだけ
def conv_car2direct1(scale,t,natom,direct,position):

    if direct:
        sys.exit("STOP: curret mode is Direct.")

    a11 = t[0,0]  # t1_x = t[0,0]
    a21 = t[1,0]  # t1_y = t[1,0]
    a31 = t[2,0]  # t1_z = t[2,0]

    a12 = t[0,1]  # t2_x = t[0,1]
    a22 = t[1,1]  # t2_y = t[1,1]
    a32 = t[2,1]  # t2_z = t[2,1]

    a13 = t[0,2]  # t3_x = t[0,2]
    a23 = t[1,2]  # t3_y = t[1,2]
    a33 = t[2,2]  # t3_z = t[2,2]


    det =   a11*a22*a33 + a21*a32*a13 + a31*a12*a23 \
          - a11*a32*a23 - a31*a22*a13 - a21*a12*a33

    t11 = (a22*a33 - a23*a32)/det;
    t21 = (a23*a31 - a21*a33)/det;
    t31 = (a21*a32 - a22*a31)/det;

    t12 = (a13*a32 - a12*a33)/det;
    t22 = (a11*a33 - a13*a31)/det;
    t32 = (a12*a31 - a11*a32)/det;

    t13 = (a12*a23 - a13*a22)/det;
    t23 = (a13*a21 - a11*a23)/det;
    t33 = (a11*a22 - a12*a21)/det;

    dp = np.zeros((natom,3))
    for j in range(natom):
        dp[j,0] = t11*position[j,0] + t12*position[j,1] + t13*position[j,2]
        dp[j,1] = t21*position[j,0] + t22*position[j,1] + t23*position[j,2]
        dp[j,2] = t31*position[j,0] + t32*position[j,1] + t33*position[j,2]

#   position = deepcopy(dp)
    for j in range(natom):
        position[j,0] = dp[j,0]
        position[j,1] = dp[j,1]
        position[j,2] = dp[j,2]

    direct = True
    return [scale,t,natom,direct,position]

