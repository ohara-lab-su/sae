# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


class ReadMxVpsList(object):

    def __init__(self, name):
        if not os.path.exists(name):
            sys.exit("STOP: " + name + " not found")
        try:
            tmp = open(name)
            datalist = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        finally:
            tmp.close()
        self.datalines = datalist.split("\n")
        self.nlist0 = int(len(self.datalines)) - 1

    def get_list(self):
        comment_reg = re.compile("^#.*", re.IGNORECASE)
        self.list_data = []
        j = 0
        for i in range(self.nlist0):
            if not bool(comment_reg.match(self.datalines[i])):
                tmp = self.datalines[i].split()
                if not int(len(tmp)) >= 4:
                    sys.exit(self.name + " Format Error: datalines < 4 ")
                self.list_data.append([tmp[0], tmp[1], tmp[2], tmp[3]])
                j += 1
        self.nlist = j
        return [self.nlist, self.list_data]

    def get_vps_name(self, atom):
        nlist, list_data = self.get_list()
        for i in range(nlist):
            if list_data[i][1] == atom:
                num = list_data[i][0]
                symbol = list_data[i][1]
                cutoff = list_data[i][2]
                vps_orbit = list_data[i][3]
                break
        return [num, symbol, cutoff, vps_orbit]
