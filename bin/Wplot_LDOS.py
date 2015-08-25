#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Wplo_LDOS.py
#
#   MXplot_LDOS.py (2015.03.25) ベースで作成
#
#   using ReadWeinDos, ReadWeinOutput0
#   基本動作は Wldos.py (2015.03.25) ベースで作成
#
################################################################################
#
# 2015.04.21
#  ケアレスミス（オービタルを呼び出す名前を間違っていた),ただしかなり重要なミス
#
# 2015.03.27
#  unit の表示
#
# 2015.03.27
#  total-DOS がないときの処理と原子毎のtotal の処理
#
# 2015.03.26
#  軌道成分の存在確認＆出力の有無の自動判別を追加
#
# 2015.03.26
#  get_ldos_ion() にて読んでいる case.output0 は並列計算すると
#  output0000 になるので注意、修正した
#
# 2015.03.26
#  暫定版
#
# 2015.03.25
#  startup
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
__version__    = "0.1.0"
################################################################################

import sys
import os
import re
#import gzip
import optparse
#import numpy as np

#import re
#from copy import deepcopy

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

import matplotlib.pyplot as plt
import matplotlib.cm as cm
#import matplotlib.mlab as mlab

################################################################################
def options():

    name = re.sub('.*/','',os.getcwd())
    unit = 'ev'

    parser = optparse.OptionParser(os.getcwd())

    parser.add_option( '-i', '--input', dest='INPUT',)
    parser.add_option( '-e', '--ev', action='store_true', default=False,)
    parser.add_option( '-f', '--fermi', action='store_true', default=False,)
    parser.add_option( '-n', '--nw', action='store_true', default=False,)
    parser.add_option( '-a', '--atomtot', action='store_true', default=False,)
    parser.add_option( '--emax', dest='EMAX',)
    parser.add_option( '--emin', dest='EMIN',)
    parser.add_option( '--ymax', dest='YMAX',)
    options,  args = parser.parse_args()

    if options.ev:
        unit='ev'
    else:
        unit='None'

    if options.INPUT:
        name = options.INPUT

    plot_ions=[]
    if len(args) > 0:
        for i in range(0,len(args)):
            plot_ions.append(int(args[i]))
    else:
        plot_ions = [1]

    return [name,unit,options.fermi,\
            options.nw,options.atomtot,\
            options.EMAX,options.EMIN,options.YMAX,plot_ions]

################################################################################
if __name__ == '__main__':

    ############################################
    # set input file
    case,unit,FERMI,\
            NO_WINDOW_FLAG,AT_FLAG,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,plot_ions = options()

    if OPT_EMAX: print "Emax=",OPT_EMAX
    if OPT_EMIN: print "Emin=",OPT_EMIN
    if OPT_YMAX: print "Ymax=",OPT_YMAX

    # ION の種類(サイトの種類)で番号を入力
    if len(plot_ions) > 1:
        print "Plot Ions:"
        for i in plot_ions:
            print i,
        print ""

    ############################################
    # case.dos ファイルを抽出
    lists = SAE.find_suffix3(case+'.dos',unit)
    if not lists:
        sys.exit("STOP: "+case+".dos* file not found")

    print "READ FILE    :",
    for i in lists:
        print i,
    print ""

    ############################################
    # unit の書き直し
    if unit == 'ev':
        unit = 'eV'
        FERMI = True
    else:
        unit = 'Ry'

    ############################################
    # check SPIN
    if os.path.exists(case+'.output0'):
        output0_file = case+'.output0'
    elif os.path.exists(case+'.output0.gz'):
        output0_file = case+'.output0.gz'
    elif os.path.exists(case+'.output0000'):
        output0_file = case+'.output0000'
    elif os.path.exists(case+'.output0000.gz'):
        output0_file = case+'.output0000.gz'
    else:
        sys.exit("STOP: output0 file not found")

    output0 = SAE.ReadWienOutput0(output0_file)
    nspin = output0.get_ispin()
    nion = output0.get_nion()
    ions_index = output0.get_ions_index()

    FLAG_SPIN = False
    if nspin >= 2:
        FLAG_SPIN = True

    ############################################
    # check NION
    if len(plot_ions) > nion:
        sys.exit("STOP: nion="+str(nion))

    if max(plot_ions) > nion:
        sys.exit("STOP: nion="+str(nion))

    ############################################
    # SPIN 有りの時に list のスピン毎の作り直し
    if FLAG_SPIN:
        up = []
        dn = []
        for i in lists:
            up.append(re.sub('up','',re.sub('dn','',i))+'up')
            dn.append(re.sub('up','',re.sub('dn','',i))+'dn')
        up_lists = list(set(up))
        dn_lists = list(set(dn))


    ############################################################################
    # matplotlib
   #plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['font.size']         = 20  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 10  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

    #################################
    # for spin-loop
    for spin in range(nspin):

        ############################
        # makes instance
        if FLAG_SPIN and spin == 0:
            lists = up_lists
        if FLAG_SPIN and spin == 1:
            lists = dn_lists

        dos = SAE.ReadWienDos(lists)

        nion = dos.get_nion()
        nedos = dos.get_nedos()
        efermi = dos.get_efermi()
        emax = dos.get_emax()
        emin = dos.get_emin()
        eng = dos.get_eng()
       #plot_ions = dos.get_plot_ions()

        title =  case

        ########################################################
        if nspin == 1:
            plt.axes([ 0.130,0.130, 0.80,0.80 ])  # 一段組の原点(x,y), 幅(x,y)
            plt.title(title)
        if nspin == 2:
            if spin == 0:
                plt.axes([ 0.130,0.530, 0.80,0.40 ])  # 二段組の上側(y幅半分) up-spin
                plt.title(title)
            if spin == 1:
                plt.axes([ 0.130,0.130, 0.80,0.40 ])  # 二段組の下段( down-spin )

        j=0 # カラーの自動調節用
        for ion in plot_ions:

            ############################################
            # ION のラベル
            if len(plot_ions) > 1:
                if ion == 0:
                    sys.exit("STOP:INPUT ERROR, ion= 0")
            ion_label =str(ions_index[ion-1])

            if nspin == 1:
                print "ion =",ion,ion_label
            else:
                print "ion(spin) =",ion,"("+str(spin+1)+")",ion_label

            ############################################
            # X軸
            e = []
            for i in range(nedos):
                if FERMI:
                    e.append(eng[i] - efermi)
                else:
                    e.append(eng[i])

            ############################################
            # Y軸チェック&プロット
            #     autumn, bone, cool, copper, flag, gray, hot, hsv,
            #     jet, pink, prism, spring, summer, winter, spectral
            TDOS_FLAG=True
            if dos.chk_raw_dos(atom=0,orbit='total-DOS'):
                tdos = dos.get_raw_dos(atom=ion,orbit='total-DOS')
                plt.fill_between(e,tdos, color='#cccccc', linewidth=2, label='total')
            else:
                TDOS_FLAG=False

            if dos.chk_raw_dos(atom=ion,orbit='total') and AT_FLAG:
                t = dos.get_raw_dos(atom=ion,orbit='total')
                if TDOS_FLAG:
                    c = 'black'
                    plt.plot(e,t, linestyle=":", color=c, linewidth=2, label=ion_label+'-tot')
                else:
                    plt.fill_between(e,t, color='#cccccc', linewidth=2, label=ion_label+'-tot')

            if dos.chk_raw_dos(atom=ion,orbit='s'):
                s = dos.get_raw_dos(atom=ion,orbit='s')
                c = cm.prism(float(j)/(nion*2))
                plt.plot(e,s, linestyle=":", color=c, linewidth=2, label=ion_label+'-s')
                j += 1

            if dos.chk_raw_dos(atom=ion,orbit='p'):
                p = dos.get_raw_dos(atom=ion,orbit='p')
                c = cm.prism(float(j)/(nion*2))
                plt.plot(e,p, linestyle="-", color=c, linewidth=2, label=ion_label+'-p')
                j += 1

            if dos.chk_raw_dos(atom=ion,orbit='d'):
                d = dos.get_raw_dos(atom=ion,orbit='d')
                c = cm.prism(float(j)/(nion*2))
                plt.plot(e,d, linestyle="--", color=c, linewidth=2, label=ion_label+'-d')
                j += 1

            if dos.chk_raw_dos(atom=ion,orbit='f'):
                f = dos.get_raw_dos(atom=ion,orbit='f')
                c = cm.prism(float(j)/(nion*2))
                plt.plot(e,f, linestyle="-.", color=c, linewidth=2, label=ion_label+'-f')
                j += 1

            ############################################
            # Y軸の調整
            plt.ylim( ymin=0 )

        if spin == 0: yl = plt.ylabel("DOS/"+unit, fontsize=20 )
        if OPT_EMAX: plt.xlim( xmax=int(OPT_EMAX) )
        if OPT_EMIN: plt.xlim( xmin=int(OPT_EMIN) )
        if OPT_YMAX: plt.ylim( ymax=int(OPT_YMAX) )

        if nspin == 2:
            if spin == 0:
                plt.xticks([])
            if spin == 1:
                # y 軸反転
                xmin,xmax,ymin,ymax = plt.axis()
                plt.ylim([ymax,0])

        # EF0
        if FERMI:
            plt.axvline(x=0,color="black",linewidth=1)
        else:
            plt.axvline(x=efermi,color="black",linewidth=1)

    ############################################################################

    if FERMI:
        plt.xlabel("$E -  E_{\mathrm{F}}$ ["+unit+"]", fontsize=20 )
    else:
        plt.xlabel("$E$ ["+unit+"]", fontsize=20 )

    leg = plt.legend(fontsize=12)   # 凡例Box
    leg.get_frame().set_alpha(0.5)  # Alphaチャンネル(半透明化)

#   plt.xlim([-10,10])
#   plt.ylim([0,200])

    plt.savefig("LDOS.eps")
    plt.savefig("LDOS.pdf")
    plt.savefig("LDOS.png")

    if not NO_WINDOW_FLAG:
        plt.show()

    plt.close('all')

#############################################################################
