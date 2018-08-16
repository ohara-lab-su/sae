#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# MXdosall.py
#  sh 版の MXdosall とほぼ同じ
#  おそらく無駄に複雑に書いている
#  一部追加機能有り
#
################################################################################
#
# 2015.02.26
#  startup
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
#import os
#import re
#import dircache
import optparse
#import numpy as np
#import glob

import shlex
import subprocess

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  


###############################################################################
def run(command, input=None):

    try:
        proc = subprocess.Popen(
            shlex.split(command),
            stdin  = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
        )

        if input:
            proc.stdin.write(input)

        proc.stdin.close()
        result = proc.stdout.read()  # 結果の標準出力
        ret    = proc.wait()         # エラーコード
        return ret, result

    except OSError, (e):
      return (e.errno, e.args[1])

###############################################################################
# suffix1 と suffix2 の両方で find_datfile が成功した時に datname を返す
#
def check_datname(suffix1,suffix2):

    try:
        datname1 = SAE.find_datfile(suffix1)
        try:
            datname2= SAE.find_datfile(suffix2)
            if datname1 == datname2:
               datname = datname1
        except:
            sys.exit("STOP: ."+suffix1+" and ."+suffix2+"file not found")
    except:
        sys.exit("STOP: ."+suffix1+" file not found")
    
    return datname

###############################################################################

#       cmd = 'ls -ls'
#       proc = subprocess.Popen(shlex.split(cmd),\
#               stderr=subprocess.PIPE,\
#               stdout=subprocess.PIPE)
#       res = proc.communicate()
#       print res[0]


###############################################################################
if __name__ == '__main__':

    #### ProgramName ====
    dosmain = 'DosMain'
    suffix1 = 'Dos.val'
    suffix2 = 'Dos.vec'
    datname = check_datname(suffix1,suffix2)  # datname のデフォルト値作成
    if datname:
        print datname

    parser = optparse.OptionParser()
    parser.add_option( '-i','--input',dest='INPUT',)
    options,args = parser.parse_args()

    # オプション指定があったらデフォルト値を上書き
    if options.INPUT:
        datname=options.INPUT

    # 引数で名前指定があったらデフォルト値を上書き
    if len(args) > 0:
        datname=args[0]

    # デフォルト値が存在したら
    if datname:
        command=dosmain+' '+datname+'.'+suffix1+' '+datname+'.'+suffix2
        print command

        ## 標準入力を受けて実行
        inline='1 1'
        ret, result = run(command,inline)
        if ret:
            print '------'
            print result


        ## 直ぐに実行
        print '------'
        proc = subprocess.Popen(\
                shlex.split(command),\
               #stdin=subprocess.PIPE,\
               #stdout=subprocess.PIPE,\
               #stderr = subprocess.PIPE,
               )
        proc.communicate()

#       print proc.poll()
       #proc.stdin.write(inline)
#       proc.stdin.close()
#       print proc.stdout.read()
#       os.read(p.stdout.fileno(), 1024)
     
################################################################################
