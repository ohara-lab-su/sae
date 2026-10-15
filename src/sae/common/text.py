# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import re
import sys
import os
from numpy import *
from copy import deepcopy

comment_reg = re.compile("^#.*", re.IGNORECASE)
import gzip

comment_reg = re.compile("^#.*", re.IGNORECASE)


class TextFiles:

    def del_comment(self, data, comment="!"):
        newdata = []
        for i in range(len(data)):
            newdata.append(re.sub(comment + ".*", "", data[i]))
        num = len(newdata)
        return (newdata, num)

    def read_dat(self, name, dimension, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            for k in range(dimension):
                dat[i, k] = tmp[k]
            j += 1
        nlist = j
        return nlist

    def read_dat2(self, name, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            dat[i, 0] = tmp[0]
            dat[i, 1] = tmp[1]
            j += 1
        nlist = j
        return nlist

    def read_dat5(self, name, dat, cut):
        if not os.path.exists(name):
            sys.exit("STOP(read_dat.py): " + name + " not found")
        try:
            tmp = open(name)
        except:
            sys.exit("STOP(read_dat.py): " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist = int(len(datalines)) - 1
        j = 0
        for i in range(cut, nlist):
            tmp = datalines[i].split()
            dat[i, 0] = tmp[0]
            dat[i, 1] = tmp[1]
            dat[i, 2] = tmp[2]
            dat[i, 3] = tmp[3]
            dat[i, 4] = tmp[4]
            j += 1
        nlist = j
        return nlist

    def read_dataline(self, name):
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit(
                "STOP(read_dataline): " + name + " or " + name + ".gz file not found"
            )
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
            if isinstance(datfile, bytes):
                datfile = datfile.decode("ascii")
        except:
            tmp.close()
            sys.exit("STOP: " + name + " or " + name + ".gz does'nt open")
        finally:
            tmp.close()
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        return (datlines, num)

    def read_dataline1(self, name):
        import re

        comment0_reg = re.compile("^#.*", re.IGNORECASE)
        comment1_reg = re.compile("^!.*", re.IGNORECASE)
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit(
                "STOP(read_dataline): " + name + " or " + name + ".gz file not found"
            )
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
        datalines0 = datfile.split("\n")
        num0 = len(datalines0) - 1
        j = 0
        datalines = []
        for i in range(num0):
            if not bool(comment0_reg.match(datalines0[i])):
                if not bool(comment1_reg.match(datalines0[i])):
                    datalines.append(datalines0[i])
                    j += 1
        num = j
        return (datalines, num)

    def read_list1(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                find_list[j] = tmp[0]
                j += 1
        nlist = j
        return nlist

    def read_list3(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        tmp = open(name)
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                if not int(len(tmp)) >= 3:
                    sys.exit(name + " Format Error: datalines < 3 ")
                find_list[j, 0] = tmp[0]
                find_list[j, 1] = tmp[1]
                find_list[j, 2] = tmp[2]
                j += 1
        nlist = j
        return nlist

    def read_list4(self, name, find_list):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        tmp = open(name)
        datalist = tmp.read()
        tmp.close
        datalines = datalist.split("\n")
        nlist0 = int(len(datalines)) - 1
        j = 0
        for i in range(nlist0):
            if not bool(comment_reg.match(datalines[i])):
                tmp = datalines[i].split()
                if not int(len(tmp)) >= 4:
                    sys.exit(name + " Format Error: datalines < 4 ")
                find_list[j, 0] = tmp[0]
                find_list[j, 1] = tmp[1]
                find_list[j, 2] = tmp[2]
                find_list[j, 3] = tmp[3]
                j += 1
        nlist = j
        return nlist

    def read_list_param(self, name):
        if not os.path.exists(name):
            sys.exit(name + " not found")
        try:
            tmp = open(name)
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        datalist = tmp.read()
        tmp.close()
        datlines = datalist.split("\n")
        nlist = int(len(datlines)) - 1
        return nlist

    def read_row(self, name, column=0):
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
        datlines = datfile.split("\n")
        num = len(datlines) - 1
        row = len(datlines[column].split())
        return (row, num)
