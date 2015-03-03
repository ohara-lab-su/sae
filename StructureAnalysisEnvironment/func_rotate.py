################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 回転関係の関数
#
################################################################################
#
# 2015.03.03
#   startup
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
#import os
#import re
import numpy as np
#from copy import deepcopy

################################################################################
# 応用群論 p.122 - p123
def rotate_z(deg):
    r = np.radians(deg)
    C = np.cos(r)
    S = np.sin(r)
    # z軸周りの回転行列
    R_z = np.matrix((                                                       
        ( C, -S, 0),                                                         
        ( S,  C, 0),                                                         
        ( 0,  0, 1)                                                          
    ))
    return R_z

def rotate_y(deg):
    r = np.radians(deg)
    C = np.cos(r)
    S = np.sin(r)
    # z軸周りの回転行列
    R_y = np.matrix((                                                       
        ( C,  0, S),                                                         
        ( 0,  1, 0),                                                         
        (-S,  0, C)                                                          
    ))
    return R_y

def rotate_euler(alpha,beta,gamma):
    R_alpha_z = rotate_z(alpha)
    R_beta_y  = rotate_y(beta)
    R_gamma_z = rotate_z(gamma)

    R_euler = R_alpha_z * R_beta_y * R_gamma_z

    return R_euler

################################################################################
