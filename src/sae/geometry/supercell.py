# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import optparse
from numpy import *
from copy import deepcopy


class SupercellOperations:

    def make_supercell0(
        self,
        super_x,
        super_y,
        super_z,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        super = int(super_x) * int(super_y) * int(super_z)
        nsv = 0
        for n in range(super_x):
            for l in range(super_y):
                for m in range(super_z):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j

    def make_supercell1(
        self,
        super_x,
        super_y,
        super_z,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
        fix,
        fix_sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        super = int(super_x) * int(super_y) * int(super_z)
        nsv = 0
        for n in range(super_x):
            for l in range(super_y):
                for m in range(super_z):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    fix_sp[nsp, 0] = fix[j, 0]
                    fix_sp[nsp, 1] = fix[j, 1]
                    fix_sp[nsp, 2] = fix[j, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j

    def make_supercell_param(self, super_x, super_y, super_z, nion, atoms, t):
        t[0, 0] = t[0, 0] * super_x
        t[1, 0] = t[1, 0] * super_y
        t[2, 0] = t[2, 0] * super_z
        t[0, 1] = t[0, 1] * super_x
        t[1, 1] = t[1, 1] * super_y
        t[2, 1] = t[2, 1] * super_z
        t[0, 2] = t[0, 2] * super_x
        t[1, 2] = t[1, 2] * super_y
        t[2, 2] = t[2, 2] * super_z
        for j in range(nion):
            atoms[j] = int(atoms[j]) * super_x * super_y * super_z

    def make_supercell_zb(
        self,
        t,
        natom,
        nion,
        atoms,
        ion,
        ion_local,
        position,
        sv,
        ion_sp,
        ion_local_sp,
        sp_j,
        sp,
    ):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        super_x = 3
        super_y = 3
        super_z = 3
        super = int(super_x * super_y * super_z)
        nsv = 0
        for n in range(-1, 2):
            for l in range(-1, 2):
                for m in range(-1, 2):
                    sv[nsv, 0] = t1_x * n + t2_x * l + t3_x * m
                    sv[nsv, 1] = t1_y * n + t2_y * l + t3_y * m
                    sv[nsv, 2] = t1_z * n + t2_z * l + t3_z * m
                    nsv += 1
        j = -1
        nsp = -1
        for k in range(nion):
            for kk in range(int(atoms[k])):
                j += 1
                for nsv in range(super):
                    nsp += 1
                    nsp_ = natom * nsv + j
                    sp[nsp, 0] = position[j, 0] + sv[nsv, 0]
                    sp[nsp, 1] = position[j, 1] + sv[nsv, 1]
                    sp[nsp, 2] = position[j, 2] + sv[nsv, 2]
                    ion_sp[nsp] = ion[j]
                    ion_local_sp[nsp] = ion_local[j]
                    sp_j[nsp] = j
