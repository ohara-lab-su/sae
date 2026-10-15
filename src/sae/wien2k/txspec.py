# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class ReadWienTxspec(object):

    def __init__(self, case="case", spin=None, suffix=".txspec"):
        from sae.common.text import TextFiles

        if spin is None:
            spin = ""
        self.datlines, self.num = TextFiles().read_dataline(case + suffix + spin)
        s_reg = re.compile(" #S=.*")
        g_reg = re.compile(" #GAMMA=.*")
        self.eng = []
        self.unbroad_xas = []
        for i in range(self.num):
            line = self.datlines[i]
            if not bool(s_reg.match(line)) and (not bool(g_reg.match(line))):
                self.eng.append(float(line.split()[0]))
                self.unbroad_xas.append(float(line.split()[1]))

    def get_eng(self):
        self.eng = np.array(self.eng)
        return self.eng

    def get_emin(self):
        self.emin = min(self.eng)
        return self.emin

    def get_emax(self):
        self.emax = max(self.eng)
        return self.emax

    def get_unbroad_xas(self):
        self.unbroad_xas = np.array(self.unbroad_xas)
        return self.unbroad_xas

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
