#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# WIEK2k case.dos を読み込む class
#
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WIEN2k 固有の問題に発する他のルーチンとの違い
#
# 注意0)
#      入力データーに LDOS も PDOS の違いもない
#      軌道の項目に何が入るかはすべて case.int による手動操作に依存する
#      *.dos* ファイルに case.outputt と同様に case.int の内容の一部が書いてある
#
# 注意1)
#       ReadMxDos* や ReadDoscar などと異なり
#       入力、および吐き出すデーターはスピン依存してない
#
# 注意2)
#       atom の入力は 一番目が 1 となる (他の Read*Dos は atom は 0 から始まる)
#       0 は total-DOS の意味として扱う  (((case.int 形式に準ずる)))
#
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#
################################################################################
#
# 2018.08.15
#  Python2/3 両対応
#
#
# 2015.04.22
#  chk_raw_dos() method の条件比較で配列と比較対象のデーターを
#  共に string にした(数値とstrigの比較とかになっちゃって意図した通りに動かないバグ)
#
#  get_raw_dos() の atom と orbit を同じく修正
#
# 2015.04.21
#  numpy オブジェクト化による簡素化
#
#      #self.ldos_ion = np.zeros(self.nedos)
#      #tmp = self.get_raw_dos(atom=atom,orbit=orbit)
#      #for i in range(self.nedos):
#      #    self.ldos_ion[i] = tmp[i]*times
#
#       self.ldos_ion = self.get_raw_dos(atom=atom,orbit=orbit)*times
#
# 2015.04.21
#   インスタンス作成時の self.dos を numpy array 化
#       np.array(self.dos,dtype=float)
#
# 2015.04.21
#   def get_raw_dos(self,atom=1,orbit='total',times=1.0):
#      戻り値の self.dos を numpy array に変換を追加
#
# 2015.04.06
#  get_head() 追加
#
# 2015.03.27
#  バグの発見
#  get_raw_dos() 呼び出し時の引数で dos 配列からのリファレンスではなくて
#  配列のコピーに変更（一度の instance 作成で、複数回の method 呼び出し対応)
#
# 2015.03.27
#  geet_nion や get_plot_ion で total-DOS 項目などが存在しない時の
#  処理を正しく処理できてなかったところを修正'
#
# 2015.03.26
#  get_ldos_ion() にて読んでいる case.output0 は並列計算すると
#  output0000 になるので注意、修正した
#  他にも output0 を読んでいる部分をまとめて修正
#
# 2015.03.26
#  get_ldos_ion() 関係を追加
#
# 2015.03.26
#  ReadWienOutput0 class にて atoms と nion を区別して atoms と atoms_index
#  を用意しなおした。そのため
#  get_plot_ions() と get_plot_atoms() を区別する
#  get_plot_atoms() と get_plot_ions() は同じ意味なので同名でアクセスできるようにする
#
# 2015.03.25
#  get_plot_atoms_index() 作成に伴い
#  get_atom_list() --> get_plot_atoms() へ名前変更
#
# 2015.03.25
#   Wldos に必要な物はほぼ整備
#
# 2015.03.24
#   startup
#
################################################################################
from __future__ import print_function
try:
    from ...copyright import *
except ImportError:
    from StructureAnalysisEnvironment.copyright import *

__status__     = "alpha"
__version__    = "0.0.1"
################################################################################

import sys
import os
import re
#import gzip
import numpy as np

#import optparse

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAEnv
except ImportError:
    import StructureAnalysisEnvironment as SAEnv


#import SpaceGroupEnvironment as SGE

################################################################################
class ReadWienDos(object):

    ############################################################################
    ## init
    ## ファイルは複数読み込む dos1,dos2,dos3,,,
    ## ただし、dos1dn,dos1up などの up/down は区別しないので呼び出す側で
    ## 工夫する必要がある
    def __init__(self,lists):

        self.nfiles = len(lists)
       #self.labels = []
        self.norbital = 0

        ###########################
        # ファイルごとの読み込み
        self.head_file = []
        self.head = []
        self.dos = []
        self.dos_list_atom = []
        self.dos_list_orbit = []
        for data in range(self.nfiles):
            name = lists[data]
            datlines,num = SAEnv.read_dataline(name)

            self.head_file.append(datlines[0])
            self.head_file.append(datlines[1])
            self.head_file.append(datlines[2])

            # 一つ目のファイルでのパラメーター読み込み & ENERGY 行の登録
            if data == 0:

                efermi0 = '^#EF='
                efermi1 = ' *NDOS.*$'
                self.efermi = re.sub(efermi0,'',datlines[1])
                self.efermi = float(re.sub(efermi1,'',self.efermi))

                word0 = '.*NENRG='
                word1 = ' *Gau.*$'
                self.nedos = re.sub(word0,'',datlines[1])
                self.nedos = int(re.sub(word1,'',self.nedos))

                word0 = '.*NDOS='
                word1 = ' *NENRG.*$'
                ndos = re.sub(word0,'',datlines[1])
                ndos = int(re.sub(word1,'',ndos))

                # Energy 行の登録
                self.dos_list_atom.append('ENERGY')
                self.dos_list_orbit.append('ENERGY')
                tmp = []
                for idos in range(self.nedos):
                    tmp.append(float(datlines[idos+3].split()[0]))
                self.dos.append(tmp)

            # ファイルごとに軌道のラベルが記述
            label = datlines[2].split()
            del label[0:2]               # コメントアウト文字 & ENERGY 行の削除

            lorbit = 0
            for l in label: # ラベル内の要素(軌道毎のループ)

                if not l == 'total-DOS':
                    atom = int(re.sub(':.*','',l))
                    orbit = str(re.sub('\d:','',l))
                    self.dos_list_atom.append(atom)
                    self.dos_list_orbit.append(orbit)
                elif l == 'total-DOS':
                    atom = 0
                    orbit = 'total-DOS'
                    self.dos_list_atom.append(atom)
                    self.dos_list_orbit.append(orbit)

                tmp = []
                for idos in range(self.nedos):
                    tmp.append(float(datlines[idos+3].split()[lorbit+1]))

                self.dos.append(tmp)
                lorbit += 1

            self.head.append(self.head_file)
            self.norbital += len(label)
           #self.labels.append(label)

        np.array(self.dos,dtype=float)
       #print len(self.dos)
       #print len(self.dos_list_atom), self.dos_list_atom
       #print len(self.dos_list_orbit), self.dos_list_orbit

    ############################################################################
    # head
    def get_head(self):
        return self.head

    ############################################################################
    # fermi
    def get_efermi(self):
        return self.efermi

    ############################################################################
    # DOS の分割数
    def get_nedos(self):  # DOS の分割数(Energy分割数)
        return self.nedos

    ############################################################################
    # DOS が収納されているファイルの合計数
    def get_nfiles(self):
        return self.nfiles

    ############################################################################
    # 計算したDOSのすべての軌道数（原子毎のすべての軌道数の合計)
    def get_norbital(self):
        return self.norbital

    ############################################################################
    # DOSを分割しているエネルギーウィンドウの範囲のエネルギーリストを返す
    def get_eng(self):
        self.eng = self.dos[0]
        self.eng = np.array(self.eng)
        return self.eng

    ############################################################################
    # ENG の最大値(DOSのXレンジ)
    def get_emax(self):
        self.emax =  max(self.dos[0])
        return self.emax

    ############################################################################
    # ENG の最小値(DOSのYレンジ)
    def get_emin(self):
        self.emin =  min(self.dos[0])
        return self.emin

    ############################################################################
    # 実際に DOS 計算が行われた原子の種類番号 (case.int 情報と元に計算された)
    # case.int は解読せずに *.dos ファイルの解読から nion 数を判別する
    def get_nion(self):

        work_list = list(self.dos_list_atom)
        for i in range(work_list.count('ENERGY')):
            work_list.remove('ENERGY')             # Energy の行
        for i in range(work_list.count(0)):
            work_list.remove(0)                    # total-DOS の要素

        plot_atoms = list(set(work_list))
        self.nion = len(plot_atoms)
        return self.nion

    ############################################################################
    # 実際に DOS 計算が行われた原子の種類番号のリスト
    # atoms(サイトごとの原子数) と ions(サイトの原子番号)の違いに注意
    def get_plot_ions(self):

        work_list = list(self.dos_list_atom)
        for i in range(work_list.count('ENERGY')):
            work_list.remove('ENERGY')             # Energy の行
        for i in range(work_list.count(0)):
            work_list.remove(0)                    # total-DOS の要素

        self.plot_ions = list(set(work_list))
        return self.plot_ions

    ############################################################################
    # 実際に DOS 計算が行われた原子種の記号リスト ( output0 から記号を読み込む)
    # atoms_index に対応
    def get_plot_ions_index(self,case):

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

        # SCF計算を行った際のすべての原子種の記号リスト
        output0 = SAEnv.io.wien2k.ReadWienOutput0(output0_file)
        atoms_index = output0.get_atoms_index()

        plot_ions = self.get_plot_ions()
        self.plot_ions_index = []
        for atom in plot_ions:
            self.plot_ions_index.append(atoms_index[atom-1])

        return self.plot_ions_index

    ############################################################################
    # 意味的に atoms_index と ions_index は同じ意味
    def get_plot_atoms_index(self,case):
        self.plot_atoms_index = self.get_plot_ions_index(case)
        return self.plot_atoms_index

    ############################################################################
    # 引数で与えられた atom と orbital を持つ DOS を返す
    def get_raw_dos(self,atom=1,orbit='total',times=1.0):

        max_atom  = len(self.dos_list_atom)
        max_orbit = len(self.dos_list_orbit)

        if not max_atom == max_orbit:
            sys.exit("STOP: not max_orbit == max_atom")

        if orbit == 'total-DOS':
            atom = 0

        for i in range(max_atom):
            if str(self.dos_list_atom[i]) == str(atom):
                if str(self.dos_list_orbit[i]) == str(orbit):
                   #print i," :",self.dos_list_atom[i],self.dos_list_orbit[i]

                   #self.dos_raw = self.dos[i]
                   #self.dos_raw = list(self.dos[i])
                    self.dos_raw = np.array(self.dos[i])
                    break

       #np.array(self.dos_raw,dtype=float)

        return self.dos_raw

    ############################################################################
    # 実際に計算したサイトのDOSをサイト内の同一対称性の原子数分のウェイトを掛ける
    def get_ldos_ion(self,case='case',atom=1,orbit='total'):
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

        output0 = SAEnv.io.wien2k.ReadWienOutput0(output0_file)
        atoms = output0.get_atoms()
        times = float(atoms[atom-1])

       #self.ldos_ion = np.zeros(self.nedos)
       #tmp = self.get_raw_dos(atom=atom,orbit=orbit)
       #for i in range(self.nedos):
       #    self.ldos_ion[i] = tmp[i]*times

        self.ldos_ion = self.get_raw_dos(atom=atom,orbit=orbit)*times

        return self.ldos_ion

    ############################################################################
    # 引数で与えられた atom と orbital がデーターに存在すれば True を返す
    def chk_raw_dos(self,atom='1',orbit='total'):
        max_atom  = len(self.dos_list_atom)
        max_orbit = len(self.dos_list_orbit)

        if not max_atom == max_orbit:
            sys.exit("STOP: not max_orbit == max_atom")

        if orbit == 'total-DOS':
            atom = 0

        FLAG=False
        for i in range(max_atom):
            if str(self.dos_list_atom[i]) == str(atom):
                if str(self.dos_list_orbit[i]) == str(orbit):
                    FLAG=True

        return FLAG


################################################################################
if __name__ == '__main__':

    import optparse

    case = re.sub('.*/','',os.getcwd())
   #case = 'Cu'

    unit = 'ev'
    output = 'ldos.dat'

    parser = optparse.OptionParser(os.getcwd())
    parser.add_option( '-i','--input', dest='INPUT', )
    options, args = parser.parse_args()

    if options.INPUT: case = options.INPUT

    print("case               : %s" % str(case))

    lists = SAEnv.find_suffix2(case+'.dos','ev')
    print("lists              : %s" % str(lists))

    output0 = SAEnv.io.wien2k.ReadWienOutput0(case+'.output0')
    atoms_index = output0.atoms_index
    atoms = output0.atoms
    print("atoms_index(output): %s" % str(atoms_index))
    print("atoms      (output): %s" % str(atoms))

    dos = SAEnv.io.wien2k.ReadWienDos(lists)

#   head = dos.get_head()
#   for i in head[0]:
#       print i

    atom=1
#   orbit='s'
#   orbit='total'
    orbit='total-DOS'

    efermi = dos.get_efermi()
    nion =  dos.get_nion()
    emax = dos.get_emax()
    emin = dos.get_emin()
    plot_ions = dos.get_plot_ions()
    plot_ions_index = dos.get_plot_ions_index(case)

    print("nion       (dos)   : %s" % str(nion))
    print("emax       (dos)   : %s" % str(emax))
    print("emin       (dos)   : %s" % str(emax))
    print("efermi     (dos)   : %s" % str(efermi))

    dos.get_ldos_ion(case=case,atom=1,orbit=orbit)

#   print efermi
#   print nion
#   print plot_atoms

# で～て～プリントテスト
#   eng = dos.get_eng()
#   dat = dos.get_raw_dos(atom=atom,orbit=orbit)
#   print "===== atom:"+str(atom)+" orbit:"+str(orbit)
#   for i in range(dos.nedos):
#       print eng[i],dat[i]




