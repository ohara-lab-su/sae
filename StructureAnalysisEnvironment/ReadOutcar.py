#!/usr/bin/env python
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# VASP
# OUTCAR 読み込み (汎用,その他)
#   情報はすべて return で返す
#
################################################################################
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
__version__    = "0.0.12"
################################################################################

import sys
import gzip
import os
import re
import optparse
import numpy as np

#import StructureAnalysisEnvironment as SAE                                      
#import SpaceGroupEnvironment as SGE  

################################################################################
class ReadOutcar(object):

    def __init__(self,cname):

        if os.path.exists(cname):
            GZIP=False
        elif os.path.exists(cname+".gz"):
            GZIP=True
        else:
            sys.exit("STOP: "+cname+" or "+cname+".gz file not found")

        try:
            if GZIP:
                tmp = gzip.open(cname+".gz")
            else:
                tmp = open(cname)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: "+cname+" or "+cname+".gz does'nt open")
        finally:
            tmp.close()

        self.datlines = datfile.split('\n')
        self.num = len(self.datlines) -1

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
        rec_reg = re.compile('.*reciprocal lattice vectors',re.IGNORECASE)
        t = np.zeros((3,3))
        rec_t = np.zeros((3,3))
        for i in range(self.num):
            if bool(rec_reg.match(self.datlines[i])):

                tmp = self.datlines[i+1].split()
                t1_x   = tmp[0]
                t1_y   = tmp[1]
                t1_z   = tmp[2]
                rec1_x = tmp[3]
                rec1_y = tmp[4]
                rec1_z = tmp[5]

                tmp = self.datlines[i+2].split()
                t2_x   = tmp[0]
                t2_y   = tmp[1]
                t2_z   = tmp[2]
                rec2_x = tmp[3]
                rec2_y = tmp[4]
                rec2_z = tmp[5]

                tmp = self.datlines[i+3].split()
                t3_x   = tmp[0]
                t3_y   = tmp[1]
                t3_z   = tmp[2]
                rec3_x = tmp[3]
                rec3_y = tmp[4]
                rec3_z = tmp[5]

                t[0,0] = t1_x
                t[1,0] = t1_y
                t[2,0] = t1_z

                t[0,1] = t2_x
                t[1,1] = t2_y
                t[2,1] = t2_z

                t[0,2] = t3_x
                t[1,2] = t3_y
                t[2,2] = t3_z

                rec_t[0,0] = rec1_x
                rec_t[1,0] = rec1_y
                rec_t[2,0] = rec1_z

                rec_t[0,1] = rec2_x
                rec_t[1,1] = rec2_y
                rec_t[2,1] = rec2_z

                rec_t[0,2] = rec3_x
                rec_t[1,2] = rec3_y
                rec_t[2,2] = rec3_z
                break
        return rec_t

    def get_title(self):
        title_reg = re.compile('.*POSCAR:')
        for i in range(self.num):
            if bool(title_reg.match(self.datlines[i])):
                src = self.datlines[i][9:]
                self.TITLE = re.sub(' *$','',src)
        return self.TITLE

    def get_nkpts(self):
        nkpts_reg = re.compile('.*NKPTS.*')
        for i in range(self.num):
            if bool(nkpts_reg.match(self.datlines[i])):
                self.NKPTS = int(self.datlines[i].split()[3])
                break
        return self.NKPTS

    def get_nbands(self):
        nbands_reg = re.compile('.*NBANDS.*')
        for i in range(self.num):
            if bool(nbands_reg.match(self.datlines[i])):
                if 'NBANDS=' == str(self.datlines[i].split()[13]):
                    self.NBANDS = int(self.datlines[i].split()[14])
                break
        return self.NBANDS


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

    # SPIN の情報を引っ張るMethod
    def get_ispin(self):
        spin_reg = re.compile('.*ISPIN.*',re.IGNORECASE)    
        for i in range(self.num):
            if bool(spin_reg.match(self.datlines[i])):
                spin_line = self.datlines[i].split()
                self.ISPIN = spin_line[2]
        return self.ISPIN

    # LORBIT の情報を引っ張るMethod
    def get_lorbit(self):
        orbit_reg = re.compile('.*LORBIT.*',re.IGNORECASE)    
        for i in range(self.num):
            if bool(orbit_reg.match(self.datlines[i])):
                orbit_line = self.datlines[i].split()
                self.LORBIT = orbit_line[2]
        return self.LORBIT

    # NSW の情報を引っ張るMethod
    def get_nsw(self):
        nsw_reg = re.compile('.*NSW.*',re.IGNORECASE)    
        for i in range(self.num):
            if bool(nsw_reg.match(self.datlines[i])):
                orbit_line = self.datlines[i].split()
                self.NSW = orbit_line[2]
        return self.NSW

    # NATOM (VASP 公式ではNIONS) の情報を引っ張るMethod
    def get_natom(self):
        nions_reg = re.compile('.*number of ions.*NIONS.*',re.IGNORECASE)    
        for i in range(self.num):
            if bool(nions_reg.match(self.datlines[i])):
                nions_line = self.datlines[i].split()
                self.NATOM = int(nions_line[11])
        return self.NATOM

    # NION (My配列) の情報を引っ張るMethod, (VASP公式ではTYPESに相当)
    def get_nion(self):
        ion_type_reg = re.compile('.*ions per type',re.IGNORECASE)
        for i in range(self.num):
            if bool(ion_type_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.NION = len(tmp)-4
        return self.NION

    # atom (My配列) の情報を引っ張るMethod
    def get_atoms(self):
        NION = self.get_nion()
        ion_type_reg = re.compile('.*ions per type',re.IGNORECASE)
        self.ATOMS = []
        for i in range(self.num):
            if bool(ion_type_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                for ion in range(NION):
                    self.ATOMS.append(int(tmp[4+ion]))
        return self.ATOMS


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

    # ISYM
    def get_isym(self):
        isym_reg = re.compile('.*ISYM',re.IGNORECASE)
        for i in range(self.num):
            if bool(isym_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.ISYM = int(tmp[2])
        return self.ISYM

    # IBRION
    def get_ibrion(self):
        ibrion_reg = re.compile('.*IBRION',re.IGNORECASE)
        for i in range(self.num):
            if bool(ibrion_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.IBRION = int(tmp[2])
        return self.IBRION

    # NWRITE
    def get_nwrite(self):
        nwrite_reg = re.compile('.*NWRITE',re.IGNORECASE)
        for i in range(self.num):
            if bool(nwrite_reg.match(self.datlines[i])):
                self.NWRITE = int(self.datlines[i].split()[2])
        return self.NWRITE

    # get_mode
    # IBRION=0 or それ以外
    def get_md_mode(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            self.MD_FLAG = True
        else:
            self.MD_FLAG = False

        return self.MD_FLAG

    # get_iter_num
    # 実際に計算した ION iter 数をゲットする
    def get_iter_num(self):
        iter_reg = re.compile('.*-- Iteration',re.IGNORECASE)
        for i in range(self.num):
            if bool(iter_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.iter_num = int(tmp[2].replace('(',''))
        return self.iter_num

    # MD-mode のときに temperature をゲットする
    def get_temperature(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            # MD-mode
            iter_num = self.get_iter_num()
            self.temperature = np.zeros(iter_num)
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

    # free energy TOTEN を ion-loop 毎にゲットする
    def get_toten_ion(self):
        toten_ion_reg = re.compile('.*free  energy   TOTEN',re.IGNORECASE)
        iter_num = self.get_iter_num()
        self.toten_ion = np.zeros(iter_num)
        j = 0
        for i in range(self.num):
            if bool(toten_ion_reg.match(self.datlines[i])):
                tmp = self.datlines[i].split()
                self.toten_ion[j] = float(tmp[4])
                j += 1

        return self.toten_ion

    # MD-mode のときに ETOTAL をゲットする
    # (非MDのときは free energy TOTENを返す)
    def get_etotal(self):
        IBRION = self.get_ibrion()
        if IBRION == 0:
            # MD-mode
            iter_num = self.get_iter_num()
            self.ETOTAL = np.zeros(iter_num)
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

    # Fermi Leve をゲット E-fermi から
    def get_efermi(self):
        efermi_reg = re.compile('^.*E-fermi')
        for i in range(self.num):
            if bool(efermi_reg.match(self.datlines[i])):
               self.efermi = self.datlines[i].split()[2]

        return self.efermi

################################################################################
if __name__ == '__main__':
                                                                                
    name = 'OUTCAR'
                                                                                
    parser = optparse.OptionParser()
    parser.add_option(  '-i','--input',
                        dest='INPUT',
                        default=name,
    )
    options,  args = parser.parse_args()
                                                                                
    if options.INPUT:
        name=options.INPUT
                                                                                
    if len(args) > 0:
        name=args[0]
                                                                                
    outcar = ReadOutcar(name)
    NION = outcar.get_nion()
    NSPIN = outcar.get_ispin()
    LORBIT = outcar.get_lorbit()
    NATOM =  outcar.get_natom()
    NSW =  outcar.get_nsw()
    NKPTS = outcar.get_nkpts()
    NBANDS = outcar.get_nbands()
    TITLE = outcar.get_title()

    print "TITLE = ", TITLE
    print "LORBIT = ", LORBIT
    print "NSW    = ", NSW
    print "NSPIN  = ", NSPIN
    print "NION   = ", NION
    print "NATOM  = ", NATOM
    print "NKPTS  = ", NKPTS
    print "NBANDS = ", NBANDS
    
    atoms = outcar.get_atoms()
    atoms_index = outcar.get_atoms_index()

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

#   atoms_j = outcar.get_atoms_j()
#   for i in range(NATOM):
#       print i,atoms_j[i]
   
#   ISYM = outcar.get_isym()
#   print "ISYM   = ",ISYM
#   print ""
#   point_sym = outcar.get_point_symmetry()
#   print "Point SYM = ", point_sym

#   IBRION = outcar.get_ibrion()
#   print IBRION

#   # loop 数
#   iter_num = outcar.get_iter_num()
#   print iter_num

#   temperature = outcar.get_temperature()
#   for j in range(iter_num):
#       print temperature[j]

#   outcar.get_etotal()
#   ETOTAL = outcar.get_etotal()
#   for j in range(iter_num):
#       print ETOTAL[j]

#   etotal_ion = outcar.get_toten_ion()
#   for j in range(iter_num):
#       print etotal_ion[j]

    rec_t = outcar.get_reciprocal_t_init()
    kpoints_FLAGS = outcar.get_kpoints_mode()
    kpoints_type = outcar.get_kpoints_type()

    print kpoints_type
#   print " reciprocal lattice vectors "
#   print " %12.9f %12.9f %12.9f" % ( rec_t[0,0], rec_t[1,0], rec_t[2,0])
#   print " %12.9f %12.9f %12.9f" % ( rec_t[0,1], rec_t[1,1], rec_t[2,1])
#   print " %12.9f %12.9f %12.9f" % ( rec_t[0,2], rec_t[1,2], rec_t[2,2])

#   efermi = outcar.get_efermi()
#   print "E-fermi:", efermi

#   NWRITE = outcar.get_nwrite()
#   print "NWRITE:",NWRITE
