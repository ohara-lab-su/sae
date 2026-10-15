# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


class ReadMxVps(object):

    def __init__(self, fullname):
        if not os.path.exists(fullname):
            sys.exit(fullname + " file not found")
        try:
            tmp = open(fullname)
            datfile = tmp.read()
        except:
            sys.exit("STOP: " + fullname + " does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    def get_valence_electron(self):
        valence_reg = re.compile("^.*valence.electron.*", re.IGNORECASE)
        for i in range(self.num):
            if bool(valence_reg.match(self.datlines[i])):
                electron = float(self.datlines[i].split()[1])
                break
        return electron
