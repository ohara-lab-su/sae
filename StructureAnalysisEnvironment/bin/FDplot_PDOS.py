#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#   特定原子の PDOS 多段組
#
#   平均化機能は付けていない
#   DOSやXANESの平均化が欲しいときは FDplot_XAS.py -a 1 2 3 -w 55 -x 10
#   などとして、FDplot_XAS.py を用いて、 filout_0.txt filout_0_sd0.txt を
#   作成してから -c -s オプションなどを用いてプロットする
#
################################################################################
#
# 2018.08.17
#  Python2/3 両対応
#
# 2015.09.11
#  spin 対応版
#
# 2015.09.08
#  DOS の最大レンジ自動取得
#
# 2015.09.08
#   DOS のウェイト追加
#
# 2015.09.08
#  conv, txt, sd の同名指定オプション --name を追加
#
# 2015.09.07
#  startup
#
################################################################################
from __future__ import print_function

################################################################################
__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
#
__status__ = "alpha"
__version__ = "0.0.1"

################################################################################

import sys
# import gzip
import os
# import re
import optparse
# import numpy as np

import StructureAnalysisEnvironment as SAEnv
# import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm


################################################################################
def options():
    parser = optparse.OptionParser()

    parser.add_option('-i', '--inp', '--inpname', dest='INPUT')
    parser.add_option('-f', '--filout', '--filoutname', dest='filoutname')
    parser.add_option('-c', '--conv', '--convname', dest='convname')
    parser.add_option('-t', '--txt', '--txtname', dest='txtname')
    parser.add_option('-s', '--sd', '--sdname', dest='sdname')
    parser.add_option('--filbav', '--bavname', dest='bavname')
    parser.add_option('--name')
    parser.add_option('--output')
    parser.add_option('-a', '--atom')
    parser.add_option('--emax')
    parser.add_option('--emin')
    parser.add_option('--ymax')  # XAS の ymax
    parser.add_option('--dmax')  # DOS の ymax共通
    parser.add_option('--label')
    parser.add_option('--outsuffix')
    parser.add_option('--weight')  # 同時設定
    parser.add_option('--xasweight')  # for XAS with convolution
    parser.add_option('--txtweight')  # for XAS without convolution
    parser.add_option('--dosweight')  # for LDOS
    parser.add_option('-b', '--broad', action='store_true', default=False)
    parser.add_option('-x', '--xas', action='store_true', default=False)
    parser.add_option('--total', action='store_true', default=False)
    parser.add_option('--intdos', action='store_true', default=False)
    parser.add_option('--fermi', action='store_true', default=False)
    parser.add_option('--s', action='store_true', default=False)
    parser.add_option('--p', action='store_true', default=False)
    parser.add_option('--sp', action='store_true', default=False)
    parser.add_option('--spd', action='store_true', default=False)
    parser.add_option('--up', action='store_true', default=False)
    parser.add_option('--dn', '--down', action='store_true', default=False, dest='dn')
    parser.add_option('--spin', action='store_true', default=False)
    # 逆のスイッチ:pdf のみ出力を diable にする ( default は pdf )
    parser.add_option('--pdf', action='store_true', default=False)
    parser.add_option('--nw', action='store_true', default=False)

    options, args = parser.parse_args()

    ########## default inpname 取得
    if options.INPUT:
        inpname = options.INPUT
    else:
        if os.path.exists('fdmfile.txt'):
            fdmfiletxt = SAEnv.io.ReadFdmFdmfile()
            inpname = fdmfiletxt.filout
        else:
            inpname = 'read_pdb.inp'

    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + ' file not fount')

    if len(args) > 0: inpname = args[0]

    if options.name:
        options.convname = options.name
        options.txtname = options.name
        options.sdname = options.name

    return [options.output, options.outsuffix,
            inpname,
            options.convname, options.txtname,
            options.filoutname, options.bavname, options.sdname,
            options.name,
            options.atom, options.label,
            options.emax, options.emin, options.ymax, options.dmax,
            options.broad, options.fermi, options.xas,
            options.up, options.dn, options.spin,
            options.s, options.p, options.sp, options.spd,
            options.weight,
            options.dosweight, options.xasweight, options.txtweight,
            options.total, options.intdos, options.pdf, options.nw]


################################################################################
if __name__ == '__main__':

    outputname, OUTSUFFIX, \
    inpname, \
    convname, txtname, \
    filout, bavname, sdname, \
    allname, \
    atom, LABEL, \
    OPT_EMAX, OPT_EMIN, OPT_YMAX, OPT_DMAX, \
    FLAG_BROAD, FLAG_FERMI, FLAG_XAS, \
    FLAG_UP, FLAG_DN, FLAG_SPIN, \
    FLAG_S, FLAG_P, FLAG_SP, FLAG_SPD, \
    WE, \
    WEDOS, WEXAS, WETXT, \
    FLAG_TOTAL, FLAG_INTDOS, FLAG_PDF, FLAG_NW = options()

    ###########################################################################

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 15  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth'] = 1.4  # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    orgx = 0.170
    orgy = 0.080
    off = 0.016
    xsize = 0.75
    ysize0 = 0.81

    ###########################################################################

    # for default
    list1_1 = ['s']
    list1_2 = ['p_y', 'p_z', 'p_x']
    list1_3 = ['d_xy', 'd_yz', 'd_3z2-r2', 'd_xz', 'd_x2-y2']
    list1 = [list1_1, list1_2, list1_3]

    # for hexagonal (s-orbital and p-orbital MODE)
    list4_1 = ['s']
    list4_2 = ['p_z']
    list4_3 = ['p_y', 'p_x']
    list4 = [list4_1, list4_2, list4_3]

    ###########################################################################

    if FLAG_BROAD: FLAG_XAS = True
    if OPT_EMAX: print("Emax=", OPT_EMAX)
    if OPT_EMIN: print("Emin=", OPT_EMIN)
    if FLAG_XAS and OPT_YMAX: print("Ymax(XAS)=", OPT_YMAX)
    if OPT_DMAX: print("Ymax(DOS)=", OPT_DMAX)

    if atom: print("ATOM=", atom)

    if WEDOS:
        print("Weight for DOS =", WEDOS)
        WEDOS = float(WEDOS)
    else:
        WEDOS = None

    if WE:
        print("Weight for XAS", WE)
        WEXAS = float(WE)
        WETXT = float(WE)

    if WETXT:
        print("Weight for XAS without convolution =", WETXT)
        WETXT = float(WETXT)
    else:
        WETXT = None

    if WEXAS:
        print("Weight for XAS with convolution =", WEXAS)
        WEXAS = float(WEXAS)
    else:
        WEXAS = None

    ###########################################################################

    inp = SAEnv.io.ReadFdmInp(inpname)

    if not atom and not inp.nonexc:
        atom = 0
    if not atom and inp.nonexc:
        atom = 1

    suffix_sd = '_sd' + str(atom) + '.txt'
    suffix_conv = '_conv.txt'

    if allname:
        convolname = allname
        txtname = allname
        sdname = allname

    if filout is None: filout = inp.filout
    if convname is None: convname = filout
    if txtname is None: txtname = filout
    if bavname is None: bavname = filout
    if sdname is None: sdname = filout

    print("")
    print("inpname    (.inp)                  =", inpname)
    print("filoutname                         =", filout)
    print("txtname    (original XAS and Eferm)=", txtname)
    print("convname   (convolution file)      =", convname)
    print("bavname    (log file)              =", bavname)
    print("")

    #   bav = SAE.io.ReadFdmBav(bavname)
    txt = SAEnv.io.ReadFdmTxt(txtname, '.txt', weight=WETXT)
    conv = SAEnv.io.ReadFdmConv(convname, suffix_conv, weight=WEXAS)
    #   sd0 = SAE.io.ReadFdmSd(sdname, '_sd0.txt',weight=WEDOS)
    sd = SAE.io.ReadFdmSd(sdname, suffix_sd, weight=WEDOS)

    ispin = inp.ispin
    if ispin >= 2:
        print("")
        print("Current calculation is Magnetic: SPIN MODE")
        print("")

    ###########################################################################

    # 選択した atom の最大の lmax を取得
    lmax = sd.lmax

    if FLAG_SPD and lmax >= 2:
        print("ORBITAL MODE: Default Orbitals")
        block_list = list1
    elif FLAG_SP and lmax >= 1:
        print("ORBITAL MODE: s-orbital and p-orbital")
        block_list = list4
    elif lmax == 1:
        print("ORBITAL MODE: s-orbital and p-orbital")
        block_list = list4
    elif lmax >= 2:
        print("ORBITAL MODE: Default Orbitals")
        block_list = list1

    nblock = len(block_list)

    # spin の有無と spin の描画モードでの多段組の数およびスピンリストの変更
    spin_list = [0]
    spin_suffix = ['']
    spin_out = ''
    nspin = 1
    if FLAG_UP:
        nspin = 1
        spin_list = [0]
        spin_suffix = ['_up', '']
        spin_out = '_up'
    elif FLAG_DN:
        nspin = 1
        spin_suffix = ['', '_dn']
        spin_list = [1]
        spin_out = '_dn'
    elif FLAG_SPIN or ispin >= 2:
        FLAG_SPIN = True
        nspin = 2
        spin_list = [1, 0]
        spin_suffix = ['_up', '_dn']
        spin_out = '_spin'

    if FLAG_XAS:
        ysize = ysize0 / (nblock * nspin + 1)
    else:
        ysize = ysize0 / (nblock * nspin)

    ###########################################################################

    ############################################ convert Energy (set eng_off)
    # PhotoEnegy モードで計算した時と同じ結果を返す
    if not inp.get_energygpho() and not FLAG_FERMI:
        print("current mode is Fermi")
        print("---> convert to PhotoEnergy")
        print("     + E_edge")
        eng_off = txt.E_edge

    # E_fermi を引く(A) : A=B
    if not inp.get_energygpho() and FLAG_FERMI:
        print("current mode is Fermi")
        print("---> subtract E_fermi")
        print("     - E_fermi")
        eng_off = - txt.E_fermi

    # E_fermi を引く(B) : A=B
    if inp.get_energygpho() and FLAG_FERMI:
        print("current mode is PhotoEnergy")
        print("---> convert to EF0 mode")
        print("     - E_edge - E_fermi")
        eng_off - txt.E_Fermi - txt.E_edge

    if FLAG_FERMI:
        EF0 = 0.0
        label_fermi = "Energy above Fermi [eV]"
    else:
        EF0 = txt.E_edge + txt.E_Fermi
        label_fermi = "Photon Energy [eV]"

    if OPT_EMAX is None:
        emax = sd.emax + EF0
        print("EMAX = ", emax)

    if OPT_EMIN is None:
        emin = sd.emin + EF0
        print("EMIN = ", emin)

    ######################################### plot XAS
    num = 0
    XTICKS_FLAG = False
    if FLAG_XAS:

        plt.axes([orgx, orgy, xsize, ysize])

        xas = conv.get_xas()
        engx = conv.get_eng() + eng_off

        # makes xticks
        plt.ylabel("Absorption [arb. unit]")
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True

        # makes label & color
        label = 'XAS (with broadening)'

        # !!!!! plot XAS !!!!!
        plt.plot(engx, xas, linewidth=2, color='black', label=label)
        plt.ticklabel_format(axis='x', useOffset=False)
        plt.axvline(x=EF0, color='black', linewidth=1)
        xmin_XAS, xmax_XAS, ymin_XAS, ymax_XAS = plt.axis()
        plt.ylim(ymin=0.0)

        # !!!!! plot XAS ( non broad ) !!!!!
        if FLAG_BROAD:

            eng_p = txt.eng + eng_off
            for spin in spin_list:
                xas_r = txt.get_xas(spin=spin)
                num += 1
                color = cm.prism((num) * 10)
                label = 'XAS' + spin_suffix[spin]

                plt.plot(eng_p, xas_r, linewidth=1, color=color, label=label)
                plt.ylim(ymax=ymax_XAS)
                plt.ylim(ymin=0.0)

        if not OPT_EMAX: plt.xlim(xmax=emax)
        if not OPT_EMIN: plt.xlim(xmin=emin)

        if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX: plt.ylim(ymax=float(OPT_YMAX))

        leg = plt.legend(loc='lower right')
        leg.get_frame().set_alpha(0.5)

        # label & xticks
        plt.ylabel("Absorption [arb. unit]")
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True

        orgy = orgy + ysize + off

    #   print "XTICKS", XTICKS_FLAG
    ######################################### plot PDOS
    #
    eng = sd.eng + eng_off
    for blk in range(nblock - 1, -1, -1):

        lm_list = block_list[blk]

        for spin in spin_list:

            plt.axes([orgx, orgy, xsize, ysize])

            dmax0 = 0.0
            for orbit in lm_list:

                dos = sd.get_pdos(lm=orbit, spin=spin)

                dmax = sd.ymax
                if dmax0 < dmax:
                    dmax0 = dmax

                # makes label & color
                num += 1
                if not LABEL:
                    label = str(atom) + '-' + orbit + spin_suffix[spin]
                else:
                    label = str(LABEL) + '-' + orbit + spin_suffix[spin]
                color = cm.prism((num + 1) * 10)

                # !!!!! plot PDOS !!!!!
                plt.plot(eng, dos, linewidth=2, color=color, label=label)
                plt.ticklabel_format(axis='x', useOffset=False)
                plt.axvline(x=EF0, color='black', linewidth=1)
                plt.ylim(ymin=0.00)

                if not OPT_DMAX: plt.ylim(ymax=float(dmax0))
                if OPT_DMAX: plt.ylim(ymax=float(OPT_DMAX))

                # DOS: down spin 反転
                if FLAG_SPIN and spin == 1:
                    xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                    plt.ylim([ymax_dn, 0])

                if not OPT_EMAX: plt.xlim(xmax=emax)
                if not OPT_EMIN: plt.xlim(xmin=emin)
                if OPT_EMAX: plt.xlim(xmax=float(OPT_EMAX))
                if OPT_EMIN: plt.xlim(xmin=float(OPT_EMIN))
                xmin0, xmax0, ymin0, ymax0 = plt.axis()
                # print orbit,": ymax =",dmax0,ymax0

                if FLAG_XAS:
                    plt.xticks([])
                else:
                    if not blk == (nblock - 1):
                        plt.xticks([])
                    if blk == (nblock - 1):
                        if spin == 0 and nspin == 2:
                            plt.xticks([])

                # makes label
                if not XTICKS_FLAG:
                    plt.xlabel(label_fermi)
                    XTICKS_FLAG = True

                leg = plt.legend(loc='upper right')
                leg.get_frame().set_alpha(0.5)

            orgy = orgy + ysize

        if blk == 1: plt.ylabel("DOS [state/eV]")
        #       if blk == 2 and FLAG_XAS: plt.xticks([])

        orgy = orgy + off

    ###############################################################

    if FLAG_FERMI:
        fermi = '_fermi'
    else:
        fermi = ''

    if outputname:
        _head = outputname + "_"
        print("output header =", outputname)
    else:
        _head = "PDOS"

    if OUTSUFFIX:
        _outsuffix = str(OUTSUFFIX)
    else:
        _outsuffix = ''

    plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".pdf")
    if FLAG_PDF:
        plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".eps")
        plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".png")

    if not FLAG_NW:
        plt.show()

    plt.close('all')

#   print "NAME",name
