# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import gzip


class ReadVaspSymdat(object):

    def __init__(self, name):
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + name + " or " + name + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1

    def get_symlines(self):
        self.symlines = []
        for i in range(self.num):
            self.symlines.append(self.datlines[i])
        return self.symlines

    def get_num_symlines(self):
        return self.num
