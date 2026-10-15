# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASPの LORBIT 11 で動かした時の lm 番号から軌道名を取り出すだけの関数
#
# [in]  lm
# [return] orbital
#
################################################################################
################################################################################
#
# 2015.01.15 startup
#
################################################################################
# import sys
# import os
# import re
# from numpy import *
#
# s py pz px dxy dyz dz2 dxz dx2
#
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function


class VaspOrbitals:

    def get_vasp_orbital_info(self, lm):
        orbital_list = [
            "s",
            "p_y",
            "p_z",
            "p_x",
            "d_xy",
            "d_yz",
            "d_3z3-r2",
            "d_xz",
            "d_x2-y2",
        ]
        orbital = orbital_list[lm]
        return orbital
