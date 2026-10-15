# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.openmx.dos_methods import ReadMxDosMethod
import sys
import os
import gzip
import optparse
import numpy as np

try:
    ReadMxDosMethod = ReadMxDosMethod
except ImportError:
    ReadMxDosMethod = ReadMxDosMethod


class ReadMxTdos(ReadMxDosMethod):

    def __init__(self, name, suffix):
        dosname = name + suffix
        if os.path.exists(dosname):
            GZIP = False
        elif os.path.exists(dosname + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + dosname + " or " + dosname + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(dosname + ".gz")
            else:
                tmp = open(dosname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + dosname + " or " + dosname + ".gz does'nt open")
        finally:
            tmp.close()
        self.suffix = suffix
        self.name = name
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    def get_tdos(self, spin=0):
        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()
        dos = np.zeros((NEDOS, NSPIN))
        for i in range(NEDOS):
            if NSPIN >= 2:
                dos[i, 0] = float(self.datlines[i].split()[1])
                dos[i, 1] = float(self.datlines[i].split()[2])
            else:
                dos[i, 0] = float(self.datlines[i].split()[1])
        self.TDOS = np.abs(dos[:, spin])
        return self.TDOS

    def get_inttdos(self, spin=0):
        NSPIN = self.get_ispin()
        NEDOS = self.get_nedos()
        intdos = np.zeros((NEDOS, NSPIN))
        for i in range(NEDOS):
            if NSPIN >= 2:
                intdos[i, 0] = float(self.datlines[i].split()[3])
                intdos[i, 1] = float(self.datlines[i].split()[4])
            else:
                intdos[i, 0] = float(self.datlines[i].split()[2])
        self.INTTDOS = intdos[:, spin]
        return self.INTTDOS
