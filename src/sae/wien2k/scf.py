#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.scf
#  エナジーパラメーターのチェックなどのために、*.scf 情報を抜き出すためのclass
#
#  *.scf ファイルは *.output0 *.output1 などの情報から重要なものを抽出したもの
#  --> WIEN2k の実行スクリプトで作られる
#
#  注意)
#    scf1 ファイルは ITERATION 情報がないのでこのクラスは使えない
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.06.30
#   == None --> is None
#
# 2015.03.30
#  startup
#
################################################################################
################################################################################
# import gzip
# import numpy as np
# import optparse
# sys.path.append('../..')
# import SpaceGroupEnvironment as SGE
################################################################################
################################################################################
# case = 'Cu'
#   scf.write_epar(ion=0,par=1)
#   scf.write_epar(l=1)
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re


############################################################################
## init
############################################################################
# print EPL
############################################################################
# print EPH
############################################################################
# print E_parameter
class ReadWienScf(object):

    def __init__(self, case="case", suffix="scf"):
        from sae.common.text import TextFiles

        suffix = "." + str(suffix)
        self.datlines, self.num = TextFiles().read_dataline(case + suffix)
        ite_reg = re.compile(".*:ITE.*:.*")
        parm_reg = re.compile(".*ATOMIC SPHERE DEPENDENT PARAMETERS.*")
        ldel_reg = re.compile(":E.*_.*:")
        rkm_reg = re.compile(":RKM.*")
        epl_reg = re.compile(":EPL.*")
        eph_reg = re.compile(":EPH.*")
        i = 0
        nscf = 0
        EPAR_ITER = []
        EPL_ITER = []
        EPH_ITER = []
        SITE = []
        # ITER 毎の区切りチェック
        while i < self.num:
            if bool(ite_reg.match(self.datlines[i])):
                E_ATOM = []
                EPL_ATOM = []
                EPH_ATOM = []
                nion = 0
                # ATOMIC SPHEARE DEPENDENT PARAMETERS のチェック
                while i < self.num:
                    if bool(parm_reg.match(self.datlines[i])):
                        SITE.append(self.datlines[i].split()[6])
                        E = []
                        i += 1
                        while i < self.num:
                            if bool(ldel_reg.match(self.datlines[i])):
                                E.append(self.datlines[i])
                            if bool(parm_reg.match(self.datlines[i])):
                                SITE.append(self.datlines[i].split()[6])
                                E_ATOM.append(E)
                                E = []
                                nion += 1
                            if bool(rkm_reg.match(self.datlines[i])):
                                E_ATOM.append(E)
                                E = []
                                nion += 1
                                break
                            i += 1
                    if bool(epl_reg.match(self.datlines[i])):
                        EPL_ATOM.append(re.sub(":EPL\\d+:", "", self.datlines[i]))
                    if bool(eph_reg.match(self.datlines[i])):
                        EPH_ATOM.append(re.sub(":EPH\\d+:", "", self.datlines[i]))
                    if bool(ite_reg.match(self.datlines[i + 1])):
                        EPAR_ITER.append(E_ATOM)
                        EPL_ITER.append(EPL_ATOM)
                        EPH_ITER.append(EPH_ATOM)
                        break
                    i += 1
                nscf += 1
            i += 1
        EPL_ITER.append(EPL_ATOM)
        EPH_ITER.append(EPH_ATOM)
        EPAR_ITER.append(E_ATOM)
        SITE_ITER = []
        for atom in range(0, len(SITE), nion):
            SITE_ITER.append(SITE[atom : atom + nion])
        self.nscf = nscf
        self.nion = nion
        self.site_iter = SITE_ITER
        self.epar_iter = EPAR_ITER
        self.epl_iter = EPL_ITER
        self.eph_iter = EPH_ITER

    def write_epl(self, ion=None):
        print(
            "         Q-s-low  E-s-low  Q-p-low  E-p-low  Q-d-low  E-d-low  Q-f-low  E-f-low"
        )
        if ion is None:
            for it in range(self.nscf):
                print("======== ITER %s" % str(it))
                # print "ion=",ion,"",self.epl_iter[it][ion]
                for ion in range(self.nion):
                    print("ion= %s %s" % (str(ion), str(self.epl_iter[it][ion])))
        else:
            ion = int(ion)
            # print "it=",it,"",self.epl_iter[it][ion]
            for it in range(self.nscf):
                print("it= %s %s" % (str(it), str(self.epl_iter[it][ion])))

    def write_eph(self, ion=None):
        print(
            "         Q-s-hi   E-s-hi   Q-p-hi   E-p-hi   Q-d-hi   E-d-hi   Q-f-hi   E-f-hi"
        )
        if ion is None:
            for it in range(self.nscf):
                print("======== ITER %s" % str(it))
                # print "ion=",ion,"",self.eph_iter[it][ion]
                for ion in range(self.nion):
                    print("ion= %s %s" % (str(ion), str(self.eph_iter[it][ion])))
        else:
            ion = int(ion)
            # print "it=",it,"",self.eph_iter[it][ion]
            for it in range(self.nscf):
                print("it= %s %s" % (str(it), str(self.eph_iter[it][ion])))

    def write_epar(self, ion=None, par=None, l=None):
        if ion is None and par is None and (l is None):
            for it in range(self.nscf):
                print("======== ITER %s" % str(it))
                for ion in range(self.nion):
                    # print self.site_iter[it][ion],self.epar_iter[it][ion][par]
                    for par in range(len(self.epar_iter[it][ion])):
                        print(self.site_iter[it][ion], self.epar_iter[it][ion][par])
        elif ion is not None and par is None and (l is None):
            ion = int(ion)
            for it in range(self.nscf):
                print("======== ITER %s" % str(it))
                # print "ion=",ion,"",\
                #        self.site_iter[it][ion],self.epar_iter[it][ion][par]
                for par in range(len(self.epar_iter[it][ion])):
                    print(
                        "ion= %s %s %s"
                        % (
                            str(ion),
                            str(self.site_iter[it][ion]),
                            str(self.epar_iter[it][ion][par]),
                        )
                    )
        elif ion is None and par is not None and (l is None):
            par = int(par)
            for it in range(self.nscf):
                print("======== ITER %s" % str(it))
                # print "ion=",ion,"orbit=",par,"",\
                #        self.site_iter[it][ion],self.epar_iter[it][ion][par]
                for ion in range(self.nion):
                    print(
                        "ion= %s orbit=%s %s %s"
                        % (
                            str(ion),
                            str(par),
                            str(self.site_iter[it][ion]),
                            str(self.epar_iter[it][ion][par]),
                        )
                    )
        elif ion is not None and par is not None and (l is not None):
            par = int(par)
            ion = int(ion)
            # print "iter=",it,"",self.site_iter[it][ion],self.epar_iter[it][ion][par]
            for it in range(self.nscf):
                print(
                    "iter= %s %s %s"
                    % (
                        str(it),
                        str(self.site_iter[it][ion]),
                        str(self.epar_iter[it][ion][par]),
                    )
                )
        elif ion is not None and par is None and (l is not None):
            ion = int(ion)
            l = int(l)
            l_orbit_txt = ":E.*_.*: E\\(.*" + str(l) + "\\)"
            l_orbit_reg = re.compile(l_orbit_txt)
            for it in range(self.nscf):
                for par in range(len(self.epar_iter[it][ion])):
                    # print "ion=",ion,"",self.epar_iter[it][ion][par]
                    if bool(l_orbit_reg.match(self.epar_iter[it][ion][par])):
                        print(
                            "ion= %s %s" % (str(ion), str(self.epar_iter[it][ion][par]))
                        )
        elif ion is None and par is None and (l is not None):
            l = int(l)
            l_orbit_txt = ":E.*_.*: E\\(.*" + str(l) + "\\)"
            l_orbit_reg = re.compile(l_orbit_txt)
            for it in range(self.nscf):
                for ion in range(self.nion):
                    for par in range(len(self.epar_iter[it][ion])):
                        if bool(l_orbit_reg.match(self.epar_iter[it][ion][par])):
                            print("%s" % str(self.epar_iter[it][ion][par]))
