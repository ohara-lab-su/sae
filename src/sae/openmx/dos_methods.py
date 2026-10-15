# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import numpy as np


class ReadMxDosMethod(object):

    def get_ispin(self):
        module_name = "sae._class_registry"
        if os.path.exists(self.name + ".out") or os.path.exists(
            self.name + ".out" + ".gz"
        ):
            class_name = "ReadMxOut"
            datname = self.name + ".out"
        elif os.path.exists(self.name + ".dat") or os.path.exists(
            self.name + ".dat" + ".gz"
        ):
            class_name = "ReadMxDat"
            datname = self.name + ".dat"
        else:
            sys.exit(
                "STOP: " + self.name + ".out or " + self.name + ".dat file not found"
            )
        module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        dat = klass(datname)
        self.ispin = dat.get_ispin()
        return self.ispin

    def get_natom(self):
        module_name = "sae._class_registry"
        if os.path.exists(self.name + ".out") or os.path.exists(
            self.name + ".out" + ".gz"
        ):
            class_name = "ReadMxOut"
            datname = self.name + ".out"
        elif os.path.exists(self.name + ".dat") or os.path.exists(
            self.name + ".dat" + ".gz"
        ):
            class_name = "ReadMxDat"
            datname = self.name + ".dat"
        else:
            sys.exit(
                "STOP: " + self.name + ".out or " + self.name + ".dat file not found"
            )
        module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        dat = klass(datname)
        self.natom = dat.get_natom()
        return self.natom

    def get_title(self):
        module_name = "sae._class_registry"
        if os.path.exists(self.name + ".out") or os.path.exists(
            self.name + ".out" + ".gz"
        ):
            class_name = "ReadMxOut"
            datname = self.name + ".out"
        elif os.path.exists(self.name + ".dat") or os.path.exists(
            self.name + ".dat" + ".gz"
        ):
            class_name = "ReadMxDat"
            datname = self.name + ".dat"
        else:
            sys.exit(
                "STOP: " + self.name + ".out or " + self.name + ".dat file not found"
            )
        module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        dat = klass(datname)
        self.title = dat.get_title()
        return self.title

    def get_emax(self):
        NEDOS = self.get_nedos()
        self.EMAX = float(self.datlines[NEDOS - 1].split()[0])
        return self.EMAX

    def get_emin(self):
        self.EMIN = float(self.datlines[0].split()[0])
        return self.EMIN

    def get_nedos(self):
        return self.num

    def get_efermi(self):
        pass

    def get_lorbit(self):
        pass

    def get_eng(self):
        NEDOS = self.get_nedos()
        eng = np.zeros(NEDOS)
        for i in range(NEDOS):
            eng[i] = float(self.datlines[i].split()[0])
        self.ENG = eng[:]
        return self.ENG

    def get_nion(self):
        module_name = "sae._class_registry"
        if os.path.exists(self.name + ".out") or os.path.exists(
            self.name + ".out" + ".gz"
        ):
            class_name = "ReadMxOut"
            datname = self.name + ".out"
        elif os.path.exists(self.name + ".dat") or os.path.exists(
            self.name + ".dat" + ".gz"
        ):
            class_name = "ReadMxDat"
            datname = self.name + ".dat"
        else:
            sys.exit(
                "STOP: " + self.name + ".out or " + self.name + ".dat file not found"
            )
        module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        dat = klass(datname)
        self.NION = dat.get_nion()
        return self.NION

    def get_atoms_j(self):
        module_name = "sae._class_registry"
        if os.path.exists(self.name + ".out") or os.path.exists(
            self.name + ".out" + ".gz"
        ):
            class_name = "ReadMxOut"
            datname = self.name + ".out"
        elif os.path.exists(self.name + ".dat") or os.path.exists(
            self.name + ".dat" + ".gz"
        ):
            class_name = "ReadMxDat"
            datname = self.name + ".dat"
        else:
            sys.exit(
                "STOP: " + self.name + ".out or " + self.name + ".dat file not found"
            )
        module = __import__(module_name, globals(), locals(), [class_name], 0)
        klass = getattr(module, class_name)
        dat = klass(datname)
        self.atoms_j = dat.get_atoms_j()
        return self.atoms_j
