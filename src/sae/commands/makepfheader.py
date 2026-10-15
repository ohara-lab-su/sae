#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import codecs
import optparse
import ReadPfformat as pf


#!/usr/bin/env python
# -*- coding: utf-8 -*-                                                                   
################################################################################
# K.NAKADA, kengo.nakada@gmail.com  
#
################################################################################
################################################################################
#import PFformat as pf
#import re
################################################################################
## default
def options():
    DAT = "Cu-foil_10ms.dat"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=DAT)
    parser.add_option("-d", "--dat", dest="DATFILE", default=DAT)
    options, args = parser.parse_args()
    if options.INPUT:
        DAT = options.INPUT
    if options.DATFILE:
        DAT = options.DATFILE
    if len(args) > 0:
        DAT = args[0]
    if not os.path.exists(DAT):
        sys.exit(DAT + " file not found")
    return DAT


################################################################################
#   STD = False
#   a.head()
#   a.write()                                                                             
#   a.write(logfile)                                                                             
if __name__ == "__main__":
    DAT = options()
    base, ext = os.path.splitext(DAT)
    outfile = base + ".README"
    logfile = base + ".log"
    STD = True
    if STD:
        out = sys.stdout
    else:
        #           out = codecs.open(outfile,'a','utf-8')                                    
        try:
            out = codecs.open(outfile, "w", "utf-8")
        except:
            sys.exit("STOP:" + outfile + " can'nt open")
    (print >> out, "PFformat (9809) ファイル名      :", DAT)
    if os.path.exists(base + ".txt"):
        (print >> out, "Athena/Artemis Format ファイル名:", base + ".txt")
    if os.path.exists(base + ".ex3"):
        (print >> out, "REX2000 Format ファイル名       :", base + ".ex3")
    (print >> out, "")
    dat = pf.ReadPfformat(DAT)
    if STD:
        dat.write_head()
    else:
        dat.write_head(outfile)
    del dat
