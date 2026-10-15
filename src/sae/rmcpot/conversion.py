# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
import numpy as np
import re
from numpy import *


class RmcConversions:

    def change_density(self, STD, datname, outname, density):
        tmp = open(datname + ".dat")
        datfile = tmp.read()
        tmp.close
        datlines = datfile.split("\n")
        nline = len(datlines)
        header = datlines[0]
        lines = datlines[1].split()
        n = len(lines)
        if STD:
            out = sys.stdout
        else:
            out = open(outname + ".dat", "w")
        print(datlines[0].rstrip(), file=out)
        lines[0] = density
        for i in range(n):
            print(lines[i], file=out, end="")
        print("", file=out)
        for i in range(2, nline):
            print(datlines[i].rstrip(), file=out)
        out.close
        return

    def conv_cfg2vaspa(self, scale, t, natom, direct, position):
        """
        :param scale:
        :param t:
        :param natom:
        :param direct:
        :param position:
        :return:
        """
        if not direct:
            sys.exit("STOP: input file is not direct mode")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        t1_x = t1_x * 2
        t1_y = t1_y * 2
        t1_z = t1_z * 2
        t2_x = t2_x * 2
        t2_y = t2_y * 2
        t2_z = t2_z * 2
        t3_x = t3_x * 2
        t3_y = t3_y * 2
        t3_z = t3_z * 2
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        for i in range(int(natom)):
            position[i, 0] = position[i, 0] / 2 + x_offset
            position[i, 1] = position[i, 1] / 2 + y_offset
            position[i, 2] = position[i, 2] / 2 + z_offset
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
        direct = True
        return (scale, direct)

    def conv_vasp2cfga(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP: input file is not direct mode")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        t1_x = scale0 * t1_x / 2.0
        t1_y = scale0 * t1_y / 2.0
        t1_z = scale0 * t1_z / 2.0
        t2_x = scale0 * t2_x / 2.0
        t2_y = scale0 * t2_y / 2.0
        t2_z = scale0 * t2_z / 2.0
        t3_x = scale0 * t3_x / 2.0
        t3_y = scale0 * t3_y / 2.0
        t3_z = scale0 * t3_z / 2.0
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        for j in range(int(natom)):
            position[j, 0] = (position[j, 0] - x_offset) * 2.0
            position[j, 1] = (position[j, 1] - y_offset) * 2.0
            position[j, 2] = (position[j, 2] - z_offset) * 2.0
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
        direct = True
        return [scale, direct]

    def conv_vasp2cfg(self, scale0, t, natom, direct, position):
        if not direct:
            sys.exit("STOP: input file is not direct mode")
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        t1_x = scale0 * t1_x / 2.0
        t1_y = scale0 * t1_y / 2.0
        t1_z = scale0 * t1_z / 2.0
        t2_x = scale0 * t2_x / 2.0
        t2_y = scale0 * t2_y / 2.0
        t2_z = scale0 * t2_z / 2.0
        t3_x = scale0 * t3_x / 2.0
        t3_y = scale0 * t3_y / 2.0
        t3_z = scale0 * t3_z / 2.0
        x_offset = 0.5
        y_offset = 0.5
        z_offset = 0.5
        for j in range(int(natom)):
            position[j, 0] = (position[j, 0] - x_offset) * 2.0
            position[j, 1] = (position[j, 1] - y_offset) * 2.0
            position[j, 2] = (position[j, 2] - z_offset) * 2.0
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
        direct = True
        return (scale, t, natom, direct, position)
