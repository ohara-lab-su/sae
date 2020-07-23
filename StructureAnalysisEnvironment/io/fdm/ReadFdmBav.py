#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *_bav.txt ファイル
#
###############################################################################
#
# 2020.07.17
#  2016.08.01 以降に sd? のナンバリングルールが変わったのでそれに対する対応
#  - バージョンチェック(ReadFdmBav.py) のための改修
#  - バージョン切り替えのために ReadFdmBav2016()
#  - バージョン切り替えのために ReadFdmBav2020() 切り替え
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.09.11
#  scf ループ関係の情報吸い出しを追加
#
# 2015.06.25
#  R2 bases に対応した cluster: atom positions 吸い出しに対応
#
# 2015.06.23 startup
#
###############################################################################
from __future__ import print_function

try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"

###############################################################################

import sys
# import gzip
import os
import re
import optparse
import numpy as np

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


# import SpaceGroupEnvironment as SGE

###############################################################################


class ReadFdmBav(object):

    def __init__(self, cname, suffix='_bav.txt'):
        """

        :param cname:  入力の bav ファイル(FDMNESの全ログ情報)
        :param suffix:
        """
        self.__datlines, self.__num = SAEnv.read_dataline(cname + suffix)

        fdmnes_ver_reg = re.compile('.*FDMNES.*program,.*')

        # for default
        fdm_version = 2020

        for i in range(self.__num):
            # Version チェック
            if bool(fdmnes_ver_reg.match(self.__datlines[i])):
                print('')
                print("get fdmnes version")
                self.__fdmnes_ver = re.sub('.*,', '', self.__datlines[i]).strip()
                fdm_version = self.__fdmnes_ver.strip('')
                print("version = %s" % fdm_version)
                break

        # FDMNES のバージョン取得
        try:
            year = int(fdm_version.split(' ')[-1])
            print(year)
        except:
            print("*** fail *** get fdmnes version")
            new = True
        else:
            if year > 2016:
                new = True
            else:
                new = False

        if new:
            # 2016.09.01 〜 (動作テストは 2020.06.12-2 version)
            print('load NEW format: sd2020')
            print('')
            self.__bav = SAEnv.ReadFdmBav2020(cname, suffix, datline=self.__datlines, num=self.__num)
        else:
            #  〜2016.01.08
            print('load OLD format: ~sd2016.01.08')
            print('')
            self.__bav = SAEnv.ReadFdmBav2020(cname, suffix, datline=self.__datlines, num=self.__num)

    def set_n_scf_loop(self, _val):
        self.__bav.n_scf_loop = _val

    def get_n_scf_loop(self):
        return self.__bav.n_scf_loop

    n_scf_loop = property(get_n_scf_loop, set_n_scf_loop)

    def get_scf_toten(self):
        return self.__bav.scf_toten

    def set_scf_toten(self, _val):
        self.__bav.scf_toten = _val

    scf_toten = property(get_scf_toten, set_scf_toten)

    #
    # get attribute
    #

    def get_nspin(self):
        return self.__bav.nspin

    def get_natom(self):
        return self.__bav.natom

    def get_ngroup(self):
        return self.__bav.ngroup

    def get_t(self):
        return self.__bav.t

    def get_edge(self):
        return self.__bav.edge

    def get_lmax(self):
        return self.__bav.lmax

    def get_position(self):
        return self.__bav.position

    def get_atoms_index_j(self):
        return self.__bav.atoms_index_j

    def get_fdmnes_ver(self):
        return self.__fdmnes_ver

    @property
    def fdmnes_ver(self):
        return self.__fdmnes_ver

def options():
    #   name = 'POSCAR.txt'
    name = 'Cu'
    suffix = '_bav.txt'

    parser = optparse.OptionParser()
    parser.add_option('-i', '--input', dest='INPUT', )
    options, args = parser.parse_args()

    if not os.path.exists(name + suffix):
        name0 = SAEnv.find_datfile1(suffix)
        name = name0.replace(suffix, '')

    if options.INPUT:
        name = options.INPUT
    if len(args) > 0:
        name = args[0]

    return name, suffix


###############################################################################
if __name__ == '__main__':

    name, suffix = options()
    bav = SAEnv.ReadFdmBav(name, suffix)
    print('')

    natom = bav.get_natom()
    lmax = bav.get_lmax()
    edge = bav.get_edge()
    t = bav.get_t()
    position = bav.get_position()
    atoms_index_j = bav.get_atoms_index_j()

    print("n_ion_loop %s" % str(bav.n_scf_loop))
    for i in range(bav.n_scf_loop):
        print("%s" % str(bav.scf_toten[i]))

    print("natom = %s" % str(natom))
    print("lmax  = %s" % str(lmax))
    print("edge  = %s" % str(edge))
    print("t     = %s" % str(t))

#   for i in range(natom):
#       print "%s %10.6f %10.6f %10.6f" \
#         % (atoms_index_j[i], position[i, 0], position[i, 1], position[i, 2])
#       print position[i][0],position[i][1],position[i][2]
