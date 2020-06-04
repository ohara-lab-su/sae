#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# ReadVaspChgcar クラスから分離して関数化した Method
#
################################################################################
from __future__ import print_function
from copyright import *
################################################################################

import numpy as np
import math

# using jit
from numba import jit


@jit
def sphere_integral_of_elf(chgcar, ngxc, ngyz, ngzc, rate_x, rate_y, rate_z, r_diff=1.0):
    """
    ある原点からのある半径内での ELF の平均値
    特定関数の高速化のために Class から分離・整理

    事前に chg/elf の 3x3x3 スーパーセルを作っておく必要がある

    self.chgdata_s[nx, ny, nz]
    self.ngxc
    self.ngyz
    self.ngzc
    self.rate_x
    self.rate_y
    self.rate_z
    self.ave_elf

    :param chgcar:
    :param ngxc:
    :param ngyz:
    :param ngzc:
    :param rate_x:
    :param rate_y:
    :param rate_z:
    :param r_diff: 半径
    :return: self.ave_elf[nx, ny, nz]: CHGCAR 形式(FFT-MESHパートのみ)のマトリックス
    """

    #
    # ある原点からのある半径内での ELF の平均値
    #
    # base となる(中心となる) cell = [ nx + sx[2], ny + sy[2], nz + sz[2])
    # ある cell の中心 nx=0, ny=0, nz=0 からある半径 r 内の mesh ポイントを探す
    #
    # 1. 原点と cell 内 mesh 点の差をとする
    #    その際、mesh-mesh の distance を実長さ換算する
    # 1. super_cell と 原点の差を全て探す(mesh-dataのみ)
    #
    #

    chgdata_s = chgcar

    # r_diff = 1.0 # Angstrom

    ### 3x3 の super-cell を作った場合の原点 shift
    #
    sx = [0, ngxc, ngxc * 2]  # supre-cell 用の Meth 原点
    sy = [0, ngyz, ngyz * 2]
    sz = [0, ngzc, ngzc * 2]

    # ある原点を中心とした ELF の平均値を取るための、ある半径の体積の計算
    v = 4.0 / 3.0 * math.pi * r_diff ** 3  # Volume /A^3

    # 初期化
    ave_elf = np.zeros((ngxc, ngyz, ngzc))

    print("search ...")
    for org_nx in range(0, ngxc):
        for org_ny in range(0, ngyz):
            for org_nz in range(0, ngzc):
                # ある原点からの ある半径内の ELF の平均値を計算する
                org = [org_nx + sx[2], org_ny + sy[2], org_nz + sz[2]]
                elf_sum = 0
                print("search (%d,%d,%d) ..." % (org_nx, org_ny, org_nz), end="")
                for nx in range(0, ngxc * 3):
                    for ny in range(0, ngyz * 3):
                        for nz in range(0, ngzc * 3):
                            # 二点間の距離
                            r = math.sqrt(((org[0] - nx) * rate_x) ** 2
                                          + ((org[1] - ny) * rate_y) ** 2
                                          + ((org[2] - nz) * rate_z) ** 2)
                            if r < r_diff:
                                elf_sum += chgdata_s[nx, ny, nz]
                            # print(nx, ny, nz, self.chgdata_s[nx, ny, nz])

                ave_elf[org_nx, org_ny, org_nz] = elf_sum / v  # 体積中のELFの平均値(ELF/A^3)
                print(" ave_elf=%f" % ave_elf[org_nx, org_ny, org_nz])

    return ave_elf
