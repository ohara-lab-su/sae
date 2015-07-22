#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# del_commentout()
# コメントアウト削除ルーチン
#
################################################################################
#
# 2015.06.19 1st
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

#import sys
#import os
import re
#from numpy import *
#from copy import deepcopy

def del_comment(data,comment='!'):

    newdata = []
    for i in range(len(data)):
        newdata.append(re.sub(comment+'.*','',data[i]))

    num = len(newdata)

    return newdata,num
