#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# OpenMX 用 dat ファイル出力 関数
#
# 基本的な構造変換に必要な情報
#      +
#  オプショナルでEDIFFなどの設定項目:オプショナル項目は (デフォ-> None)
#      +
#  OpenMX の擬波動関数および擬ポテンシャルの自動設定
#
#
#  実行にはPAO と VPS の情報一覧を必須とする (ReadMxVps.py, ReadMxVpsList.py)
#
#    情報一覧ファイル: openmx_defaults_vpsdata.list
#       1) カレントをサーチ
#       2) ホーム直下の DFT_DATA13 ディレクトリをサーチ
#       3) ../DFT_DATA13 ディレクトリをサーチ
#       4) ~/openmx1/ ディレクトリをサーチ
#
#    vpsdata ファイルを発見したら読み込む
#    vapdata ファイルの中身は PAO の軌道情報および VPS 情報で
#    元素記号から最低限動くデフォルトの PAO/VPS 情報を引っ張るために用いる
#
################################################################################
#
# 2015.08.20
#  関数化&統合クラス統合化前のバージョンコメント
#
# 2015.06.30
#  == None --> is None
#
# 2016.06.19
#  simple_v1 へと古いバージョンをブランチ(実質バックアップ)
#   今後の master 版は INCAR や KPOINTS や OUTCAR などを読み込んで
#   なるべくそのまま VASP の計算と同じ条件になる *.dat を自動作成する
#   方向性へゴージャスにする
#
# 2015.02.27
#
#   hexagonal 系でのバグ (cubic では基本並進は対象なのでこの問題発生しない)
#
#     1) ライブラリ化をしたときに基本並進ベクトルを表示する部分で
#        行列を転地して表示していたミス
#
#   cartesina モードでのバグ(FRACはダイレクトなのでこの問題が発生しなかった)
#
#     2) OpenMX の cartesian モードは scale=1.0 でさらに内部座標を基本並進で
#        再スケールする必要がある
#
# 2015.02.27
#
#  変換系の部分を conv_direct2car 関数を再利用
#  *) 戻り値版として作りなおした
#
#   conv_scale21r        (scaleファクターを1.0にする-->基本並進に押し付ける)
#   conv_direct2car1     (内部座標をスケールしない VASP の意味での Car 座標)
#   conv_direct2carABS1  (絶対値版,一般的な意味での Car 座標化)
#
#   --> それぞ戻り値版とした
#
# 2015.02.27
#  変換バグ発覚、再チェック
#   1) IGZO (sc) vasp direct    --> dat [OK]
#   2) IGZO (sc) vasp cartesian --> dat [OK]
#   3) Cu   (fcc) vasp direct   --> dat [OK]
#   4) graphene (hex) vasp direct   --> dat [Error]
#
# 2015.02.27
#  入力拡張子の自動判別ルーチン追加
#
#  -o オプションでのファイル名入力で *.dat 拡張子を付けたいた時は
#  内部的には自動で拡張子を落とすようにする（最終的な出力は拡張子有り）
#  ただし、オプション無しの引数でファイル名を指定した時はファイル名の
#  自動削除なしで、そのまま処理する
#
# 2015.02.24
#   基本並進ベクトルに scale factor がかかってなかったので修正
#   OpenMX は scale factor は transition vector 内部にかかっている
#
# 2015.02.24
#   -o オプション追加
#
# 2015.02.24
#  ReadPoscar.get_fix() が numpy オブジェクトでキャラクター指定で作っていた
#  のに合わせて print する時の出力を %s に変更しなおした。（変更忘れていた)
#   ---> この変更そのものがミス
#         VASP の F と T 形式での出力をやめて OpenMX の 1 0 形式の出力へ
#         変更した
#
# 2015.02.24
#   vasp のバージョンチェックの位置を変更(いままでだと意味をなしてなかった)
#
# 2015.02.18
#   get_position() の引数を変更していたのを忘れていたので
#   get_fix() と get_position() に分離
#
# 2015.02.10
#
#  全面的に改修
#
#    0) POSCAR 読み込みを直接実行から ReadPoscar クラス呼び出しへ変更
#
#    1) VPS and PAO リスト一覧からそれぞれの情報をゲットするクラス呼び出し
#
#    2) 元素名から valence.electron の数を VPS ファイルから読み取り、出力する
#       デフォルトポテンシャルは PBE で DFT_DATA13 とする
#       non-mag 版
#
#    3) 元素名から PAO ファイル一覧を取得
#        その中の中間のカットオフ長のファイルをチョイスする形で一応ジェネレート
#        する
#
# 2014.06.20
#   based on Vdirect2car.pl (and ReadPOSCAR.py)
#
################################################################################
__author__     = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__    = ["Kengo NAKADA"]
__email__      = "kengo.nakada@gmail.com"
__copyright__  = "Copyright 2014,2015, Kengo NAKADA"
__license__    = "MIT"
#
__status__     = "alpha"
__version__    = "0.1.0"
################################################################################

#import optparse
import sys
import os
import re
import numpy as np

#import glob
import StructureAnalysisEnvironment as SAEnv
#import SpaceGroupEnvironment as SGE

################################################################################
#
#  using ReadMxVps.py and ReadMxVpsList.py
#
def print_mx_dat(datname,STD,\
        title,scale,natom,nion,selective,direct,vasp_version,\
        t,atoms,atoms_index,position,fix,\
        atoms_index_j,\
        NSW=None,\
        NELM=None,\
        IBRION=None,\
        EDIFF=None,\
        EDIFFG=None,\
        KP=None,\
        FRAC=True):

    if vasp_version is None : vasp_version = 5

    if KP:
        kx = KP[0:0]
        ky = KP[0:1]
        kz = KP[0:2]

    ############################################################################
    ## OpenMX Version チェック & DATAPATH 環境変数の確認
    ##
    version_FLAG=False
    if sys.version_info[0] >= 2 and sys.version_info[1] >= 7:
         version_FLAG=True

    DATAPATH=os.environ.get('OPENMXDATAPATH', "")
    if not DATAPATH:
        print "can't found OPENMXDATAPATH environment on yuur system"
        print "please export OPENMXDATAPATH=~/DFT_DATA13"
        print "STOP"
        sys.exit()

    ############################################################################
    ## データーファイルパスとデフォルトPAO/VPS 情報のセット
    ##
    VPSLIST = 'openmx_defaults_vpsdata.list'
    DFT_DATA = 'DFT_DATA13'

    data = '../'+DFT_DATA
    pot = 'PBE'
    ver = '13'

    # ../DFT_DATA が存在しない時は 環境変数 DATAPATH を選択
    if not os.path.exists(data):
        data = DATAPATH
    print "DATA PATH ",data


    # VPS 及び PAO のパス設定
    vpspath = data+'/VPS/'
    paopath = data+'/PAO/'


    ############################################################################
    ## VPSLIST のファイル場所確認
    ##   元素記号からPAOとVPS情報を取り出すためのリストの存在している場所探し
    ##
    HOMEPATH=os.environ.get('HOME',"")
    if os.path.exists(VPSLIST):
        vpslistpath = VPSLIST
    elif os.path.exists(data+'/'+VPSLIST):
        vpslistpath = data+'/'+VPSLIST
    elif os.path.exists(HOMEPATH+'/'+DFT_DATA+'/'+VPSLIST):
        vpslistpath = HOMEPATH+'/openmx2/'+DFT_DATA+'/'+VPSLIST
    elif os.path.exists(HOMEPATH+'/openmx1/'+VPSLIST):
        vpslistpath = HOMEPATH+'/openmx1/'+VPSLIST
    else:
        sys.exit("STOP: "+VPSLIST+" file not found")


    ############################################################################
    ## OpenMX(*.dat) 出力ファイル名をセット
    ##
    OUT=datname
    datfile = open(OUT+'.dat','w')

    if not STD:
        sys.stdout = datfile

    ############################################################################
    ## 座標系を Cartesian に変換
    ##    (non FRAC モードは Cartesian, 対してFRAC はdirect-mode
    ##
   #if direct and not OPT_FRAC:
   #    car_x = np.zeros(natom)
   #    car_y = np.zeros(natom)
   #    car_z = np.zeros(natom)
   #    for i in range(natom):
   #        car_x[i] = t[0][0]*position[i][0] + t[1][0]*position[i][1] + t[2][0]*position[i][2]
   #        car_y[i] = t[0][1]*position[i][0] + t[1][1]*position[i][1] + t[2][1]*position[i][2]
   #        car_z[i] = t[0][2]*position[i][0] + t[1][2]*position[i][1] + t[2][2]*position[i][2]
   #
   #        position[i][0]=car_x[i]
   #        position[i][1]=car_y[i]
   #        position[i][2]=car_z[i]

    if direct and not FRAC:
        scale,t,natom,direct,position = \
                SAEnv.conv_direct2carABS(scale,t,natom,direct,position)

    # scale factor を1に変更(内部座標もスケール)
    scale,t,natom,direct,position = \
            SAEnv.conv_scale21(scale,t,natom,direct,position)

    ############################################################################
    # VPS と PAO の情報リストのインスタンス生成
    vpslist = SAEnv.ReadMxVpsList(vpslistpath)


    ############################################################################
    # VPS の情報から valence electron の電子数をゲットする
    #   1) potential と database のバージョン から類推する
    #   2) ファイルが存在しない時は S (soft) , H (hard) を仮定してみる
    #
    electron = np.zeros(natom)
    for j in range(natom):

        num,symbol,cutoff,vps_orbit = vpslist.get_vps_name(atoms_index_j[j])
        opt = re.sub(r'[0-9\.]+','',cutoff) # cutoff 名から英数文字のみ取り出す
        fullname = vpspath+symbol+'_'+pot+ver+opt+'.vps'

       #fullname = vpspath+atoms_index_j[i]+'_'+pot+ver+'.vps'
       #if not os.path.exists(fullname):
       #    SUFFIX='S'
       #    if not os.path.exists(fullname):
       #        SUFFIX='H'
       #    fullname = vpspath+atoms_index_j[i]+'_'+pot+ver+SUFFIX+'.vps'
       #    if not os.path.exists(fullname):
       #        sys.exit("STOP: VPS file not found")

        vpsfile = SAEnv.ReadMxVps(fullname)
        electron[j] = vpsfile.get_valence_electron() / 2.0 # 初期なので非磁性を仮定


    ############################################################################
    ## output OpenMX *.dat file
    ##

    print "###########################################"
    print "# File Name"
    print "###########################################"
    print ""
    print "System.CurrentDirectory            ./   # default=./"
    print "System.Name                       ",title
    print "level.of.stdout                    1    # default=1 (1-3)"
    print "level.of.fileout                   1    # default=1 (0-2)"
    print "DATA.PATH                        "+data


    ################################################
    print ""
    print "###########################################"
    print "# Definition of Atomic Species"
    print "#    name PAO VPS"
    print "#    Cu   Cu6.0S-s3p3d3 Cu_PBE13S"
    print "###########################################"
    print ""
    print "Species.Number", nion
    print "<Definition.of.Atomic.Species"

    for i in range(nion):

        atom = re.sub('_.*','',atoms_index[i])
        atoms_index[i]=atom

        ## VPS と PAO の情報リストから PAO と VPS の情報ゲット
        num,symbol,cutoff,vps_orbit = vpslist.get_vps_name(atoms_index[i])
        opt = re.sub(r'[0-9\.]+','',cutoff) # cutoff 名から英数文字のみ取り出す

        vps_name = symbol+cutoff+'-'+vps_orbit
        vps_file = vpspath+symbol+'_'+pot+ver+opt+'.vps'
        pao_file = paopath+symbol+cutoff+'.pao'

        if not os.path.exists(pao_file):
            sys.exit("STOP: "+pao_file+" not found")
        if not os.path.exists(vps_file):
            sys.exit("STOP: "+vps_file+" not found")

        vps0 = symbol+cutoff+'-'+vps_orbit
        pao0 = symbol+'_'+pot+ver+opt
        print "  %2s  %13s  %13s " %( symbol, vps0, pao0 )

    print "Definition.of.Atomic.Species>"


    ################################################
    print ""
    print "#<Hubbard.U.values                 #  eV"
    print "# Ni  1s 0.0 2s 0.0 1p 0.0 2p 0.0 1d 4.0 2d 0.0"
    print "# O   1s 0.0 2s 0.0 1p 0.0 2p 0.0 1d 0.0"
    print "#Hubbard.U.values>"


    ################################################
    print ""
    print "###########################################"
    print "# Atom"
    print "#    num, name, x,y,z,  up-spin, down-spin"
    print "###########################################"
    print ""

    print "Atoms.Number",natom
    if FRAC:
        print "Atoms.SpeciesAndCoordinates.Unit  FRAC  # Ang|AU|FRAC"
        print "<Atoms.SpeciesAndCoordinates            # Unit=FRAC"
    else:
        print "Atoms.SpeciesAndCoordinates.Unit  Ang   # Ang|AU|FRAC"
        print "<Atoms.SpeciesAndCoordinates            # Unit=Ang."

    for i in range(natom):
        atom = re.sub('_.*','',atoms_index_j[i])
        atoms_index_j[i]=atom

        if not version_FLAG:
            print "%4d  %2s %12.8f %12.8f %12.8f  %12.8f  %12.8f " \
                   %(i+1, atoms_index_j[i], \
                   position[i][0],position[i][1],position[i][2],\
                   electron[i], electron[i])
        else:
            myStr = "{:>4}  {:^2} {:12f}  {:12f}  {:12f}   {:12f}  {:12f}"
            print myStr.format(i+1, atoms_index_j[i], \
                    position[i][0],position[i][1],position[i][2],\
                    electron[i], electron[i])

    print "Atoms.SpeciesAndCoordinates>"

    print "Atoms.UnitVectors.Unit            Ang   # Ang|AU"
    print "<Atoms.UnitVectors                      # Unit=Ang."
    print "   %12.8f %12.8f %12.8f" %(t[0][0], t[1][0], t[2][0])
    print "   %12.8f %12.8f %12.8f" %(t[0][1], t[1][1], t[2][1])
    print "   %12.8f %12.8f %12.8f" %(t[0][2], t[1][2], t[2][2])

    print "Atoms.UnitVectors>"


    ################################################
    print ""
    print "###########################################"
    print "# SCF or Electronic System"
    print "###########################################"
    print ""

    print "#scf.restart                On"
    print ""

    print "scf.XcType                 GGA-PBE     # LDA|LSDA-CA|LSDA-PW|GGA-PBE"
    print "scf.SpinPolarization       Off         # On|Off|NC"
    print "#scf.SpinOrbit.Coupling     Off         # On|Off"
    print "scf.ElectronicTemperature  300.0       # default=300 (K)"
    print ""
    print "scf.energycutoff           150.0       # default=150 (Ry)"
    print "#scf.Ngrid                  18 18 18    # Ngrid or scf.energycutoff"
    print "#scf.fixed.grid             12 12 12"
    print ""
    print "scf.EigenvalueSolver       band        # DC|Krylov|ON2|Cluster|Band"

    ################################################
    if not KP:
        KP = np.zeros((1,3))
        KP[0,0] = 12
        KP[0,1] = 12
        KP[0,2] = 12
    print "scf.Kgrid                 "\
            +str(int(KP[0,0]))+" "+str(int(KP[0,1]))+" "+str(int(KP[0,2]))+\
            "     # means 4x4x4"
    ################################################

    print "scf.Generation.Kpoint     regular      # regular|MP"
    print ""

    ################################################
    EDIFF = EDIFF if 'EDIFF' in locals() else 1.0e-6
    print "scf.criterion             "+str(EDIFF)+"       # default=1.0e-6 (Hartree) "
    ################################################

    print "scf.lapack.dste            dstevx      # dstegr|dstedc|dstevx, default=dstevx"
    print ""
    print "scf.Mixing.Type           rmm-diisk    # Simple|Rmm-Diis|Gr-Pulay|Kerker|Rmm-Diisk"
    print "scf.Init.Mixing.Weight     0.30        # default=0.30 "
    print "scf.Mixing.History          5          # default=5"
    print ""
    print "# on-the-fly ( using ./case_SCF_keywords files"
    print ""

    ################################################
    NELM = NELM if 'NELM' in locals() else 40
    print "scf.maxIter                 "+str(NELM)+"         # default=40"
    ################################################

    print "scf.Min.Mixing.Weight      0.001       # default=0.001 "
    print "scf.Max.Mixing.Weight      0.400       # default=0.40 "
    print "#scf.Kerker.factor"
    print "scf.Mixing.StartPulay       6          # default=6"


    ################################################
    print ""
    print "###########################################"
    print "# 1D FFT"
    print "###########################################"
    print ""

    print "#1DFFT.NumGridK             900         # default=900"
    print "#1DFFT.NumGridR             900         # default=900"
    print "#1DFFT.EnergyCutoff        3600.0       # default=3600 (Ry)"


    ################################################
    print ""
    print "###########################################"
    print "# Orbital Optimization"
    print "###########################################"
    print ""

    print "#orbitalOpt.Method           Off        # Off|Unrestricted|Restricted|species"
    print "#orbitalOpt.Opt.Method       EF         # DIIS|EF"
    print "#orbitalOpt.SD.step        0.001        # default=0.001"
    print "#orbitalOpt.HistoryPulay     30         # default=15"
    print "#orbitalOpt.StartPulay       10         # default=1"
    print "#orbitalOpt.InitCoes     Symmetrical    # Symmetrical|Free"
    print "#orbitalOpt.initPrefactor   0.1         # default=0.1"
    print "#orbitalOpt.scf.maxIter      12         # default=12"
    print "#orbitalOpt.MD.maxIter        2         # default=5"
    print "#orbitalOpt.per.MDIter        2         # default=1000000"
    print ""
    print "#orbitalOpt.criterion      1.0e-4       # default=1.0e-4 (Hartree/borh)"
    print ""
    print "#CntOrb.fileout               off       # on|off, default=off"
    print "#Num.CntOrb.Atoms              1        # default=1"
    print "#<Atoms.Cont.Orbitals"
    print "# 1"
    print "#Atoms.Cont.Orbitals>"


    ################################################
    print ""
    print "###########################################"
    print "# SCF Order-N"
    print "###########################################"
    print ""

    print "#orderN.HoppingRanges        7.0        # default=5.0 (Ang) "
    print "#orderN.NumHoppings           2         # default=2"


    ################################################
    print ""
    print "###########################################"
    print "# MD or Geometry Optimization"
    print "###########################################"
    print ""

    ################################################
    #print "MD.Type                   nomd         # Nomd|Opt|NVE|NVT_VS|NVT_NH or EvsLC"
    print "# Nomd|Opt|DIIS|BFGS|RF|EF, MD( NVE|NVT_VS|NVT_NH ) or EvsLC"
    NSW = NSW if 'NSW' in locals() else 0
    if NSW == 0:
        print "MD.Type                   nomd"
    else:
        IBRION = IBRION if 'IBRION' in locals() else 2
        if IBRION != 0:
            print "MD.Type                   Opt"
    ################################################

    print ""
    print "#MD.EvsLC.Step             0.4         # default=0.4%"
    print "#MD.EvsLC.flag            1 1 1        # a,b,c, default=1 1 1"
    print ""
    print "MD.Opt.DIIS.History         3          # default=3"
    print "MD.Opt.StartDIIS           20          # default=3"
    print "MD.Opt.EveryDIIS           200         # default=200"
    print ""

    ################################################
    if NSW > 0:
        print "MD.maxIter                 "+str(NSW)+"        # default=1 (only MD=1)"
    else:
        print "MD.maxIter                 1       # default=1 (only MD=1)"
    ################################################

    print "MD.TimeStep                1.0         # default=0.5 (fs)"

    ################################################
    EDIFFG = EDIFFG if 'EDIFFG' in locals() else EDIFF*10.
    print "MD.Opt.criterion          "+str(EDIFFG)+"       # default=1.0e-4 (Hartree/bohr)"
    ################################################

    print "MD.Opt.DIIS_Mixing         0.5         # default=0.5"
    print ""
    print "scf.ExtCharge.History       2          # default=2"

    print "#<MD>TempControl"
    print "#2"
    print "#100   2   5500.0 0.0"
    print "#600  50    300.0 0.4"
    print "#MD.TempControl>"

    if selective:
        print ""
        print "###########################################"
        print "# MD.Fixed.XYZ"
        print "###########################################"
        print ""

        print "<MD.Fixed.XYZ"
        for i in range(natom):
            if fix[i][0] == 'F':
                fix_x = 1 # fix
            else:
                fix_x = 0 # non fix

            if fix[i][1] == 'F':
                fix_y = 1 # fix
            else:
                fix_y = 0 # non fix

            if fix[i][2] == 'F':
                fix_z = 1 # fix
            else:
                fix_z = 0 # non fix

            print "  %d  %d %d %d" %(i+1,fix_x,fix_y,fix_z)
        print "MD.Fixed.XYZ>"


    ################################################
    print ""
    print "###########################################"
    print "# Band dispersion"
    print "###########################################"
    print ""

    print "#Band.dispersion              on        # on|off, default=off"
    print "#<Band.KPath.UnitCell"
    print "#3.56  0.00  0.00"
    print "#0.00  3.56  0.00"
    print "#0.00  0.00  3.56"
    print "#Band.KPath.UnitCell>"
    print "## if <Band.KPath.UnitCell does not exist,"
    print "##     the reciprical lattice vector is employed. "
    print "#Band.Nkpath                5"
    print "#<Band.kpath"
    print "#   25  0.0 0.0 0.0   1.0 0.0 0.0   g X"
    print "#   25  1.0 0.0 0.0   1.0 0.5 0.0   X W"
    print "#   25  1.0 0.5 0.0   0.5 0.5 0.5   W L"
    print "#   25  0.5 0.5 0.5   0.0 0.0 0.0   L g"
    print "#   25  0.0 0.0 0.0   1.0 0.0 0.0   g X"
    print "#Band.kpath>"

    ################################################
    print ""
    print "###########################################"
    print "# MO output"
    print "###########################################"
    print ""

    print "#MO.fileout                       off   # on|off"
    print "#num.HOMOs                         1    # default=2"
    print "#num.LUMOs                         1    # default=2"
    print "#MO.Nkpoint                        2    # default=1 "
    print "#<MO.kpoint"
    print "#  0.0  0.0  0.0"
    print "#  0.0  0.0  0.2"
    print "#MO.kpoint>"

    ################################################
    print ""
    print "###########################################"
    print "# DOS and PDOS"
    print "###########################################"
    print ""

    print "Dos.fileout                  on        # on|off, default=off"
    print "Dos.Erange              -20.0  10.0    # default = -20 20 "
    print "#Dos.Kgrid                12 12 12     # default = Kgrid1 Kgrid2 Kgrid3"
    print ""
    print "#DosGauss.fileout             on        # default=off, on|off"
    print "#DosGauss.Num.Mesh           200        # default=200"
    print "#DosGauss.Width              0.2        # default=0.2 (eV)"


    ################################################
    print ""
    print "###########################################"
    print "# output Hamiltonian and overlap (for Developer)"
    print "###########################################"
    print ""
    print "#HS.fileout               off    # on|off, default=off"


    ################################################
    print ""
    print "###########################################"
    print "# Electric Field"
    print "###########################################"
    print ""
    print "#scf.Electric.Field"


    ################################################
    print ""
    print "###########################################"
    print "# Charge Dorping"
    print "###########################################"
    print ""
    print "#scf.system.charge         1.0   # default=0.0"


    ################################################
    print "###########################################"
    print "# ESM (Effective Screening Medium)"
    print "###########################################"
    print "#ESM.switch                   on3      # off, on1=v|v|v, on2=m|v|m, on3=v|v|m, on4=on2+EF"
    print "#ESM.potential.difference     0.0      # default=0.0 (eV)"
    print ""
    print "#ESM.wall.switch              off"
    print "#ESM.wall.position            6.0      # default=10.0 (ang)"
    print "#ESM.wall.height            100.0      # default=100.0 (eV)"
    print ""
    print "#ESM.buffer.range             4.5      # default=10.0 (ang)"
    print ""


    ################################################
    print "###########################################"
    print "# Wannier Function"
    print "###########################################"
    print ""

    print "#Wannier.Func.Calc        on"
    print "#Wannier.Func.Num          4"
    print "#Wannier.Outer.Window.Bottom -14.0"
    print "#Wannier.Outer.Window.Top     0.0"
    print "#Wannier.Inner.Window.Bottom   0.0"
    print "#Wannier.Inner.Window.Top       0.0"
    print "#Wannier.Initial.Guess         on"
    print "#Wannier.Initial.Projectors.Unit FRAC     # AU, ANG or FRAC "

    print "##proj-sp3 0.25 0.25 0.25 0.0 0.0 -1.0  -1.0 0.0 0.0"
    print "#"
    print "#<Wannier.Initial.Projectors"
    print "#proj-s 0.125 0.125 0.125 0.0 0.0 1.0  1.0 0.0 0.0"
    print "#proj-s -0.375 0.125 0.125 0.0 0.0 1.0 1.0 0.0 0.0"
    print "#proj-s 0.125 -0.375 0.125 0.0 0.0 1.0 1.0 0.0 0.0"
    print "#proj-s 0.125 0.125 -0.375 0.0 0.0 1.0 1.0 0.0 0.0"
    print "#Wannier.Initial.Projectors>"
    print "#"
    print "## Si1-s  1.275 1.275 1.275  0.0 0.0 1.0    1.0 0.0 0.0 "
    print "## Si1-s  -1.275 -1.275 1.275 0.0 0.0 1.0    1.0 0.0 0.0 "
    print "## Si1-s  -1.275 1.275 -1.275 0.0 0.0 1.0    1.0 0.0 0.0 "
    print "## Si1-s  1.275 -1.275 -1.275 0.0 0.0 1.0    1.0 0.0 0.0 "
    print "#Wannier.Kgrid   8 8 8"
    print "#Wannier.MaxShells   12"
    print "#"
    print "#Wannier.Interpolated.Bands              on   # on|off, default=off "
    print "#"
    print "#Wannier.Function.Plot                   on   # on|off, default=off"
    print "#Wannier.Function.Plot.SuperCells     1 1 1   # default=0 0 0"
    print "#"
    print "#Wannier.Dis.Mixing.Para     0.5"
    print "#Wannier.Dis.Conv.Criterion    1e-12"
    print "#Wannier.Dis.SCF.Max.Steps    200"
    print "#"
    print "#Wannier.Minimizing.Max.Steps    100"
    print "#Wannier.Minimizing.Scheme     2"
    print "#Wannier.Minimizing.StepLength  2.0"
    print "#Wannier.Minimizing.Secant.Steps         5"
    print "#Wannier.Minimizing.Secant.StepLength    2.0"
    print "#Wannier.Minimizing.Conv.Criterion        1e-10"
    print "#"
    print "#"
    print "#Wannier.Readin.Overlap.Matrix            off"
    print ""
    print ""

    if not STD:
        datfile.close()
        sys.stdout = sys.__stdout__

################################################################################
if __name__ == '__main__':

    import optparse
    poscarname = 'POSCAR'
    datname    = 'POSCAR'
    parser = optparse.OptionParser(os.getcwd())
    parser = optparse.OptionParser()
    parser.add_option( '-s','--stdout', action='store_true',)
    parser.add_option( '-i','--input', dest='INPUT',)
    parser.add_option( '-o','--output', dest='OUTPUT',)
    parser.add_option( '-d','--direct', action='store_true', dest='FRAC',)
    options, args = parser.parse_args()

    if not os.path.exists(poscarname):
        poscarname0 = SAEnv.find_datfile('vasp')
        if poscarname0 is None:
            sys.exxit("STOP: POSCAR or .vasp files not found")
        poscarname = poscarname0+'.vasp'

    if options.INPUT: poscarname=options.INPUT
    if options.OUTPUT: datname=options.OUTPUT
    datname=re.sub('\.dat','',datname) # 拡張子 .dat がついていたらそれを消す

    # オプション無し引数の時は拡張子自動削除を付けずにそのままファイル名とする
    if len(args) >0: poscarname=args[0]


    ###################################################################
    # 必殺オプション
    NSW,NELM,IBRION,EDIFF,EDIFFG,KP = SAEnv.get_calinfo(code='VASP')

    cell = SAEnv.Read(filename=poscarname,code='VASP')

    title = cell.title
    scale = cell.scale
    natom = cell.natom
    nion = cell.nion
    selective = cell.selective
    direct = cell.direct
    vasp_version = cell.direct
    t = cell.t
    atoms = cell.atoms
    atoms_index = cell.atoms_index
    position = cell.position
    fix = cell.fix
    atoms_index_j = cell.atoms_index_j

#   STD=True
    STD=False
    FRAC=True

    print_mx_dat(datname,STD,\
        title,scale,natom,nion,selective,direct,vasp_version,\
        t,atoms,atoms_index,position,fix,\
        atoms_index_j,\
        NSW=NSW,\
        NELM=NELM,\
        IBRION=IBRION,\
        EDIFF=EDIFF,\
        EDIFFG=EDIFFG,\
        KP=KP,\
        FRAC=FRAC)

    if direct and not FRAC:
        print "CARTESIAN MODE"
    else:
        print "FRAC(Direct) MODE"
    print "INPUT  "+poscarname
    print "OUTPUT "+datname+".dat"
    print "NORMAL END"


