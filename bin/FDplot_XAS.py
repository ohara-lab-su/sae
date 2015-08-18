#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
#
#   *_conv.txt plot program
#    ファイル名自動判別を付け加えただけの基本的な XAS plot
#
#   fdXAS.py のゴージャス版
#   fdXAS は書き換えるのを前提としたスクリプト(小文字系)
#
#   Kエッジ版
#
#   SPIN 対応版
#    ただし、read_pdb.inp と conv.inp 両対応を意識して、自動判別ではなく
#    -s もしくは --spin オプション時に強制的に対応させる
#    spin の計算で -s をつけていない時は up-spin の DOS を描く
#
#   Weight
#     もしPd19クラスター（つまりPd原子が19個)で、計算したサイトがall-siteで
#     4つならば(サイト内には同種の対称性の複数の原子を含む)
#
#     FDplot_xas.py -a 1 2 3 4 -w 19
#      とプロットすると、４つのサイトの平均値を19で割る(1原子あたり)に
#      変換した XANES をプロットする
#
#    このとき、DOS プロットも一緒にすると DOS のときはサイト情報は
#    そもそもが原子一個あたりなので（サイト内は一個の原子扱い）
#
#       FDplot_xas.py -d -x 4
#       とする(xはDOS weight)
#
#    両方時にプロットするには
#      FDplot_xas.py -a 1 2 3 4 -w 19 -d -x 4
#
################################################################################
#
# 2015.07.06
#   XAS の Weight と DOS の Weight を別に設定可能にした
#
# 2015.07.02
#  spin対応(DOSのプロットでupとdownの併記プロット)
#  その代わりに LDOS のプロットで p軌道のみ出力
#
# 2015.07.01
#  平均化ルーチンで重み(平均する際に割る数)を引数に追加したのを呼び出すように
#
# 2015.07.01
#   average モードで XAS だけではなく DOS も対応(ReadFdmSdの対応化)
#
# 2015.06.30
#   average モードを追加
#    filout 名 + _ + 数字 + _conv.txt
#    ファイルを複数読み込み平均化してプロットするモードを追加
#
# 2015.06.30
#   可変長オプションに変更
#   optparser() --> argparse()
#
# 2015.06.30
#   -i 指定で conv.inp を読み込んで 別途に計算した XAS conv を
#   プロットできるように修正
#
#   このとき、conv.inp ファイル中の conv_out 情報を取得して
#   プロットする名前を獲得できる
#
#   さらにDOS モードの時は
#     conv.inp 中の Filout から *_bav.txt 名を取得して情報を入手がかのう
#
#   つまり、Convolution 名とログファイル名の２つの名前を扱える
#
# 2015.06.24
#  実験データもプロット可能に
#        obs_file = filout+'_obs.txt.nor'
#
# 2015.06.23
#  DOSもプロット可能に
#
# 2015.06.19 FDplot_XAS startup
#
# 2015.05.21 fdXAS startup
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
__version__    = "0.0.1"
################################################################################

import sys
#import gzip
import os
#import re
#import optparse
import argparse
#import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

#from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick


################################################################################
def options():

    name = 'read_pdb.inp'
#   name = 'POSCAR.inp'

#   parser = optparse.OptionParser()
    parser = argparse.ArgumentParser()
    parser.add_argument(  '-i','--input', dest='INPUT',)  # inp ファイル名(自動処理用)
    parser.add_argument(  '-c','--convolution',)          # convolution ファイル名
    parser.add_argument(  '-t','--text',)                 # 元ソースファイル名
    parser.add_argument(  '--emax',)
    parser.add_argument(  '--emin',)
    parser.add_argument(  '--ymax',)
    parser.add_argument(  '--dmax',)
    parser.add_argument(  '-s','--spin', action='store_true',default=False,)
    parser.add_argument(  '-f','--fermi', action='store_true',default=False,)
    parser.add_argument(  '-n','--nonsubtract', action='store_true',default=False,)
    parser.add_argument(  '-b','--broad', action='store_true',default=False,)
    parser.add_argument(  '-d','--dos', action='store_true',default=False,)
    parser.add_argument(  '-o','--obs', action='store_true',default=False,)
    parser.add_argument(  '-a','--absorber', nargs='*')
    parser.add_argument(  '-w','--weight',) # for XAS
    parser.add_argument(  '-x','--dosweight',) # for LDOS
#   options,args = parser.parse_args()
    options = parser.parse_args()

    if options.INPUT: name=options.INPUT
#   if len(args) > 0: name=args[0]

    if not os.path.exists(name):
        name = 'conv.inp'

    return name,options.convolution,options.text,\
            options.emax,options.emin,options.ymax,options.dmax,\
            options.spin,\
            options.fermi,options.nonsubtract,\
            options.broad,options.dos,options.obs,\
            options.absorber,options.weight,options.dosweight

###############################################################################
if __name__ == '__main__':

    inpname,convolname,textname,\
            OPT_EMAX,OPT_EMIN,OPT_YMAX,OPT_DMAX,\
            FLAG_SPIN,\
            FLAG_fermi,FLAG_subt,\
            FLAG_B,FLAG_DOS,FLAG_OBS,AV,WE,WEDOS = options()

    # *.inp から各種情報を読み込む
    if inpname:
        print "INP name        =",inpname

    # *.txt (計算結果のconv前のファイル)
    if textname:
        print "TEXT name       =",textname

    # 直接 *_conv.txt を指定して表示する機能
    if convolname:
        print "Convolution file=",convolname

    if OPT_EMAX:
        OPT_EMAX=float(OPT_EMAX)
        print "Emax             =",OPT_EMAX
    if OPT_EMIN:
        OPT_EMIN=float(OPT_EMIN)
        print "Emin             =",OPT_EMIN
    if OPT_YMAX:
        OPT_YMAX=float(OPT_YMAX)
        print "Ymax             =",OPT_YMAX
    if OPT_DMAX:
        OPT_DMAX=float(OPT_DMAX)
        print "Ymax(DOS)        =",OPT_DMAX
    if FLAG_SPIN:
        print "Enforce spin=2 mode"

    if WE:
        WE=float(WE)
        print "Weight           =",WE
    if WEDOS:
        WEDOW=float(WEDOS)
        print "Weight for LDOS  =",WEDOS

#   eng = conv.get_eng()
#   xas = conv.get_xas()

    plt.rcParams['font.family']     = 'Times New Roman'
    plt.rcParams['font.size']       = 16  # ラベル等のフォントサイズ
    plt.rcParams['legend.fontsize'] = 14  # レジェンドのフォントサイズ
    plt.rcParams['axes.linewidth']  = 1.5 # 軸の太さを設定。目盛りは変わらない

#   plt.figure(figsize=(7.00, 9.89))  # for portrait
    plt.figure(figsize=(8.10, 9.89))  # for portrait

#   orgx = 0.170
#   orgy = 0.080
#   off = 0.010
#   xsize = 0.75
#   ysize = 0.83/2.
#   plt.axes([orgx,orgy,xsize,ysize])


    ############################################################################
    inp = SAE.ReadFdmInp(inpname)

    calculation = inp.get_calculation()
    if calculation:
        filout = calculation.replace('.txt','')
    else:
        filout = inp.get_filout()


    ## 計算結果の読み込み (平均化モード のときは最初に指定したabsorberから)
    if convolname:
        cn = convolname
    else:
        cn = filout

    if textname:
        tn = textname
    else:
        tn = filout

    txt = SAE.ReadFdm(tn,'.txt')  # Read Edge and Efermi
    conv = SAE.ReadFdmConv(cn,'_conv.txt')

    if AV:
        txt = SAE.ReadFdm(filout+'_'+str(AV[0]),'.txt')
        conv = SAE.ReadFdmConv(filout+'_'+str(AV[0]),'_conv.txt')

    ############################################################################
    # 平均化モードのとき txt インスタンスの結果を上書き(平均の結果にする)
    # 平均化モードの時に filbav 名を取得
    if AV:
        try:
            filbav = inp.get_filout()
        except:
            if filbav is None:
                sys.exit("STOP: filout TAG not found in "+inpname)

        print "--- average mode "
        if WE:
            conv.xas = conv.average_conv(filbav,AV,weight=WE)
        else:
            conv.xas = conv.average_conv(filbav,AV)

    ############################################################################
    ## *_0_conv.txt ファイルへ結果出力
    if AV:
        try:
            outav = open(filbav+'_'+str(0)+'_conv.txt','w')
            print >> outav, ""
            for i in range(len(conv.eng)):
                print >> outav, "  %14.8f %14.8f" %(conv.eng[i],conv.xas[i])
        except:
            outav.close()


    ############################################################################
    # DOS モードで fileout TAG から元の計算のログファイル名を入手
    if FLAG_DOS:
        try:
            filbav = filbav
        except:
            filbav = inp.get_filout()
            if filbav is None:
                sys.exit("STOP: filout TAG not found in "+inpname)

        if AV:
            if WEDOS:
                sd = SAE.ReadFdmSd(filout,suffix='_sd0.txt',\
                        bavname=filbav,inpname=inpname,absorber=AV,weight=WEDOS)
            elif WE:
                sd = SAE.ReadFdmSd(filout,suffix='_sd0.txt',\
                        bavname=filbav,inpname=inpname,absorber=AV,weight=WE)
            else:
                sd = SAE.ReadFdmSd(filout,suffix='_sd0.txt',\
                        bavname=filbav,inpname=inpname,absorber=AV)
        else:
            sd = SAE.ReadFdmSd(filout,suffix='_sd0.txt',\
                    bavname=filbav,inpname=inpname)

    if AV: print ""
    print "INP FILE           = ",inpname," (.inp)"
    print "DATA FILE (filout) = ",filout, " (.txt)"
    try:
        filbav = filbav
        print "BAV FILE  (filout) = ",filbav, " (_bav.txt)"
    except:
        pass

    print "-------------------"
    print "E_edge   =",txt.E_edge
    print "E_fermi  =",txt.E_Fermi


    ############################################################################
    # XASエネルギー原点の変換 (*.txt ファイルおよび *_conv.txt 読み込み)
    if not FLAG_subt:

        # PhotoEnegy モードで計算した時と同じ結果を返す
        if not inp.get_energygpho() and not FLAG_fermi:
            print "current mode is Fermi"
            print "---> convert to PhotoEnergy"
            print "     + E_edge"
            txt.eng = txt.eng + txt.E_edge
            conv.eng = conv.eng  + txt.E_edge

        # E_fermi を引く(A) : A=B
        if not inp.get_energygpho() and FLAG_fermi:
            print "current mode is Fermi"
            print "---> subtract E_fermi"
            print "     - E_fermi"
            txt.eng = txt.eng - txt.E_Fermi
            conv.eng = conv.eng - txt.E_Fermi

        # E_fermi を引く(B) : A=B
        if inp.get_energygpho() and FLAG_fermi:
            print "current mode is PhotoEnergy"
            print "---> convert to EF0 mode"
            print "     - E_edge - E_fermi"
            txt.eng = txt.eng - txt.E_Fermi - txt.E_edge
            conv.eng = conv.eng - txt.E_Fermi - txt.E_edge


    ############################################################################
    ## XAS plot
    if FLAG_DOS:
        plt.subplot(3,1,2)
    else:
#       plt.subplot()
        plt.subplot(2,1,2)

    if not FLAG_B:
        plt.plot(txt.eng,txt.xas,color='green',linewidth=1,label='XAS')
    plt.plot(conv.eng,conv.xas,color='red',linewidth=3,label='XAS broad')

    plt.ticklabel_format(axis='x',useOffset=False)
#   plt.ticklabel_format(axis='x',style='plain')

#   if FLAG_fermi:
#       plt.xlabel("Energy above Fermi [eV]")
#   else:
#       plt.xlabel("Photon Energy [eV]")
    plt.ylabel("Absorption [arb. unit]")

    EF0 =txt.E_edge + txt.E_fermi
    if not FLAG_subt:
        if FLAG_fermi:
            plt.axvline(x=0,color='black',linewidth=1)
        else:
            plt.axvline(x=EF0,color='black',linewidth=1)


#   leg = plt.legend(fontsize=12,loc='lower right')
    leg = plt.legend(loc='lower right')
    leg.get_frame().set_alpha(0.5)

    if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX))
    if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN))
    if OPT_YMAX: plt.ylim( ymax=float(OPT_YMAX))

    xas_xmin,xas_xmax,xas_ymin,xas_ymax = plt.axis()

    ############################################################################
    ## DOS plot
    if FLAG_DOS:
        plt.subplot(3,1,3)

        dos_p = sd.get_ldos(l='p')
        plt.plot(conv.eng,dos_p,linewidth=1,label='absorber-LDOS(p)')
        plt.ticklabel_format(axis='x',useOffset=False)

        if not FLAG_SPIN:
            dos_s = sd.get_ldos(l='s')
            plt.plot(conv.eng,dos_s,linewidth=1,label='absorber-LDOS(s)')
            plt.ticklabel_format(axis='x',useOffset=False)
        else:
            dos_s = sd.get_ldos(l='p',spin='up')
            plt.plot(conv.eng,dos_s,linewidth=1,label='absorber-LDOS(p)  up')
            dos_s = sd.get_ldos(l='p',spin='down')
            plt.plot(conv.eng,dos_s,linewidth=1,label='absorber-LDOS(p)  down')
            plt.ticklabel_format(axis='x',useOffset=False)

        plt.ylabel("DOS [stat/eV]")
        if not FLAG_subt:
            if FLAG_fermi:
                plt.axvline(x=0,color='black',linewidth=1)
            else:
                plt.axvline(x=EF0,color='black',linewidth=1)

    #   leg = plt.legend(fontsize=12,loc='lower right')
        leg = plt.legend(loc='upper right')
        leg.get_frame().set_alpha(0.5)

        if OPT_EMAX: plt.xlim( xmax=float(OPT_EMAX))
        if OPT_EMIN: plt.xlim( xmin=float(OPT_EMIN))
        if OPT_DMAX: plt.ylim( ymax=float(OPT_DMAX))

    if FLAG_fermi:
        plt.xlabel("Energy above Fermi [eV]")
    else:
        plt.xlabel("Photon Energy [eV]")

    ############################################################################
    # Athena data plot
    if FLAG_OBS:
        obs_file = filout+'_obs.txt.nor'
        if not os.path.exists(obs_file):
            sys.exit("STOP: "+obs_file+" not found")

        nor = SAE.ReadAthenaNor(obs_file)
        if FLAG_DOS:
            plt.subplot(3,1,1)
        else:
            plt.subplot(2,1,1)

        plt.plot(nor.eng,nor.nor,label='obs.')
        plt.xlim([xas_xmin,xas_xmax])
        plt.ticklabel_format(axis='x',useOffset=False)

    #   leg = plt.legend(fontsize=12,loc='lower right')
    #   leg = plt.legend(loc='upper right')
        leg = plt.legend(loc='lower right')
        leg.get_frame().set_alpha(0.5)

    ############################################################################

    plt.savefig("XAS.eps")
    plt.savefig("XAS.pdf")
    plt.savefig("XAS.png")

    plt.show()

    plt.close('all')

#   print "NAME",name


