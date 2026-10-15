# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


class ReadWienOutputt(object):

    def __init__(self, name):
        from sae.common.text import TextFiles

        self.datlines, self.num = TextFiles().read_dataline(name)
        jatom_txt = ".*JATOM"
        jatom_reg = re.compile(jatom_txt)
        self.isplits = []
        for i in range(self.num):
            if bool(jatom_reg.match(self.datlines[i])):
                jatom = re.sub(jatom_txt, "", self.datlines[i])
                jatom = int(re.sub(" *MULT=.*$", "", jatom))
                isplit = re.sub(".*ISPLIT=", "", self.datlines[i]).split()[1].split(",")
                self.isplits.append(isplit)
        self.nion = jatom

    def get_nion(self):
        return self.nion

    def get_wien_orbital(self):
        return self.isplits
