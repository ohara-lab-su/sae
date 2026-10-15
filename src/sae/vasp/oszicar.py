# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import gzip
import os
import re
import numpy as np


class ReadVaspOszicar(object):

    def __init__(self, cname):
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
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    def get_n_ion_loop(self):
        iter_reg = re.compile(".*F=", re.IGNORECASE)
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.n_ion_loop = int(tmp[0])
        return self.n_ion_loop

    def get_md_mode(self):
        iter_reg = re.compile(".*T=")
        self.md_FLAG = False
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                self.md_FLAG = True
                break
        return self.md_FLAG

    def get_temperature(self):
        MD_FLAG = self.get_md_mode()
        if MD_FLAG:
            n_ion_loop = self.get_n_ion_loop()
            self.temperature = np.zeros(n_ion_loop)
            iter_reg = re.compile(".*T=", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(iter_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.temperature[j] = float(tmp[2])
                    j += 1
        return self.temperature

    def get_etotal(self):
        MD_FLAG = self.get_md_mode()
        if MD_FLAG:
            n_ion_loop = self.get_n_ion_loop()
            self.ETOTAL = np.zeros(n_ion_loop)
            iter_reg = re.compile(".*E=", re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(iter_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.ETOTAL[j] = float(tmp[4])
                    j += 1
        return self.ETOTAL
