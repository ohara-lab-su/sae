#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# for Vpython (and VTK)
#
# 結晶を描くときの単位胞の描画につかうルーチン
# 基本呼び出すだけ
#
# [in/(out)] t[3,3]         :  基本並進ベクトル(注意:配列内indexは0から)
#                                  x   y   z
#                            t1 = a11 a21 a31
#                            t2 = a12 a22 a32
#                            t3 = a13 a23 a33
#
# [in/(out)] O(3)            : 単位胞の原点(0,0,0)ではなくて少しずらすのが描画上幸せ
# [in/(out)] C(3)            : 単位胞の箱の色(R,G,B)
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

#from __future__ import division
#from visual import *
import visual as vp

################################################################################
# origin: 結晶描画の単位胞の座標原点
# radius: 珠の大きさ
# color: [255,255,255] # white
################################################################################
def crystal_make_unit(t,origin=[-0.5,-0.5,0],radius=0.05,color=[255,255,255]):

    t1_x = t[0,0]
    t1_y = t[1,0]
    t1_z = t[2,0]

    t2_x = t[0,1]
    t2_y = t[1,1]
    t2_z = t[2,1]

    t3_x = t[0,2]
    t3_y = t[1,2]
    t3_z = t[2,2]

    # 結晶描画の単位胞の座標原点
   #O = [ -3,-3,0 ]

    Ox = origin[0]
    Oy = origin[1]
    Oz = origin[2]

    # 基本並進ベクトル
    t1 = vp.cylinder(pos=(Ox,Oy,Oz), axis=(t1_x,t1_y,t1_z), radius=radius)
    t2 = vp.cylinder(pos=(Ox,Oy,Oz), axis=(t2_x,t2_y,t2_z), radius=radius)
    t3 = vp.cylinder(pos=(Ox,Oy,Oz), axis=(t3_x,t3_y,t3_z), radius=radius)

    # 基本並進ベクトルによって囲まれる単位胞の箱を構成する(12-3)本のベクトル
    t31  = vp.cylinder(pos=(t3_x+Ox,t3_y+Oy,t3_z+Oz), axis=(t1_x,t1_y,t1_z), radius=radius)
    t32  = vp.cylinder(pos=(t3_x+Ox,t3_y+Oy,t3_z+Oz), axis=(t2_x,t2_y,t2_z), radius=radius)
    t13  = vp.cylinder(pos=(t1_x+Ox,t1_y+Oy,t1_z+Oz), axis=(t3_x,t3_y,t3_z), radius=radius)
    t23  = vp.cylinder(pos=(t2_x+Ox,t2_y+Oy,t2_z+Oz), axis=(t3_x,t3_y,t3_z), radius=radius)
    t12  = vp.cylinder(pos=(t1_x+Ox,t1_y+Oy,t1_z+Oz), axis=(t2_x,t2_y,t2_z), radius=radius)
    t21  = vp.cylinder(pos=(t2_x+Ox,t2_y+Oy,t2_z+Oz), axis=(t1_x,t1_y,t1_z), radius=radius)

    v12x = t1_x + t2_x
    v12y = t1_y + t2_y
    v12z = t1_z + t2_z
    t123 = vp.cylinder(pos=(v12x+Ox,v12y+Oy,v12z+Oz), axis=(t3_x,t3_y,t3_z), radius=radius)

    v31x = t3_x + t1_x
    v31y = t3_y + t1_y
    v31z = t3_z + t1_z
    t312 = vp.cylinder(pos=(v31x+Ox,v31y+Oy,v31z+Oz), axis=(t2_x,t2_y,t2_z), radius=radius)

    v32x = t3_x + t2_x
    v32y = t3_y + t2_y
    v32z = t3_z + t2_z
    t321 = vp.cylinder(pos=(v32x+Ox,v32y+Oy,v32z+Oz), axis=(t1_x,t1_y,t1_z), radius=radius)

    # 単位胞を構成する箱の色設定
    t1.color   = color
    t2.color   = color
    t3.color   = color
    t31.color  = color
    t32.color  = color
    t13.color  = color
    t23.color  = color
    t12.color  = color
    t21.color  = color
    t123.color = color
    t312.color = color
    t321.color = color


