#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vtemp.py
#
#   OUTCAR から temperature と ETOTAL を吸い出す
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.24
#  method名ルール変更に伴い get_iter_num() --> get_n_ion_loop()
#
# 2015.02.16
#  バグ
#  get_tmod() ===> get_md_mode() へ修正した方針を忘れていたので修正しなおした
#
# 2015.01.26 1st run
#   OUTCAR と OSZICAR の両方があったら OSZICAR を読み込むようにする
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.3"
################################################################################

import sys
import os
#import re
#import optparse

#import numpy as np

#from pylab import *
#import matplotlib.pyplot as plt

#from LIB_vasp.read_dat import *

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE 


################################################################################
if __name__ == '__main__':

    name_out = 'OUTCAR'
    name_osz = 'OSZICAR'

    module_name = 'StructureAnalysisEnvironment'

    if os.path.exists(name_osz) or os.path.exists(name_osz+".gz"):
        class_name ='ReadOszicar'
        name = name_osz
    else:
        class_name = 'ReadOutcar'
        name = name_out

    module = __import__(module_name, globals(), locals(), [class_name], -1)
    klass = getattr(module,class_name)

    outfile = klass(name)
#   t_FLAG = outfile.get_tmode()
    t_FLAG = outfile.get_md_mode()

    if not t_FLAG:
        sys.exit("STOP: current is non MD mode")

    temperature = outfile.get_temperature()
    etotal = outfile.get_etotal()

    n_ion_loop = outfile.get_n_ion_loop()
    for i in range(n_ion_loop):
        print "%5d %6.2f  %15.8f" % (i+1, temperature[i], etotal[i])

################################################################################
