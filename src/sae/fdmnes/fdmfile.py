# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


class ReadFdmFdmfile(object):

    def __init__(self, cname="fdmfile", suffix=".txt"):
        from sae.common.text import TextFiles

        name = cname + suffix
        self.datlines, self.num = TextFiles().read_dataline1(name)
        for i in range(self.num):
            if len(self.datlines[i].split()):
                _line = self.datlines[i].split()[0]
                if bool(re.compile("^[0-9]").match(_line)):
                    if _line == "1":
                        self.filout = self.datlines[i + 1].split()[0]
                    else:
                        self.filout = None
                    break

    def get_filout(self):
        return self.filout
