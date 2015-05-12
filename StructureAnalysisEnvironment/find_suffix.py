#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# find_suffix(name)
#
# 基本仕様
#    find_datfile.py の逆
#    特定のファイル名を引いたら suffix いろいろを探してくれる
#
#    >ls case.dos*
#    case.dos1
#    case.dos2
#      .
#      .
#    find_datfile() と異なり、こちらは最初から複数ファイルが前提
#
# find_suffix1(name)              # ls name*
# find_suffix2(head,tail)         # ls head*tail
# find_suffix3(head,tail,delete)  # ls head* | sed 's/delete//'
#                                 # tail が None のときは tail を delete として動作
#
################################################################################
#
# 2015.03.27
#  spin + ev のときに suffix3 が正しく動いていないバグを修正
#
# 2015.03.25
#  tail が None のときの処理を追加
#
# 2015.03.24
#   startup
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.6"
################################################################################

#import sys
#import os
#import gzip

import re
import glob
import optparse

################################################################################
# ls name*
#
def find_suffix1(name):
    files = glob.glob(str(name)+"*")
    return files

################################################################################
# ls head*tail
#
def find_suffix2(head,tail):
    filelist = glob.glob(str(head)+"*"+str(tail))
    return filelist

################################################################################
# ls head* | sed 's/tail//'
#
def find_suffix3(head='case',tail='ev',delete='ev'):
    if not tail == 'None':
        filelist = glob.glob(str(head)+"*"+str(tail)+"*")
    else:
        files = glob.glob(str(head)+"*")
        filelist = []
        for i in files:
            filelist.append(re.sub(delete,'',i))

        filelist = sorted(set(filelist), key=filelist.index)

    return filelist


################################################################################
if __name__ == '__main__':

    name = 'Cu.dos'
    tail = 'ev'
#   tail = 'None'
    parser = optparse.OptionParser()
    parser.add_option( '-n','--name',)
    options, args = parser.parse_args()

    if len(args) >0:
        name = args[0]

    if options.name:
        name = options.name

    try:
        files = find_suffix1(name)
        print "name",files
        files = find_suffix2(name,tail)
        print "name,tail",files
        files = find_suffix3(name,'None')
        print "name,None",files
        files = find_suffix3(name,'None','ev')
        print "name,None",files
    except:
        pass

