# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import re
import glob
import optparse


class FileDiscovery:

    def find_datfile(self, suffix):
        suffix0 = re.sub("^\\.", "", suffix)
        filelist = glob.glob("*." + suffix0)
        datname = None
        if len(filelist) == 1:
            datname = re.sub("." + suffix0, "", filelist[0])
        return datname

    def find_datfile1(self, tail):
        filelist = glob.glob("*" + tail)
        datname = None
        if len(filelist) == 1:
            datname = filelist[0]
        return datname

    def find_datfiles(self, suffix):
        filelist = glob.glob("*." + str(suffix))
        datnames = None
        datnames = []
        for i in filelist:
            datnames.append(re.sub("." + str(suffix), "", i))
        return datnames

    def find_suffix1(self, name):
        files = glob.glob(str(name) + "*")
        return files

    def find_suffix2(self, head, tail):
        filelist = glob.glob(str(head) + "*" + str(tail))
        return filelist

    def find_suffix3(self, head="case", tail="ev", delete="ev"):
        if not tail == "None":
            filelist = glob.glob(str(head) + "*" + str(tail) + "*")
        else:
            files = glob.glob(str(head) + "*")
            filelist = []
            for i in files:
                filelist.append(re.sub(delete, "", i))
            filelist = sorted(set(filelist), key=filelist.index)
        return filelist
