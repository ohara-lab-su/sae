# Copyright Kengo NAKADA; SAE class library.
import sys
import gzip
import os
import re
import optparse
from numpy import *


class OutcarFields:

    def read_outcar_param(self, cname, natom):
        if os.path.exists(cname):
            GZIP = False
        elif os.path.exists(cname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + cname + " or " + cname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(cname + ".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " or " + cname + ".gz does'nt open")
        finally:
            tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        nion_reg = re.compile(".*NIONS = ", re.IGNORECASE)
        tforce_reg = re.compile(".*TOTAL-FORCE", re.IGNORECASE)
        tvector_reg = re.compile(".*Lattice vectors:", re.IGNORECASE)
        a_reg = re.compile(".*ALAT       =", re.IGNORECASE)
        potcar_reg = re.compile(".*POTCAR:", re.IGNORECASE)
        for i in range(num):
            if bool(nion_reg.match(datlines[i])):
                lines = datlines[i].split()
                natom_outcar = int(lines[11])
        if natom != natom_outcar:
            sys.exit("OUTCAR is inconsistent with POSCAR")
        loop = 0
        for i in range(num):
            if bool(tforce_reg.match(datlines[i])):
                loop += 1
        return loop

    def read_outcar_position(self, cname, natom, nloop, position_loop, force_loop):
        if os.path.exists(cname):
            GZIP = False
        elif os.path.exists(cname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + cname + " or " + cname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(cname + ".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + cname + " or " + cname + ".gz does'nt open")
        finally:
            tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        nion_reg = re.compile(".*NIONS = ", re.IGNORECASE)
        tforce_reg = re.compile(".*TOTAL-FORCE", re.IGNORECASE)
        tvector_reg = re.compile(".*Lattice vectors:", re.IGNORECASE)
        a_reg = re.compile(".*ALAT       =", re.IGNORECASE)
        potcar_reg = re.compile(".*POTCAR:", re.IGNORECASE)
        n_local = 0
        for i in range(num):
            if bool(potcar_reg.match(datlines[i])):
                n_local += 1
            if bool(nion_reg.match(datlines[i])):
                lines = datlines[i].split()
                natom_local = int(lines[11])
            if bool(a_reg.match(datlines[i])):
                tmp = datlines[i].split()
                scale_local = float(tmp[2])
            if bool(tvector_reg.match(datlines[i])):
                t1_local = filter(
                    lambda w: len(w) > 0, re.split('\\s|"|,|\\)|\\(|=', datlines[i + 2])
                )
                t1_x_local = float(t1_local[1]) / scale_local
                t1_y_local = float(t1_local[2]) / scale_local
                t1_z_local = float(t1_local[3]) / scale_local
                t2_local = filter(
                    lambda w: len(w) > 0, re.split('\\s|"|,|\\)|\\(|=', datlines[i + 3])
                )
                t2_x_local = float(t2_local[1]) / scale_local
                t2_y_local = float(t2_local[2]) / scale_local
                t2_z_local = float(t2_local[3]) / scale_local
                t3_local = filter(
                    lambda w: len(w) > 0, re.split('\\s|"|,|\\)|\\(|=', datlines[i + 4])
                )
                t3_x_local = float(t3_local[1]) / scale_local
                t3_y_local = float(t3_local[2]) / scale_local
                t3_z_local = float(t3_local[3]) / scale_local
        if natom != natom_local:
            sys.exit("OUTCAR is inconsistent with POSCAR")
        loop = 0
        for i in range(num):
            if bool(tforce_reg.match(datlines[i])):
                for j in range(natom):
                    tmp = datlines[i + j + 2].split()
                    position_loop[loop, j, 0] = float(tmp[0])
                    position_loop[loop, j, 1] = float(tmp[1])
                    position_loop[loop, j, 2] = float(tmp[2])
                    force_loop[loop, j, 0] = float(tmp[3])
                    force_loop[loop, j, 1] = float(tmp[4])
                    force_loop[loop, j, 2] = float(tmp[5])
                loop += 1
