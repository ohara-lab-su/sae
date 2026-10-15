#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
#       print proc.poll()
#proc.stdin.write(inline)
#       proc.stdin.close()
#       print proc.stdout.read()
#       os.read(p.stdout.fileno(), 1024)
################################################################################
from __future__ import print_function

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
# 2018.08.23
#  Python2/3 両対応 (runはpython3のみかもしれん)
#
# 2015.02.26
#  startup
#
################################################################################
################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import optparse
import shlex
import subprocess


#
################################################################################
#import os
#import re
#import dircache
#import numpy as np
#import glob
#import re
#from copy import deepcopy
#import SpaceGroupEnvironment as SGE  
###############################################################################
def run(command, input=None):
    # for Python2.7
    #   except OSError, (e):
    #       return (e.errno, e.args[1])
    # for Python3
    try:
        proc = subprocess.Popen(
            shlex.split(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if input:
            proc.stdin.write(input)
        proc.stdin.close()
        # 結果の標準出力
        result = proc.stdout.read()
        # エラーコード
        ret = proc.wait()
        return (ret, result)
    except OSError as e:
        return (e.errno, e.args[1])


###############################################################################
# suffix1 と suffix2 の両方で find_datfile が成功した時に datname を返す
#
def check_datname(suffix1, suffix2):
    from sae.common.paths import FileDiscovery

    try:
        datname1 = FileDiscovery().find_datfile(suffix1)
        try:
            datname2 = FileDiscovery().find_datfile(suffix2)
            if datname1 == datname2:
                datname = datname1
        except:
            sys.exit("STOP: ." + suffix1 + " and ." + suffix2 + "file not found")
    except:
        sys.exit("STOP: ." + suffix1 + " file not found")
    return datname


###############################################################################
#       cmd = 'ls -ls'
#       proc = subprocess.Popen(shlex.split(cmd),\
#               stderr=subprocess.PIPE,\
#               stdout=subprocess.PIPE)
#       res = proc.communicate()
#       print res[0]
###############################################################################
#### ProgramName ====
# オプション指定があったらデフォルト値を上書き
# 引数で名前指定があったらデフォルト値を上書き
# デフォルト値が存在したら
if __name__ == "__main__":
    dosmain = "DosMain"
    suffix1 = "Dos.val"
    suffix2 = "Dos.vec"
    # datname のデフォルト値作成
    datname = check_datname(suffix1, suffix2)
    if datname:
        print(datname)
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT")
    options, args = parser.parse_args()
    if options.INPUT:
        datname = options.INPUT
    if len(args) > 0:
        datname = args[0]
    ## 標準入力を受けて実行
    ## 直ぐに実行
    if datname:
        command = (
            dosmain + " " + datname + "." + suffix1 + " " + datname + "." + suffix2
        )
        print(command)
        inline = "1 1"
        ret, result = run(command, inline)
        if ret:
            print("------")
            print(result)
        print("------")
        #stdin=subprocess.PIPE,\
        #stdout=subprocess.PIPE,\
        #stderr = subprocess.PIPE,
        proc = subprocess.Popen(shlex.split(command))
        proc.communicate()
