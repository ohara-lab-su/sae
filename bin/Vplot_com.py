#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# Vplot_com.py
#
#  vplot_com10.pl/com11.pl モドキ
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
# 2015.02.06
#  band の plot で spd 分解（全原子まとめて表示、原子毎表示）を追加
#
# 2015.01.30
#  DOS プロットのところに s,p,d 表示を追加(TOTAL_spd)
#
# 2015.01.30
#  Vplot_band.py と同等のものを PROCAR から作成
#  ---> Vplot_com_band.py と暫定的に名前を変えて、そのバージョンを保存
#
# 2015.01.29 startup
#
################################################################################
from __future__ import print_function
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
m_mmail__      = "kmngo.nakada@gmail.com"
__copyright__  = "Copyright 2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.0.2"
################################################################################

import sys
import os
#import gzip
import optparse
import numpy as np

#import re
#from copy import deepcopy
import matplotlib.pyplot as plt

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
def options():

    # 必須ファイル(vasprun.xml に置き換え可能)
    procarname = 'PROCAR'
    kpointsname = 'KPOINTS'
    doscarname = 'DOSCAR'
    outcarname = 'OUTCAR'
    symdatname = 'sym.dat'

    out1 = 'band1.dat'
    out2 = 'band2.dat'

    parser = optparse.OptionParser()

    ###########################################
    # INPUT files
    parser.add_option(  '-p','--procar', dest='PROCAR', default=procarname,)
    parser.add_option(  '-o','--outcar', dest='OUTCAR', default=outcarname,)

    parser.add_option(  '-k','--kpoints', dest='KPOINTS', default=kpointsname,)
    parser.add_option(  '-d','--doscar', dest='DOSCAR', default=doscarname,)
    parser.add_option(  '-s','--symdat', dest='SYMDAT', default=symdatname,)
    ###########################################
    # FLAGS
    parser.add_option(  '-a','--absolute',
                        action='store_true',
                        default=False,
                        dest='ABS_FLAG',
    )
    parser.add_option(  '-1','--up',
                        action='store_true',
                        default=False,
                        dest='UP_SPIN_FLAG',
    )
    parser.add_option(  '-2','--down',
                        action='store_true',
                        default=False,
                        dest='DOWN_SPIN_FLAG',
    )
    parser.add_option(  '-i','--index',
                        action='store_true',
                        default=False,
                        dest='INDEX_FLAG',
    )
    parser.add_option(  '-l','--line',
                        action='store_true',
                        default=False,
                        dest='LINE_FLAG',
    )
    parser.add_option(  '-w','--withdos',
                        action='store_true',
                        default=False,
                        dest='DOS_FLAG',
    )
    parser.add_option(  '--spd',
                        action='store_true',
                        default=False,
                        dest='SPD_FLAG',
    )
    parser.add_option(  '--com',
                        action='store_true',
                        default=False,
                        dest='PRO_FLAG',
    )
    ###########################################
    # Parameters
    parser.add_option(  '--emin', dest='EMIN',)
    parser.add_option(  '--emax', dest='EMAX',)
    parser.add_option(  '--band', dest='BAND',)
    parser.add_option(  '--atom', dest='ATOM',)
    options,  args = parser.parse_args()


    return [options.PROCAR,options.OUTCAR,\
            options.KPOINTS,options.DOSCAR,options.SYMDAT,\
            out1,out2,\
            options.ABS_FLAG,options.UP_SPIN_FLAG,options.DOWN_SPIN_FLAG,\
            options.INDEX_FLAG,options.LINE_FLAG,options.DOS_FLAG,\
            options.SPD_FLAG,options.PRO_FLAG,\
            options.EMIN,options.EMAX,options.BAND,options.ATOM]


################################################################################
if __name__ == '__main__':

    procarname,outcarname,kpointsname,doscarname,symdatname,\
            out1,out2,\
            ABS_FLAG,UP_FLAG,DOWN_FLAG,\
            INDEX_FLAG,LINE_FLAG,DOS_FLAG,\
            SPD_FLAG,COM_FLAG,\
            OPT_EMIN,OPT_EMAX,OPT_BAND,OPT_ATOM = options()

    print "PROCAR   :",procarname
    print "OUTCAR   :",outcarname
    print "KPOINTS  :",kpointsname
    print "DOSCAR   :",doscarname

    if OPT_EMIN: print "EMIN       :",OPT_EMIN
    if OPT_EMAX: print "EMAX       :",OPT_EMAX
    if UP_FLAG: print "UP_SPIN    :",UP_FLAG
    if DOWN_FLAG: print "DOWN_FLAG  :",DOWN_FLAG
    if OPT_BAND: print "BAND       :",OPT_BAND
    if OPT_ATOM: print "ATOM       :",OPT_ATOM
    if DOS_FLAG: print "WRITE DOS  :",DOS_FLAG
    if SPD_FLAG: print "SPD MODE   :",SPD_FLAG

    # 基本インスタンス生成
    procar = SAE.ReadVaspProcar(procarname)
    kpoints = SAE.ReadVaspKpoints(kpointsname)

    # バンドの基本情報取得
#   TITLE = doscar.get_title()
    NATOM = procar.get_natom()
    NKPTS = procar.get_nkpts()
    NBANDS = procar.get_nbands()
    NSPIN = procar.get_ispin()
    LORBIT = procar.get_lorbit()

    # K点&バンドごとのデータ
    if not SPD_FLAG:
        pro_all = procar.get_pro_all()
        kp,eigenval,occ,pro,pro_ratio = pro_all
    else:
        pro_spd = procar.get_pro_spd()
        kp,eigenval,occ,pro,pro_ratio = pro_spd

    # K点のゾーン情報(KPOINTS & OUTCAR)
    kpoints_array = kpoints.get_kpoints_array()
    num_kpoints_line = kpoints.get_num_kpoints_line()
    div_kpoints_line = kpoints.get_div_kpoints_line()
    zone_ratio = kpoints.get_kpoints_vector_ratio(outcarname)

    # データーのチェック
    flags = kpoints.get_kpoints_mode()
    if flags[0]:
        sys.exit("STOP: KPOINTS file format error")
    if not flags[1]:
        sys.exit("STOP: KPOINTS file format error")

    if num_kpoints_line != NKPTS/div_kpoints_line:
        print "STOP: KPONTS lines =",num_kpoints_line
        sys.exit("STOP: NKPTS inconsistence")

    ############################################################################
    # E-fermi は DOSCAR から取得する(DOSCARがない場合はOUTCARから)
    # K点情報はバンドの計算のOUTCARが必須
    # E-fermi情報は SCF 計算の DOSCAR(E-fermi が欲しい)
    #
    if not DOS_FLAG:
        if os.path.exists(doscarname) or os.path.exists(doscarname+".gz"):
            class_name ='ReadDoscar'
            optname = doscarname
            print 'EFERMI(DOS):',
        else:
            class_name ='ReadOutcar'
            optname = outcarname
            print 'EFERMI(OUT):',

        module_name = 'StructureAnalysisEnvironment'

        module = __import__(module_name, globals(), locals(), [class_name], -1)
        klass = getattr(module,class_name)

        kinstance = klass(optname)
        efermi = kinstance.get_efermi()
        TITLE = kinstance.get_title()
        print efermi
    else:
        dos = SAE.ReadVaspDoscar(doscarname)
        TITLE = dos.get_title()
        efermi = dos.get_efermi()
        print 'EFERMI(DOS):',
        print efermi

    if not TITLE:
        TITLE='dummy'

    ############################################################################
    # LDOS_ALL 読み込み
    if SPD_FLAG and DOS_FLAG:
       #ldos_all = dos.get_ldos_all()  # LDOS(NEDOS,l,atom,ispin)
        NEDOS = dos.get_nedos()

    ############################################################################
    # sym.dat ファイルをゲットする(K点の自動処理をする前の暫定措置)
    SYMDAT_FLAG=False
    if os.path.exists(symdatname) or os.path.exists(symdatname+".gz"):
        print "SYM.DAT    :", symdatname

        sym = SAE.ReadVaspSymdat(symdatname)
        num_symlines = sym.get_num_symlines()
        symlines = sym.get_symlines()

        for i in range(num_symlines):
            print "  ",symlines[i]

        if num_kpoints_line != num_symlines -1:
            print "STOP: KPONTS lines =",num_kpoints_line
            sys.exit("STOP: sym.dat inconsistence")

        SYMDAT_FLAG=True

    ############################################################################
    # KPOINTS print
    print "KPOINTS"
    for i in range(len(kpoints_array)):
        print " %10.7f %10.7f %10.7f " \
                % ( kpoints_array[i,0],kpoints_array[i,1],kpoints_array[i,2] )
        if not i % 2 == 0:
            print ""

    for i in range(num_kpoints_line):
        print " line %d : %10.7f " % ( i, zone_ratio[i] )


    ############################################################################
    # 最大の固有値と最小の固有値をゲット
    # multi-plot する zone 共通のデフォルト ymin,ymax を作成する
    eigen_min,eigen_max = procar.get_max_eigenval()
    delta = (eigen_max - eigen_min)/20  # 1/20 だけ下限を増やすため
    if ABS_FLAG:
        eigen_max = eigen_max+delta
        eigen_min = eigen_min-delta
    else:
        eigen_max = eigen_max+delta - efermi
        eigen_min = eigen_min-delta - efermi

    ############################################################################
    # matplotlib
#   plt.rcParams['font.family']       = 'Times New Roman'
    plt.rcParams['font.size']         = 14  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize']   = 5   # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']    = 1.5 # 軸の太さを設定。目盛りは変わらない

    orgx = 0.130
    orgy = 0.110

    sizey = 0.80
    sizex0 = 0.80

    sizex_dos = 0.20
    if DOS_FLAG:
        sizex0 = sizex0 - sizex_dos

    ymin0 = 0
    ymax0 = 0

    if NSPIN == 2:
        istart = 0
        iend = 2
        title=TITLE+" both-spin"
    if NSPIN == 1:
        istart = 0
        iend = 1
        title=TITLE+" nonmag"
    if UP_FLAG:
        istart = 0
        iend = 1
        title=TITLE+" majority-spin"
    if DOWN_FLAG:
        istart = 1
        iend = 2
        title=TITLE+" minority-spin"

    if OPT_BAND:
        title = title+"  band= "+str(OPT_BAND)


    for i in range(num_kpoints_line):

        # multi plot の原点と軸の修正
        sizex = zone_ratio[i]*sizex0
        plt.axes([orgx,orgy, sizex, sizey])
        orgx= orgx+sizex


        # X 軸の作成(lines数)
        X = np.zeros(div_kpoints_line)
        for j in range(div_kpoints_line):  # (0) 〜 (div_kpoints_line)
            X[j] = j

        # X軸のticks (gnuplot形式のsym.dat を TeX 形式へ変更
        if SYMDAT_FLAG:
            if i != num_kpoints_line -1:
                if "{/Symbol G}" == symlines[i]:
                    symlines[i] = "\Gamma"      # gnuplot 形式から TeX形式へ
                sym = "$"+str(symlines[i])+"$"  # TeX 出力形式へ
                plt.xticks([0],[sym])
            if i == num_kpoints_line -1:
                if "{/Symbol G}" == symlines[i]:
                    symlines[i] = "\Gamma"        # gnuplot 形式から TeX形式へ
                if "{/Symbol G}" == symlines[i+1]:
                    symlines[i+1] = "\Gamma"      # gnuplot 形式から TeX形式へ
                sym0 = "$"+str(symlines[i])+"$"   # TeX 出力形式へ
                sym1 = "$"+str(symlines[i+1])+"$" # TeX 出力形式へ
                plt.xticks([0,div_kpoints_line-1],(sym0,sym1))

        # Y軸のticks
        if i != 0:
            plt.yticks([])
        if i == 0:
            plt.title(title)
            plt.ylabel("$E - E_{\mathrm{F}}$ [eV]", fontsize=16)

        # バンドの重ね書きプロット
        for ispin in range(istart,iend):
            for iband in range(NBANDS):

                # Y 軸の作成,eigenval(NBANDS,NKPTS,NSPIN), NKPTS の分割プロット
                startx = i*div_kpoints_line
                endx = startx+div_kpoints_line-1
                Y = np.zeros(div_kpoints_line)
                k = 0
                for j in range(startx,endx):
                    if ABS_FLAG:
                        Y[k] = eigenval[iband,j,ispin]
                    else:
                        Y[k] = eigenval[iband,j,ispin] - efermi
                    k += 1

                # SPD_FLAG mode (plot s,p,d lines)
                # pro_spd(lm,atom,NBANDS,NKPTS,NSPIN)
                # s --> red
                # p --> green
                # d --> blue
                if OPT_ATOM:
                    start_atom = int(OPT_ATOM)
                    end_atom = int(OPT_ATOM)+1
                else:
                    start_atom = 0
                    end_atom = NATOM
                if SPD_FLAG:
                    for j in range(startx,endx):
                        for atom in range(start_atom,end_atom):
                            for lm in range(3):
                                ##################################
                                ratio=pro[lm,atom,iband,j,ispin]
                                ##################################
                                rsize=ratio*5

                                if lm == 0:
                                    c='red'
                                elif lm == 1:
                                    c='green'
                                elif lm == 2:
                                    c='blue'
                                else:
                                    c='#cccccc'

                                if ratio != 0:
                                    plt.plot(X,Y,color=c,\
                                            linestyle='None',\
                                            marker='o',\
                                            markersize=rsize,\
                                            markeredgecolor=c,\
                                            markerfacecolor='None',\
                                            alpha=ratio )

                # 線の色の調整
                alpha=1
                if ispin == 0:
                    c='black'
                else:
                    c='red'
                if OPT_BAND:
                    c='black'
                    alpha=0.2
                    if iband == int(OPT_BAND):
                        c='red'
                        alpha=1
                if SPD_FLAG:
                    c='black'
                    alpha=0.2

                if INDEX_FLAG:
                    plt.plot(X,Y)
                elif not LINE_FLAG:
                    plt.plot(X,Y,color=c,\
                            linestyle='None',marker='o',markersize=2, \
                            markeredgecolor=c,markerfacecolor='None',\
                            alpha=alpha )
                else:
                    plt.plot(X,Y,color=c)


                # Y幅の調整
                plt.ylim( ymin=eigen_min, ymax=eigen_max )
                if OPT_EMIN:
                    plt.ylim( ymin=float(OPT_EMIN))
                if OPT_EMAX:
                    plt.ylim( ymax=float(OPT_EMAX))

        ## ispin/band-loop ##
        # X幅の調整
        plt.xlim( xmin=0, xmax=div_kpoints_line-1)

        # Fermi-Level
        if ABS_FLAG:
            plt.axhline(y=efermi, color='blue')
        else:
            plt.axhline(y=0, color='blue')

    ############################################################################
    # DOS plot
    if DOS_FLAG:
        for ispin in range(istart,iend):

            # スピンの有無と SPIN_FLAG による位置修正
            if NSPIN == 2:
                if UP_FLAG or DOWN_FLAG:
                    sizex_dos1 = sizex_dos
                else:
                   sizex_dos1 = sizex_dos/2
            else:
                sizex_dos1 = sizex_dos
            plt.axes([orgx,orgy, sizex_dos1, sizey])
            if UP_FLAG or DOWN_FLAG:
                pass
            else:
                orgx= orgx+sizex_dos1

            ENG = dos.get_eng()
            if not ABS_FLAG:
                ENG = ENG -efermi
            TDOS = dos.get_tdos(ispin)

            c='#cccccc'
            if UP_FLAG or DOWN_FLAG:
                plt.fill_between(TDOS,ENG,color=c,linewidth=2)
            else:
                if ispin == 0:
                    lc='black'
                if ispin == 1:
                    lc='red'
                if SPD_FLAG:
                    lc=c
                plt.fill_between(TDOS,ENG,\
                        color=lc,facecolor=c,linewidth=2)

            if SPD_FLAG:
                for l in range(3):
                    Y = dos.get_tdos_spd(l,ispin)

                    if l == 0:
                        c='red'
                    elif l == 1:
                        c='green'
                    elif l == 2:
                        c='blue'
                    else:
                        c='#cccccc'

                    plt.plot(Y,ENG,color=c)


            # 目盛の調整
            plt.yticks([])
#      #    plt.xticks(range(1,4))
            plt.xticks([])

            # X軸の調整
            plt.xlim( xmin=0 )

            # Y幅の調整(DOS)
            plt.ylim( ymin=eigen_min, ymax=eigen_max )
            if OPT_EMIN: plt.ylim( ymin=float(OPT_EMIN))
            if OPT_EMAX: plt.ylim( ymax=float(OPT_EMAX))

            # Fermi-Level
            if ABS_FLAG:
                plt.axhline(y=efermi, color='blue')
            else:
                plt.axhline(y=0, color='blue')
    ############################################################################

#   plt.subplot(1,num_kpoints_line,1)
#   plt.subplot(1,num_kpoints_line,3)
#   for i in range(num_kpoints_line):
#       print vector[i]
#       plt.subplot(1,num_kpoints_line,i)
#   ax3 = fig.add_subplot(1,num_kpoints_line,3, sharey=ax1)
#   plt.subplots_adjust(wspace=0)
#   plt.subplots_adjust(hspace=0)


#   plt.savefig("ek_band.eps")
#   plt.savefig("ek_band.pdf")
#   plt.savefig("ek_band.png")

    plt.show()

    plt.close('all')

################################################################################
