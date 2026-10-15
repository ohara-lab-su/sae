# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadWienXspec(object):

    def __init__(self, case="case", spin=None, suffix=".xspec"):
        from sae.common.text import TextFiles

        if spin is None:
            spin = ""
        if not os.path.exists(case + suffix):
            case = case.replace(suffix, "")
        self.datlines, self.num = TextFiles().read_dataline(case + suffix + spin)
        self.head = []
        self.head.append(self.datlines[0])
        self.head.append(self.datlines[1])
        s_reg = re.compile(" #S=.*")
        g_reg = re.compile(" #GAMMA=.*")
        self.eng = []
        self.xas = []
        self.s = 0.0
        self.g = 0.0
        for i in range(self.num):
            line = self.datlines[i]
            if bool(s_reg.match(line)):
                self.s = float(line.split()[1])
            if bool(g_reg.match(line)):
                self.g = float(line.split()[1])
            if not bool(s_reg.match(line)) and (not bool(g_reg.match(line))):
                self.eng.append(float(line.split()[0]))
                self.xas.append(float(line.split()[1]))
        self.eng = np.array(list(self.eng))
        self.xas = np.array(list(self.xas))
        self.gamma = self.g
        self.ymax_xas = max(self.xas)
        self.xasmax = self.ymax_xas
        self.emax = max(self.eng)
        self.emin = min(self.eng)

    def get_head(self):
        return self.head

    def get_eng(self):
        return self.eng

    def get_xas(self):
        return self.xas

    def get_ymax_xas(self):
        return self.ymax_xas

    def get_emin(self):
        return self.emin

    def get_emax(self):
        return self.emax

    def get_s(self):
        return self.s

    def get_gamma(self):
        return self.g

    def write(self, outputname=None):
        if outputname is None:
            out = sys.stdout
        else:
            try:
                out = open(outputname, "w")
            except:
                out.close()
                sys.exit(outputname + " can't not open")
        nxas = len(self.xas)
        for i in range(nxas):
            print("%9.5f %14.8f" % (self.eng[i], self.xas[i]), file=out)
        if not outputname is None:
            out.close()
