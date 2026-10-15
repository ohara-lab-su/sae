# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import optparse
from numpy import *
import re


class RmcConfigFields:

    def read_cfg(self, cname, t, atoms, ion_site, position):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        header = str(datlines[0])
        comment = str(datlines[1])
        tmp = datlines[2]
        tmp = datlines[3]
        moves = datlines[4]
        saved = datlines[5]
        tmp = datlines[6]
        a = datlines[7].split()
        natom = int(a[0])
        a = datlines[8].split()
        nion = int(a[0])
        nmoles = datlines[9]
        angles = datlines[10]
        tmp = datlines[11]
        tmp = datlines[12]
        tmp = datlines[13]
        v = datlines[14].split()
        t1_x = float(v[0])
        t1_y = float(v[1])
        t1_z = float(v[2])
        v = datlines[15].split()
        t2_x = float(v[0])
        t2_y = float(v[1])
        t2_z = float(v[2])
        v = datlines[16].split()
        t3_x = float(v[0])
        t3_y = float(v[1])
        t3_z = float(v[2])
        t[0, 0] = float(t1_x)
        t[1, 0] = float(t1_y)
        t[2, 0] = float(t1_z)
        t[0, 1] = float(t2_x)
        t[1, 1] = float(t2_y)
        t[2, 1] = float(t2_z)
        t[0, 2] = float(t3_x)
        t[1, 2] = float(t3_y)
        t[2, 2] = float(t3_z)
        tmp = datlines[17]
        lines = 17
        for i in range(int(nion)):
            lines += 1
            n = datlines[lines].split()
            atoms[i] = int(n[0])
            lines += 1
            tmp = datlines[lines]
            lines += 1
            tmp = datlines[lines]
            lines += 1
            tmp = datlines[lines]
        index = 0
        for j in range(nion):
            for k in range(atoms[j]):
                ion_site[index] = j
                index += 1
        for i in range(int(natom)):
            lines += 1
            xyz = datlines[lines].split()
            position[i, 0] = xyz[0]
            position[i, 1] = xyz[1]
            position[i, 2] = xyz[2]
        return [header, comment]

    def read_cfg_coll(
        self, cname, nloop, t, natom, nion, atoms, ion_site, position_loop
    ):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_coll.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        lines = 0
        for loop in range(nloop):
            header = datlines[lines]
            comment = datlines[lines + 1]
            moves = datlines[lines + 4]
            saved = datlines[lines + 5]
            tmp = datlines[lines + 7].split()
            natom0 = int(tmp[0])
            if natom0 != natom:
                sys.exit("NATOM is inconsistent (read_cfg_coll.py)")
            tmp = datlines[lines + 8].split()
            nion0 = int(tmp[0])
            if nion0 != nion:
                sys.exit("NION is inconsistent (read_cfg_coll.py)")
            nmoles = datlines[lines + 9]
            angles = datlines[lines + 10]
            t1 = datlines[lines + 14].split()
            t1_x = float(t1[0])
            t1_y = float(t1[1])
            t1_z = float(t1[2])
            t2 = datlines[lines + 15].split()
            t2_x = float(t2[0])
            t2_y = float(t2[1])
            t2_z = float(t2[2])
            t3 = datlines[lines + 16].split()
            t3_x = float(t3[0])
            t3_y = float(t3[1])
            t3_z = float(t3[2])
            t[0, 0] = t1_x
            t[1, 0] = t1_y
            t[2, 0] = t1_z
            t[0, 1] = t2_x
            t[1, 1] = t2_y
            t[2, 1] = t2_z
            t[0, 2] = t3_x
            t[1, 2] = t3_y
            t[2, 2] = t3_z
            lines = lines + 18
            for i in range(nion):
                tmp = datlines[lines].split()
                atoms[i] = int(tmp[0])
                lines = lines + 4
            index = 0
            for j in range(nion):
                for k in range(int(atoms[j])):
                    ion_site[index] = j
                    index += 1
            for i in range(natom):
                xyz = datlines[lines].split()
                position_loop[loop, i, 0] = xyz[0]
                position_loop[loop, i, 1] = xyz[1]
                position_loop[loop, i, 2] = xyz[2]
                lines += 1
            lines = lines + 1
        scale = 1.0
        direct = True
        return [header, comment, scale, direct]

    def read_cfg_coll_param(self, cname):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_coll_param.py): " + cname + " not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        lines = 0
        t = datlines[lines + 7].split()
        natom = int(t[0])
        t = datlines[lines + 8].split()
        nion = int(t[0])
        lines = lines + 18
        lines = lines + nion * 4
        lines = lines + natom
        lines = lines + 1
        max_lines = lines
        nloop = num / max_lines
        return (nloop, natom, nion)

    def read_cfg_param(self, cname):
        try:
            tmp = open(cname + ".cfg")
        except:
            tmp.close()
            sys.exit("Error(read_cfg_param.py): " + cname + ".cfg not open")
        datfile = tmp.read()
        tmp.close()
        datlines = datfile.split("\n")
        a = datlines[7].split()
        natom = int(a[0])
        a = datlines[8].split()
        nion = int(a[0])
        return [natom, nion]
