#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# WIEN2k 用 XAS plot 用関数 (nonmag)
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.04.06
#  1) Wplot_XAS.py から分離
#  2) xspec & txspec クラスの引数変更に対応
#
################################################################################
from __future__ import print_function

try:
    from copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *

__status__ = "alpha"
__version__ = "0.0.1"


################################################################################
def plot_xas(case='case',
             dos_suffix='.dos1ev',
             txspec_suffix='.txspec',
             xspec_suffix='.xspec',
             outname='XAS', OPT_EMAX='None', OPT_EMIN='None', OPT_YMAX='None', FLAG_SHOW=True):
    import matplotlib.pyplot as plt
    # import matplotlib.cm as cm
    # import matplotlib.mlab as mlab

    import StructureAnalysisEnvironment as SAE
    # import SpaceGroupEnvironment as SGE

    ############################################
    # set input file
    #   case,OPT_EMAX,OPT_EMIN,OPT_YMAX = options()

    if OPT_EMAX:
        print("Emax= %s" % str(OPT_EMAX))
    if OPT_EMIN:
        print("Emin= %s" % str(OPT_EMIN))
    if OPT_YMAX:
        print("Ymax= %s" % str(OPT_YMAX))

    ############################################
    # txspec instance ( unbroad XAS )
    txspec = SAE.ReadWienTxspec(case=case, suffix=txspec_suffix)
    #   eng_unbroad = txspec.get_eng()
    #   eng_unbroad_emin = txspec.get_emin()
    #   eng_unbroad_emax = txspec.get_emax()
    unbroad = txspec.get_unbroad_xas()

    ############################################
    # xspec instance ( XAS )
    xspec = SAE.ReadWienXspec(case=case, suffix=xspec_suffix)
    eng_xas = xspec.get_eng()
    #   eng_xas_min = xspec.get_emin()
    #   eng_xas_max = xspec.get_emax()
    xas = xspec.get_xas()

    ############################################
    # dos instance
    unit = 'ev'
    name = [case + dos_suffix]

    print('DOS = %s' % str(name[0]))
    dos = SAE.ReadWienDos(name)
    efermi = dos.get_efermi()
    eng = dos.get_eng()
    eng_emin = dos.get_emin()
    eng_emax = dos.get_emax()

    norbital = dos.get_norbital()
    if norbital == 2:
        mode = 'K'  # or L1
    elif norbital == 3:
        mode = 'L'
    print("MODE = %s" % str(mode))

    dos_total = dos.get_raw_dos(atom=0, orbit='total-DOS')
    if mode == 'K':  # or L1
        dos_p = dos.get_raw_dos(atom=1, orbit='p')
    else:
        dos_s = dos.get_raw_dos(atom=1, orbit='s')
        dos_d = dos.get_raw_dos(atom=1, orbit='d')

    ############################################################################
    # matplotlib

    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size'] = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth'] = 1.5  # 軸の太さを設定。目盛りは変わらない

    plt.figure(figsize=(7.00, 9.89))  # for portrait

    ############################################################################

    orgx = 0.150
    # orgx = 0.130
    orgy = 0.080
    # orgy = 0.100
    off = 0.010
    xsize = 0.75

    ysize0 = 0.83

    if mode == 'K':  # or L1
        ysize = ysize0 / 3.5
        ysize_dos = ysize0 / 4
    else:
        ysize = ysize0 / 4
        ysize_dos = ysize0 / 4.8

    ####################################################################
    # 軸調整
    if OPT_EMAX:
        emax = float(OPT_EMAX)
    else:
        emax = eng_emax

    if OPT_EMIN:
        emin = float(OPT_EMIN)
    else:
        emin = eng_emin

    ####################################################################
    # DOS (*.dos1) TOTAL
    plt.axes([orgx, orgy, xsize, ysize_dos])  # 原点位置を自動調整
    eng = eng - efermi
    plt.plot(eng, dos_total, color='black', linewidth=2, label='total-DOS')
    plt.ylabel("DOS [unit/" + unit + "]")
    plt.xlabel("Energy above Fermi [" + unit + "]")
    plt.axvline(x=0, color='black', linewidth=1)

    plt.xlim([emin, emax])
    plt.ylim(ymin=0)

    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)

    ####################################################################
    # DOS (*.dos1) p-orbital
    # dennsity of states for conduction electron
    if mode == 'K':  # or L1
        ###################### p
        orgy = orgy + ysize_dos + off
        plt.axes([orgx, orgy, xsize, ysize_dos])  # 原点位置を自動調整
        eng = eng - efermi
        plt.plot(eng, dos_p, color='black', linewidth=2, label='p')
        plt.xticks([])
        plt.xlabel("")
        plt.ylabel("")
        plt.axvline(x=0, color='black', linewidth=1)

        plt.xlim([emin, emax])
        plt.ylim(ymin=0)

        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)
    else:
        ###################### s
        orgy = orgy + ysize_dos + off
        plt.axes([orgx, orgy, xsize, ysize_dos])  # 原点位置を自動調整
        eng = eng - efermi
        plt.plot(eng, dos_s, color='black', linewidth=2, label='s')
        plt.xticks([])
        plt.xlabel("")
        plt.ylabel("")
        plt.axvline(x=0, color='black', linewidth=1)

        plt.xlim([emin, emax])
        plt.ylim(ymin=0)

        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)

        ###################### d
        orgy = orgy + ysize_dos + off
        plt.axes([orgx, orgy, xsize, ysize_dos])  # 原点位置を自動調整
        eng = eng - efermi
        plt.plot(eng, dos_d, color='black', linewidth=2, label='d')
        plt.xticks([])
        plt.xlabel("")
        plt.ylabel("")
        plt.axvline(x=0, color='black', linewidth=1)

        plt.xlim([emin, emax])
        plt.ylim(ymin=0)

        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)

    ############################################################################
    # XAS ( *.xspec and *.txspec )
    orgy = orgy + ysize + off + off + off + off
    plt.axes([orgx, orgy, xsize, ysize])  # 原点位置を自動調整
    # broad (XAS)
    plt.plot(eng_xas, xas, color='black', linewidth=2, label='XAS')
    # plt.fill_between(eng_xas,xas, color='#cccccc', linewidth=2, label='XAS')
    # unbroad (XAS)
    plt.plot(eng_xas, unbroad, linestyle='-', color='green', linewidth=0.8, label='unbroad')
    plt.yticks([])
    # plt.xlabel("")
    plt.xlabel("Energy above Fermi [" + unit + "]")
    plt.ylabel("Absorption [arb. unit]")
    plt.axvline(x=0, color='black', linewidth=1)

    plt.xlim([emin, emax])
    plt.ylim(ymin=0)

    leg = plt.legend(fontsize=12)
    leg.get_frame().set_alpha(0.5)

    ############################################################################
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    else:
        ymax = xspec.get_ymax_xas()
        ymax0 = ymax / 10.0
        ymax = ymax + ymax0 * 1.5
        plt.ylim(ymax=ymax)

    plt.savefig(outname + ".eps")
    plt.savefig(outname + ".pdf")
    plt.savefig(outname + ".png")

    if FLAG_SHOW:
        plt.show()

    plt.close('all')
