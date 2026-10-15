#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 3.7
#    DAT_DATA13/VPSファイルを読み込む
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.09 1st
#
################################################################################
################################################################################
# import optparse
# import numpy as np
# import re
# from copy import deepcopy
# import StructureAnalysisEnvironment as SAE
# import SpaceGroupEnvironment as SGE
################################################################################
#
#   data = '../DFT_DATA13'
#   atom = 'C'
#   pot  = 'PBE'
#   ver  = '13'
#   name = 'C_PBE13'
#
################################################################################
################################################################################
#   opts = data, atom, pot, ver, name
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


#   def __init__(self,opts):
# valence.electron を返す
class ReadMxVps(object):

    #       data,\
    #       atom,\
    #       pot,\
    #       ver,\
    #       name = opts
    #       fullname = data+'/VPS/'+name+'.vps'
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
