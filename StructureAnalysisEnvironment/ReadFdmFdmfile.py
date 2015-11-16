#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *.txt ãƒ•ã‚¡ã‚¤ãƒ«
#
###############################################################################
#
# 2015.11.12 startup
#
###############################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"
###############################################################################

#import sys
#import gzip
#import os
import re
#import optparse
#import numpy as np

import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmFdmfile(object):

    def __init__(self, cname='fdmfile', suffix='.txt'):

        name = cname+suffix

        self.datlines, self.num = SAEnv.read_dataline1(name)

        # •¡”“ü—Íƒtƒ@ƒCƒ‹‚Ìê‡‚Í–¢‘Î‰(None‚ğ•Ô‚·)
        #
        for i in range(self.num):
            if len(self.datlines[i].split()):
                _line = self.datlines[i].split()[0]

                if bool(re.compile(r'^[0-9]').match(_line)):
                    if _line == '1':
                        self.filout = self.datlines[i+1].split()[0]
                    else:
                        self.filout = None
                    break

    def get_filout(self):
        return self.filout

###############################################################################
if __name__ == '__main__':

    conv = ReadFdmFdmfile()
    print conv.filout

