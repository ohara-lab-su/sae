################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 原子番号もしくは元素記号を渡すと原子半径を返すルーチン等
#
# atomic_radius.list ファイルが必要
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

#from LIB_vasp.read_list_param import *
#from LIB_vasp.read_list import *

import numpy as np
import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 

### 原子番号から原子半径を返す
def get_atomic_radius0(num):

    name='atomic_radius.list' 
    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if num == radius_list[i,0]:
            radius=float(radius_list[i,2])

    return radius


### 元素記号から原子半径を返す
def get_atomic_radius1(atom):

    name='atomic_radius.list' 
    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if atom == radius_list[i,1]:
            radius=float(radius_list[i,2])

    return radius


### 元素記号から原子番号を返す
def get_atomic_number1(atom):

    name='atomic_radius.list' 
    nlist = SAE.read_list_param(name)

    radius_list = np.zeros((nlist,3),dtype='S4')
    nlist = SAE.read_list3(name,radius_list)

    for i in range(nlist):
        if atom == radius_list[i,1]:
            num=float(radius_list[i,0])

    return num
