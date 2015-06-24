#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# OUTCAR 読み込み (汎用,その他)
#   情報はすべて return で返す
#
################################################################################
# 共通基本変数
#
# atoms[i]          : 原子の種類番号(max=nion)を与えると、その原子種の数を返す
# atoms_index[i]    : 原子の種類番号(max=nion)を与えると、原子種の元素記号を返す
# atoms_index_j[i]  : 通し番号(max=natom)を与えると、原子種の元素記号を返す
# ion[j]            : 通し番号(max=natom)を与えると原子の種類番号を返す
# ion_local[j]      : 通し番号(max=natom)を与えるとサイト内のローカル通し番号を返す
#
# position[j,3]     : 通し番号(max=natom)とx,y,z 指定で内部座標
# fix[j,3]          : 通し番号(max=natom)とx,y,z 指定でForceのFix/non-Fix 指定
#
# title             : タイトル
# scale             : 格子定数(スケールファクター)
# selective         : selective mode
# direct            : direct or cartesian
#
################################################################################
#
# 2015.06.15
#  nbands 及び natom の 読み込みでの複数の Dimension of array があったときに
#  最初の dim. of array のみ有効にするように変更（ OUTCAR 出力のバグ対応)
#
# 2015.06.15
#
#  OUTCAR 出力のバグをうけて、NION が 10 以上ならば間違った出力の可能性があるので
#  vasprun.xml からの読み込みに切り替える様にする(vasprun.xml がもしあれば)
#
# 2015.06.15
#
#  atoms_index_j() 実装
#
# 2015.06.15
#
#  VASP の OUTCR の出力にバグを発見 ( ions per type が正しい出力をされない )
#
#  ION の TYPE がめっちゃ多いと途中までしか ions per type に出力されない
#  全部で 10 種類の原子まで
#  計算自体は内部でしっかりやっているようなのだが、OUTCAR の出力が途中
#  vasprun.xml は正常
#
# 2015.06.15
#
#   OUTCAR 中に複数尾 Dimension of array 項目が出てくることがある
#     ex. monoclinic ZrO2 (111) surface
#   vasprun.xml を見ていると 最初に出てきたモノが正解？っぽいので
#   二度目以降は読まないようにする
#
# 2015.06.15
#
#  master を version 0.1.00 へアップデート
#  （旧バージョンは old_class_method としてブランチしておく)
#
#  class の使い方を2015年中版での方法論へ全面的にアップデート
#  (いくつかのバグの荒い直しでコードを読み直すためのアップデートでもある)
#
#  クラスのリファクタリング
#
#  パースの方法論としてはむしろクラスを使わずに一括処理していた時代に近い
#  method と constracta での処理の比率を constracta 比重を多くして、ほとんど
#  constracta で一括処理をする。method は get_* アクセスのための立ち位置。
#  シンプル化が目的。--> 2015中期だとそのバランスの方が自分の中での主流
#
#  ただし、速度が遅い（たぶん失敗）、DOS などのデーターパースだと constracta
#  重視の方がかなり高速なのだが、莫大なテキストを正規表現で毎回マッチするのは
#  たぶんアホ。元に戻す必要があるかもしれない。
#
################################################################################
#
# 2015.02.24
#  method 名ルール変更に伴い get_iter_num() --> get_n_ion_loop()
#
# 2015.01.31
#  title 取得における末尾までの空白削除を追加(ReadDoscarに準ずる)
#
# 2015.01.29
#  get_nkpts() 追加
#  get_nbands() 追加
#  get_title() 追加
#
# 2015.01.29
#   get_tmode() の名前を get_md_mode に変更(意味のある名前にした)
#   ReadOszicar.get_tmode() も同様に ReadOszicar.get_md_mode() へ変更
#
# 2015.01.29
#   get_kpoints_type() method が KPOINTS が auto mesh だと
#   生成されない（原理的に生成しない)事に気がついたので、
#   KPOINTS auto mesh のときは disable にする
#
#   get_kpoints_mode()
#   上記のフラグを取得する
#   ReadKpoints.get_kpoints_mode() と基本互換(まだ実装自体は一部のフラグのみ)
#
#     OUTCAR の KPOINTS セッションから KPOINTS ファイルの内容(動作モード)の類推
#     かなり未完成。SCF でのオートmesh と band での line-mode の区別くらい
#     def get_kpoints_mode(self):
#
# 2015.01.29
#   get_atoms_index で用いている OUTCAR かの PP 情報入手に使っている
#   VRHFIN は NWRITE 2 以上でないと記述されないため
#   POTCAR: タグから PP 情報を入手する方針へ method を変更
#   旧method は get_atoms_index0 と命名変更して残す
#
# 2015.01.29
#   NWRITE を返すmethod , get_nwrite()
#
# 2015.01.28
#   # Fermi Leve をゲット E-fermi から
#   def get_efermi(self):
#
# 2015.01.27
#   逆格子の情報を吸い出すmethodを追加
#
# 2015.01.26
#   ISYM =0 の時の処理のために get_isym メソッドを追加し,
#   get_pint_sym method を修正した
#
#   IBRION ゲット method 追加
#
#   実際に計算した ion_loop 数をゲットするmethod (get_iter_num)追加
#
#   ETOTAL (MDモード FreeEnergy + EKIN ) ゲット method
#   free energy TOTEN ゲット method
#
# 2015.01.15
#   結晶点群を吸い出すmethodを追加
#
# 2015.01.13
#   nion, atoms, atoms_index 対応
#
# 2015.01.09
#   startup, 圧縮ファイル対応版
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
#import gzip
import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadOutcar(object):


    def __init__(self,cname):

        self.datlines, self.num = SAE.read_dataline(cname)

        rec_reg = re.compile('.*reciprocal lattice vectors',re.IGNORECASE)
        title_reg = re.compile('.*POSCAR:')
        nkpts_reg = re.compile('.*NKPTS.*')
        nbands_reg = re.compile('.*NBANDS.*')
        spin_reg = re.compile('.*ISPIN.*',re.IGNORECASE)
        orbit_reg = re.compile('.*LORBIT.*',re.IGNORECASE)
        nsw_reg = re.compile('.*NSW.*',re.IGNORECASE)
        isym_reg = re.compile('.*ISYM',re.IGNORECASE)
        ibrion_reg = re.compile('.*IBRION',re.IGNORECASE)
        nwrite_reg = re.compile('.*NWRITE',re.IGNORECASE)
        efermi_reg = re.compile('^.*E-fermi')

        iter_reg = re.compile('.*-- Iteration',re.IGNORECASE)
        toten_ion_reg = re.compile('.*free  energy   TOTEN',re.IGNORECASE)

        nions_reg = re.compile('.*number of ions.*NIONS.*',re.IGNORECASE)
        ion_type_reg = re.compile('.*ions per type',re.IGNORECASE)

        self.t = np.zeros((3,3))
        self.rec_t = np.zeros((3,3))

        self.atoms = []
        self.toten_ion = []

        for i in range(self.num):

            # title
            if bool(title_reg.match(self.datlines[i])):
                self.title = re.sub(' *$','',self.datlines[i][9:])

            # nkpts (複数の dim. of array 項目があったときに最初のみ有効)
            if bool(nkpts_reg.match(self.datlines[i])):
                try:
                    self.nkpts = self.nkpbs
                except:
                    self.nkpts = int(self.datlines[i].split()[3])

            # natom ( VASP 公式では NSIONS に相当 , 複数の dim. 対応)
            if bool(nions_reg.match(self.datlines[i])):
                try:
                    self.natom = self.natom
                except:
                    self.natom = int(self.datlines[i].split()[11])

            # nbands (複数の dim. of array 項目があったときに最初のみ有効)
            if bool(nbands_reg.match(self.datlines[i])):
                try:
                    self.nbands = self.nbands
                except:
                    self.nbands = int(self.datlines[i].split()[14])

            # spin
            if bool(spin_reg.match(self.datlines[i])):
                self.ispin = int(self.datlines[i].split()[2])

            # lorbit
            if bool(orbit_reg.match(self.datlines[i])):
                self.lorbit = int(self.datlines[i].split()[2])

            # nsw
            if bool(nsw_reg.match(self.datlines[i])):
                self.nsw = int(self.datlines[i].split()[2])

            # isym
            if bool(isym_reg.match(self.datlines[i])):
                self.isym = int(self.datlines[i].split()[2])

            # ibrion
            if bool(ibrion_reg.match(self.datlines[i])):
                self.ibrion = int(self.datlines[i].split()[2])

            # nwrite
            if bool(nwrite_reg.match(self.datlines[i])):
                self.nwrite = int(self.datlines[i].split()[2])

            # nion ( VASP 公式では TYPES に相当 )
            if bool(ion_type_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.nion = len(tmp)-4

            # atoms[i] : 原子の種類番号(max=nion)を与えるとその原子種の数を返す
            if bool(ion_type_reg.match(self.datlines[i])):
                for ion in range(self.nion):
                    self.atoms.append(int(self.datlines[i].split()[4+ion]))

            # current の iter number をゲット(最後には全Iter番号が入る)
            # get_n_ion_loop (旧名) get_iter_num
            if bool(iter_reg.match(self.datlines[i])):
                self.n_ion_loop = int(self.datlines[i].split()[2].replace('(',''))

            # Total Free Energy
            if bool(toten_ion_reg.match(self.datlines[i])):
                self.toten_ion.append(float(self.datlines[i].split()[4]))

            # Fermi Energy
            if bool(efermi_reg.match(self.datlines[i])):
               self.efermi = self.datlines[i].split()[2]

            # t and recipcola
            if bool(rec_reg.match(self.datlines[i])):

                t1_x = float(self.datlines[i+1].split()[0])
                t1_y = float(self.datlines[i+1].split()[1])
                t1_z = float(self.datlines[i+1].split()[2])
                rec1_x = float(self.datlines[i+1].split()[3])
                rec1_y = float(self.datlines[i+1].split()[4])
                rec1_z = float(self.datlines[i+1].split()[5])

                t2_x = float(self.datlines[i+2].split()[0])
                t2_y = float(self.datlines[i+2].split()[1])
                t2_z = float(self.datlines[i+2].split()[2])
                rec2_x = float(self.datlines[i+2].split()[3])
                rec2_y = float(self.datlines[i+2].split()[4])
                rec2_z = float(self.datlines[i+2].split()[5])

                t3_x = float(self.datlines[i+3].split()[0])
                t3_y = float(self.datlines[i+3].split()[1])
                t3_z = float(self.datlines[i+3].split()[2])
                rec3_x = float(self.datlines[i+3].split()[3])
                rec3_y = float(self.datlines[i+3].split()[4])
                rec3_z = float(self.datlines[i+3].split()[5])

                self.t[0,0] = t1_x
                self.t[1,0] = t1_y
                self.t[2,0] = t1_z

                self.t[0,1] = t2_x
                self.t[1,1] = t2_y
                self.t[2,1] = t2_z

                self.t[0,2] = t3_x
                self.t[1,2] = t3_y
                self.t[2,2] = t3_z

                self.rec_t[0,0] = rec1_x
                self.rec_t[1,0] = rec1_y
                self.rec_t[2,0] = rec1_z

                self.rec_t[0,1] = rec2_x
                self.rec_t[1,1] = rec2_y
                self.rec_t[2,1] = rec2_z

                self.rec_t[0,2] = rec3_x
                self.rec_t[1,2] = rec3_y
                self.rec_t[2,2] = rec3_z


    ############################################################################
    ## 逆格子ベクトルを吸い出す
    ##         x   y   z
    ##   t1 = t11 t21 t31
    ##   t2 = t12 t22 t32
    ##   t3 = t13 t23 t33
    ##
    ## 本来の基本並進ベクトルの定義は
    ##       t1  t2   t3
    ##   x = t11 t12 t13
    ##   y = t21 t22 t23
    ##   z = t31 t32 t33
    ##
    ## >> 正常なmatrixの添字とは転置した添字となるが、
    ##    正しいmatrixの添字で見直すときに正しい並進ベクトルになるためである
    ##    VASP の入力(表示)形式が縦横逆なため
    ##
    def get_reciprocal_t_init(self):
        return self.rec_t

    def get_t(self):
        return self.t

    def get_title(self):
        return self.title

    def get_nkpts(self):
        return self.nkpts

    def get_nbands(self):
        return self.nbands

    def get_ispin(self):
        return self.ispin

    def get_lorbit(self):
        return self.lorbit

    def get_nsw(self):
        return self.nsw

    def get_natom(self): # 注意) VASP 公式では NIONS に相当
        return self.natom

    def get_nion(self): # 注意) VASP 公式では TYPES に相当
        if self.nion >= 10: # OUTCAR出力バグ対策
            if os.path.exists('vasprun.xml'):
                vrun = SAE.ReadVasprun()
                self.nion = vrun.get_nion()
            else:
                sys.exit("STOP(get_nion): NION >= 10")
        return self.nion

    def get_atoms(self):
        if self.nion >= 10: # OUTCAR出力バグ対策
            if os.path.exists('vasprun.xml'):
                vrun = SAE.ReadVasprun()
                self.atoms = vrun.get_atoms()
        return self.atoms

    def get_isym(self):
        return self.isym

    def get_ibrion(self):
        return self.ibrion

    def get_nwrite(self):
        return self.nwrite

    def get_n_ion_loop(self):
        return self.n_ion_loop

    def get_toten_ion(self):
        return self.toten_ion

    def get_efermi(self):
        return self.efermi


    # OUTCAR の KPOINTS セッションから KPOINTS ファイルの内容(動作モード)の類推
    # かなり未完成。SCF でのオートmesh と band での line-mode の区別くらい
    def get_kpoints_mode(self):
        auto_FLAG = False
        line_FLAG = False
        hand_FLAG = False
        car_FLAG  = False
        rec_FLAG  = False

        kpoints_reg = re.compile('.*KPOINTS:.*')
        for i in range(self.num):
            if bool(kpoints_reg.match(self.datlines[i])):
                if "Automatic" == self.datlines[i+2].split()[0]:
                    auto_FLAG = True
                if "k-points" == self.datlines[i+2].split()[0]:
                    line_FLAG = True
                break

        self.FLAGS = [auto_FLAG,line_FLAG,hand_FLAG,car_FLAG,rec_FLAG]
        return self.FLAGS


    # 入力された KPOINTS の座標形式をゲット(cartesian or reciprocal)
    # もし band-mode(line-mode) でないのならば、Automatic モードならば
    # Automatic と返す
    def get_kpoints_type(self):
        kpoints_reg = re.compile('.*KPOINTS:.*')
        for i in range(self.num):
            if bool(kpoints_reg.match(self.datlines[i])):
                if "Automatic" == self.datlines[i+2].split()[0]:
                    self.kpoints_type = 'Automatic'
                else:
                    self.kpoints_type = self.datlines[i+2].split()[2]
                break
        return self.kpoints_type


    # atoms_index (My配列) の情報を引っ張るMethod
    # VRHFIN ではなく POTCAR: から PP の原子種情報を引っ張る
    def get_atoms_index(self):
        NION = self.get_nion()
        self.atoms_index = []
        j = 0

        potcar_reg = re.compile('.*POTCAR: ')
        for i in range(self.num):
            if bool(potcar_reg.match(self.datlines[i])):
                j += 1
                tmp = str(self.datlines[i].split()[2])
                self.atoms_index.append(tmp)
        j = int(j/2)
        for i in range(j):
            self.atoms_index.pop()
        if j != NION:
            sys.exit("STOP(get_atoms_index): NION !=",NION)

        return self.atoms_index


    # atoms_index (My配列) の情報を引っ張るMethod
    # 名称を get_atoms_index0 と変更 (NWRITE =2 以上でないと動作しない)
    def get_atoms_index0(self):
        NION = self.get_nion()
        self.atoms_index = []
        j = 0

        # 注意)  NWRITE が 2(default) 以上でないと VRHFIN 項目が出てこない
        vrhfin_reg = re.compile('.*VRHFIN =',re.IGNORECASE)
        for i in range(self.num):
            if bool(vrhfin_reg.match(self.datlines[i])):
                j += 1
                src = self.datlines[i]
                dst = re.sub(':.*','',src)
                dst = re.sub('.*VRHFIN =','',dst)
                self.atoms_index.append(dst)
        if j != NION:
            sys.exit("STOP(get_atoms_index): NION !=",NION)

        return self.atoms_index

    # atoms_j (My配列),natomまでの通し番号で原子の種類を返すMethod
    def get_atoms_j(self):
        natom = self.get_natom()
        nion = self.get_nion()
        atoms = self.get_atoms()
        j = 0
        atoms_j = np.zeros(natom,dtype=int)
        for ion in range(nion):
            for atom in range(atoms[ion]):
                atoms_j[j] = ion
                j += 1

        return atoms_j

    def get_atoms_index_j(self):
        natom = self.get_natom()
        nion = self.get_nion()
        atoms = self.get_atoms()
        atoms_index = self.get_atoms_index()
        j = 0
        atoms_index_j = np.zeros(natom,dtype='S2')
        for ion in range(nion):
            for atom in range(atoms[ion]):
                atoms_index_j[j] = atoms_index[ion]
                j += 1
        return atoms_index_j

    # get_mode
    # IBRION=0 or それ以外
    def get_md_mode(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            self.MD_FLAG = True
        else:
            self.MD_FLAG = False
        return self.MD_FLAG

    # MD-mode のときに temperature をゲットする
    def get_temperature(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            # MD-mode
            n_ion_loop = self.get_n_ion_loop()
            self.temperature = np.zeros(n_ion_loop)
            ekin_reg = re.compile('.*EKIN_LAT=',re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(ekin_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.temperature[j] = float(tmp[5])
                    j += 1
        else:
            self.temperature = ['0']

        return self.temperature

    # MD-mode のときに ETOTAL をゲットする
    # (非MDのときは free energy TOTENを返す)
    def get_etotal(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            # MD-mode
            n_ion_loop = self.get_n_ion_loop()
            self.ETOTAL = np.zeros(n_ion_loop)
            etotal_reg = re.compile('.*ETOTAL =',re.IGNORECASE)
            j = 0
            for i in range(self.num):
                if bool(etotal_reg.match(self.datlines[i])):
                    tmp = self.datlines[i].split()
                    self.ETOTAL[j] = float(tmp[4])
                    j += 1
        else:
            toten_ion = self.get_toten_ion()
            self.ETOTAL = toten_ion

        return self.ETOTAL


    # OUTCAR から 結晶点群を吸い出す
    # ISYM=0 のときは off を返す
    def get_point_symmetry(self):
        ISYM = self.get_isym()
        if ISYM != 0:
            point_sym_text = '.*The.*tic.*fig.*ion.*ha.* point symmetry '
            point_sym_reg = re.compile(point_sym_text, re.IGNORECASE)
            for i in range(self.num):
                if bool(point_sym_reg.match(self.datlines[i])):
                    src = self.datlines[i]
                    dst = re.sub(point_sym_text,'',src)
                    dst = re.sub('\.','',dst)
                    point_sym = str(dst)
        else:
            point_sym = 'sym_off'

        return point_sym


################################################################################
if __name__ == '__main__':

    name = 'OUTCAR'

    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input', dest='INPUT',)
    options,  args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    outcar = ReadOutcar(name)
    NION = outcar.get_nion()
    NSPIN = outcar.get_ispin()
    LORBIT = outcar.get_lorbit()
    NATOM =  outcar.get_natom()
    NSW =  outcar.get_nsw()
    NKPTS = outcar.get_nkpts()
    NBANDS = outcar.get_nbands()
    TITLE = outcar.get_title()
    ISYM = outcar.get_isym()
    IBRION = outcar.get_ibrion()
    NWRITE = outcar.get_nwrite()

    point_sym = outcar.get_point_symmetry()
    n_ion_loop = outcar.get_n_ion_loop()
    efermi = outcar.get_efermi()

    print "TITLE     = ", TITLE
    print "LORBIT    = ", LORBIT
    print "NSW       = ", NSW
    print "NSPIN     = ", NSPIN
    print "NION      = ", NION
    print "NATOM     = ", NATOM
    print "NKPTS     = ", NKPTS
    print "NBANDS    = ", NBANDS
    print "ISYM      = ", ISYM
    print "Point SYM = ", point_sym
    print "IBRION    = ", IBRION
    print "Num.of IT = ", n_ion_loop
    print "E-fermi   = ", efermi
    print "NWRITE    = ", NWRITE

    atoms = outcar.get_atoms()
    atoms_index = outcar.get_atoms_index()

    print ""
    print "atoms_index"
    print "   ",
    for ion in range(NION):
        print atoms_index[ion],
    print ""
    print "atoms"
    print "   ",
    for ion in range(NION):
        print atoms[ion],
    print ""

    print "",
    print "i,atoms_j"
    atoms_j = outcar.get_atoms_j()
    for i in range(NATOM):
        print " ",i,atoms_j[i]

    print "",
    print "i,atoms_index_j"
    atoms_index_j = outcar.get_atoms_index_j()
    for i in range(NATOM):
        print " ",i,atoms_index_j[i]

#   temperature = outcar.get_temperature()
#   for j in range(n_ion_loop):
#       print temperature[j]

#   outcar.get_etotal()
#   ETOTAL = outcar.get_etotal()
#   for j in range(n_ion_loop):
#       print ETOTAL[j]

#   etotal_ion = outcar.get_toten_ion()
#   for j in range(n_ion_loop):
#       print etotal_ion[j]

#   kpoints_FLAGS = outcar.get_kpoints_mode()
#   kpoints_type = outcar.get_kpoints_type()

#   print kpoints_type
#   print " reciprocal lattice vectors "

    print ""
    rec_t = outcar.get_reciprocal_t_init()
    print " %12.9f %12.9f %12.9f" % ( rec_t[0,0], rec_t[1,0], rec_t[2,0])
    print " %12.9f %12.9f %12.9f" % ( rec_t[0,1], rec_t[1,1], rec_t[2,1])
    print " %12.9f %12.9f %12.9f" % ( rec_t[0,2], rec_t[1,2], rec_t[2,2])


