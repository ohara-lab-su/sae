# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import numpy as np
from ase.io.wien2k import *
from ase import Atoms


class CoordinateTransforms:

    def conv_car2carABSa(self, scale0, t, natom, direct, position):
        if direct:
            sys.exit("STOP: current is Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        scale = 1.0
        for j in range(natom):
            position[j, 0] = position[j, 0] * scale0
            position[j, 1] = position[j, 1] * scale0
            position[j, 2] = position[j, 2] * scale0
        t1_x = t1_x * scale0
        t1_y = t1_y * scale0
        t1_z = t1_z * scale0
        t2_x = t2_x * scale0
        t2_y = t2_y * scale0
        t2_z = t2_z * scale0
        t3_x = t3_x * scale0
        t3_y = t3_y * scale0
        t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        return scale

    def conv_car2carABS(self, scale0, t, natom, direct, position):
        if direct:
            sys.exit("STOP: current is Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        scale = 1.0
        p = np.zeros((natom, 3))
        for j in range(natom):
            p[j, 0] = position[j, 0] * scale0
            p[j, 1] = position[j, 1] * scale0
            p[j, 2] = position[j, 2] * scale0
        t1_x = t1_x * scale0
        t1_y = t1_y * scale0
        t1_z = t1_z * scale0
        t2_x = t2_x * scale0
        t2_y = t2_y * scale0
        t2_z = t2_z * scale0
        t3_x = t3_x * scale0
        t3_y = t3_y * scale0
        t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        return [scale, t, natom, direct, p]

    def conv_car2directa(self, scale, t, natom, direct, position):
        if direct:
            sys.exit("STOP: curret mode is Direct.")
        a11 = t[0, 0]
        a21 = t[1, 0]
        a31 = t[2, 0]
        a12 = t[0, 1]
        a22 = t[1, 1]
        a32 = t[2, 1]
        a13 = t[0, 2]
        a23 = t[1, 2]
        a33 = t[2, 2]
        det = (
            a11 * a22 * a33
            + a21 * a32 * a13
            + a31 * a12 * a23
            - a11 * a32 * a23
            - a31 * a22 * a13
            - a21 * a12 * a33
        )
        t11 = (a22 * a33 - a23 * a32) / det
        t21 = (a23 * a31 - a21 * a33) / det
        t31 = (a21 * a32 - a22 * a31) / det
        t12 = (a13 * a32 - a12 * a33) / det
        t22 = (a11 * a33 - a13 * a31) / det
        t32 = (a12 * a31 - a11 * a32) / det
        t13 = (a12 * a23 - a13 * a22) / det
        t23 = (a13 * a21 - a11 * a23) / det
        t33 = (a11 * a22 - a12 * a21) / det
        dp = np.zeros((natom, 3))
        for j in range(natom):
            dp[j, 0] = (
                t11 * position[j, 0] + t12 * position[j, 1] + t13 * position[j, 2]
            )
            dp[j, 1] = (
                t21 * position[j, 0] + t22 * position[j, 1] + t23 * position[j, 2]
            )
            dp[j, 2] = (
                t31 * position[j, 0] + t32 * position[j, 1] + t33 * position[j, 2]
            )
        for j in range(natom):
            position[j, 0] = dp[j, 0]
            position[j, 1] = dp[j, 1]
            position[j, 2] = dp[j, 2]
        direct = True
        return [scale, direct]

    def conv_car2direct(self, scale, t, natom, direct, position):
        if direct:
            sys.exit("STOP: curret mode is Direct.")
        a11 = t[0, 0]
        a21 = t[1, 0]
        a31 = t[2, 0]
        a12 = t[0, 1]
        a22 = t[1, 1]
        a32 = t[2, 1]
        a13 = t[0, 2]
        a23 = t[1, 2]
        a33 = t[2, 2]
        det = (
            a11 * a22 * a33
            + a21 * a32 * a13
            + a31 * a12 * a23
            - a11 * a32 * a23
            - a31 * a22 * a13
            - a21 * a12 * a33
        )
        t11 = (a22 * a33 - a23 * a32) / det
        t21 = (a23 * a31 - a21 * a33) / det
        t31 = (a21 * a32 - a22 * a31) / det
        t12 = (a13 * a32 - a12 * a33) / det
        t22 = (a11 * a33 - a13 * a31) / det
        t32 = (a12 * a31 - a11 * a32) / det
        t13 = (a12 * a23 - a13 * a22) / det
        t23 = (a13 * a21 - a11 * a23) / det
        t33 = (a11 * a22 - a12 * a21) / det
        dp = np.zeros((natom, 3))
        for j in range(natom):
            dp[j, 0] = (
                t11 * position[j, 0] + t12 * position[j, 1] + t13 * position[j, 2]
            )
            dp[j, 1] = (
                t21 * position[j, 0] + t22 * position[j, 1] + t23 * position[j, 2]
            )
            dp[j, 2] = (
                t31 * position[j, 0] + t32 * position[j, 1] + t33 * position[j, 2]
            )
        for j in range(natom):
            position[j, 0] = dp[j, 0]
            position[j, 1] = dp[j, 1]
            position[j, 2] = dp[j, 2]
        direct = True
        return (scale, t, natom, direct, position)

    def conv_cellparam(self, atoms):
        return

    def conv_cellparam0(self, atoms):
        cell = atoms.get_cell()
        metT = np.dot(cell, np.transpose(cell))
        cell2 = cellconst(metT)
        a = cell2[0]
        b = cell2[1]
        c = cell2[2]
        alpha = cell2[3]
        beta = cell2[4]
        gamma = cell2[5]
        natom = len(atoms.get_positions())
        return (a, b, c, alpha, beta, gamma, natom)

    def conv_cellparam1(self, cell):
        t = cell.t
        metT = np.dot(t, np.transpose(t))
        param = cellconst(metT)
        a = param[0]
        b = param[1]
        c = param[2]
        alpha = param[3]
        beta = param[4]
        gamma = param[5]
        natom = cell.natom
        return (a, b, c, alpha, beta, gamma, natom)

    def conv_direct2cara(self, ABS, scale0, t, natom, direct, position):
        """

        :param ABS:
        :param scale0:
        :param t:
        :param natom:
        :param direct:
        :param position:
        :return:
        """
        if not direct:
            sys.exit("STOP(conv_direct2car): current is not Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        car = np.zeros((natom, 3))
        for j in range(natom):
            car[j, 0] = (
                t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
            )
            car[j, 1] = (
                t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
            )
            car[j, 2] = (
                t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
            )
        if not ABS:
            scale = scale0
            scale0 = 1.0
        else:
            scale = 1.0
        for j in range(natom):
            position[j, 0] = car[j, 0] * scale0
            position[j, 1] = car[j, 1] * scale0
            position[j, 2] = car[j, 2] * scale0
        if ABS:
            t1_x = t1_x * scale0
            t1_y = t1_y * scale0
            t1_z = t1_z * scale0
            t2_x = t2_x * scale0
            t2_y = t2_y * scale0
            t2_z = t2_z * scale0
            t3_x = t3_x * scale0
            t3_y = t3_y * scale0
            t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = scale
        direct = False
        return [scale, direct]

    def conv_direct2car(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP(conv_direct2car): current is not Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        car = np.zeros((natom, 3))
        for j in range(natom):
            car[j, 0] = (
                t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
            )
            car[j, 1] = (
                t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
            )
            car[j, 2] = (
                t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
            )
        scale = scale0
        scale0 = 1.0
        for j in range(natom):
            position[j, 0] = car[j, 0] * scale0
            position[j, 1] = car[j, 1] * scale0
            position[j, 2] = car[j, 2] * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = scale
        direct = False
        poscar = (scale, t, natom, direct, position)
        return poscar

    def conv_direct2carABSa(self, ABS, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP(conv_direct2car): current is not Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        car = np.zeros((natom, 3))
        for j in range(natom):
            car[j, 0] = (
                t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
            )
            car[j, 1] = (
                t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
            )
            car[j, 2] = (
                t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
            )
        if not ABS:
            scale = scale0
            scale0 = 1.0
        else:
            scale = 1.0
        for j in range(natom):
            position[j, 0] = car[j, 0] * scale0
            position[j, 1] = car[j, 1] * scale0
            position[j, 2] = car[j, 2] * scale0
        if ABS:
            t1_x = t1_x * scale0
            t1_y = t1_y * scale0
            t1_z = t1_z * scale0
            t2_x = t2_x * scale0
            t2_y = t2_y * scale0
            t2_z = t2_z * scale0
            t3_x = t3_x * scale0
            t3_y = t3_y * scale0
            t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = scale
        direct = False
        return [scale, direct]

    def conv_direct2carABS(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP(conv_direct2car): current is not Direct.")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        car = np.zeros((natom, 3))
        for j in range(natom):
            car[j, 0] = (
                t1_x * position[j, 0] + t2_x * position[j, 1] + t3_x * position[j, 2]
            )
            car[j, 1] = (
                t1_y * position[j, 0] + t2_y * position[j, 1] + t3_y * position[j, 2]
            )
            car[j, 2] = (
                t1_z * position[j, 0] + t2_z * position[j, 1] + t3_z * position[j, 2]
            )
        scale = 1.0
        for j in range(natom):
            position[j, 0] = car[j, 0] * scale0
            position[j, 1] = car[j, 1] * scale0
            position[j, 2] = car[j, 2] * scale0
        t1_x = t1_x * scale0
        t1_y = t1_y * scale0
        t1_z = t1_z * scale0
        t2_x = t2_x * scale0
        t2_y = t2_y * scale0
        t2_z = t2_z * scale0
        t3_x = t3_x * scale0
        t3_y = t3_y * scale0
        t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = scale
        direct = False
        poscar = (scale, t, natom, direct, position)
        return poscar

    def conv_scale21a(self, scale0, t):
        """

        :param scale0: 変換する元の scale ファクタ
        :param t:  基本並進は引数で引き渡せる
        :return: scale, 変換結果
        """
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        t1_x = t1_x * scale0
        t1_y = t1_y * scale0
        t1_z = t1_z * scale0
        t2_x = t2_x * scale0
        t2_y = t2_y * scale0
        t2_z = t2_z * scale0
        t3_x = t3_x * scale0
        t3_y = t3_y * scale0
        t3_z = t3_z * scale0
        t[0, 0] = t1_x
        t[1, 0] = t1_y
        t[2, 0] = t1_z
        t[0, 1] = t2_x
        t[1, 1] = t2_y
        t[2, 1] = t2_z
        t[0, 2] = t3_x
        t[1, 2] = t3_y
        t[2, 2] = t3_z
        scale = 1.0
        return scale

    def conv_scale21(self, scale0, t, natom, direct, position):
        t = t * scale0
        scale = 1.0
        return (scale, t, natom, direct, position)
