#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# FDMNES
# *.in ファイル
#
# 主に Crystal の部分の解析と読み込み
#
################################################################################
#
# 2015.06.24
#  allsite 計算をしているか否かの判断を*.inp かおこなう
#
# 2015.06.19
#   読み込むタグをいくつか追加
#   コメントアウトの処理
#   タグ名とタグの内容が同一行でも対応可能に
#
# 2015.05.19 startup
#   cellpar(a,b,c,alpha,beta,gamma) --> cell(基本並進) への変換が意外に鬼門
#
#   ２つの選択肢
#
#   (1) 以前に HiLAPW の群論パートを参考に実装したもの SGE を用いる
#   (2) ASE を用いる
#
#   ---> とりあえずこのルーチンの開発は一旦サスペンド
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
__version__    = "0.1.1"
################################################################################

import sys
#import gzip
#import os
import re
import optparse
import numpy as np

import StructureAnalysisEnvironment as SAE
#import SpaceGroupEnvironment as SGE

################################################################################
class ReadFdmInp(object):

    def __init__(self,cname='POSCAR.inp'):

        self.datlines, self.num = SAE.read_dataline(cname)
        self.datlines, self.num = SAE.del_comment(self.datlines)

        magnetism_reg = re.compile('.*Magnetism.*',re.IGNORECASE)
        energygpho_reg = re.compile('.*Energpho.*',re.IGNORECASE)
        absorber_reg = re.compile('.*Absorber.*',re.IGNORECASE)
#       filout_reg = re.compile('.*Filout.*',re.IGNORECASE)
        filout_reg = re.compile('.*Fil.*out.*',re.IGNORECASE)
        atom_reg = re.compile('^\S*Atom',re.IGNORECASE)
        crystal_reg = re.compile('.*crystal.*',re.IGNORECASE)
        mole_reg = re.compile('.*molecule.*',re.IGNORECASE)
        char_reg = re.compile('\D',re.IGNORECASE)
        comment_reg = re.compile('^!.*',re.IGNORECASE)
        allsite_reg = re.compile('^.*allsite.*',re.IGNORECASE)
        calculation_reg = re.compile('^.*Calculation.*',re.IGNORECASE)
        conv_out_reg = re.compile('^.*Conv_out.*',re.IGNORECASE)
        convolution_reg = re.compile('^.*Convolution.*',re.IGNORECASE)
        center_abs_reg = re.compile('^.*Center_abs.*',re.IGNORECASE)

        self.ispin = 1
        self.allsite = False
        self.energygpho = False
        self.position = []
        self.convolution = False
        self.center_abs = False

        for i in range(self.num):


            if bool(energygpho_reg.match(self.datlines[i])):
                self.energygpho = True

            # Atom TAG があるときは停止(未対応)
            if bool(atom_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):
                sys.exit("STOP: non support Atom tag")

            # Magnetism ( Atom タグがない Magnetism は SOC のみ )
            if bool(magnetism_reg.match(self.datlines[i])):
                self.ispin = 2

            # allsite
            if bool(allsite_reg.match(self.datlines[i])):
                self.allsite = True

            # Filout 名確保
            if bool(filout_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.filout = self.datlines[i].split()[1].strip()
                else:
                    self.filout = self.datlines[i+1].strip()

            # Calculation (以前の計算結果を引き継ぐ) 名の確保
            if bool(calculation_reg.match(self.datlines[i])):
                self.calculation = str(self.datlines[i+1].split()[0])

            # conv_out
            if bool(conv_out_reg.match(self.datlines[i])):
                self.conv_out = self.datlines[i+1].split()[0]

            # convolution flag
            if bool(convolution_reg.match(self.datlines[i])):
                self.convolution = True

            # center_abs flag
            if bool(center_abs_reg.match(self.datlines[i])):
                self.center_abs = True

            # Absorber
            if bool(absorber_reg.match(self.datlines[i])):
                if len(self.datlines[i].split()) > 1:
                    self.absorber = int(self.datlines[i].split()[1].strip())
                else:
                    self.absorber = int(self.datlines[i+1].strip())

            # Crystal 行を検索 (position の スペース行コメント行も対応)
            if bool(crystal_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):

                # crystal 行を見つけたらそれは molecule モードではない
                self.MOL=False

                # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
                if not len(self.datlines[i+1].split()) == 6:
                    sys.exit("STOP: a,b,c,alpha,beta,gamma INPUT LINE error")

                i += 1

                # cell パラメーターをゲット
                lattice_a = float(self.datlines[i].split()[0])
                lattice_b = float(self.datlines[i].split()[1])
                lattice_c = float(self.datlines[i].split()[2])
                alpha = float(self.datlines[i].split()[3])
                beta = float(self.datlines[i].split()[4])
                gamma = float(self.datlines[i].split()[5])

                self.cell = [lattice_a,lattice_b,lattice_c,alpha,beta,gamma]

                self.atoms_index_j = []
                while 1:
                    i +=1
                    if len(self.datlines[i].split()) > 0: # 空白行はスキップ

                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break # 数字以外は スキップ

                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        self.atoms_index_j.append(SAE.get_atomic_symbol0(zz))
                        self.position.append([x,y,z])

                    if i == self.num:
                        break

                self.position = np.array(self.position)

            # Mol 行を検索 (position の スペース行コメント行も対応)
            elif bool(mole_reg.match(self.datlines[i])) \
                    and not bool(comment_reg.match(self.datlines[i])):

                # molecule mode (ただし、現状ではcrystal と変わりない形式しか読まない)
                self.MOL=True

                # ここで想定しているのは a,b,c,alpha,beta,gamma 記述モード
                if not len(self.datlines[i+1].split()) == 6:
                    sys.exit("STOP: a,b,c,alpha,beta,gamma INPUT LINE error")

                i +=1
                self.atoms_index_j = []
                while 1:
                    i +=1
                    if len(self.datlines[i].split()) > 0: # 空白行はスキップ

                        if bool(char_reg.match(self.datlines[i].split()[0])):
                            break # 数字以外は スキップ

                        zz = int(self.datlines[i].split()[0])
                        x = float(self.datlines[i].split()[1])
                        y = float(self.datlines[i].split()[2])
                        z = float(self.datlines[i].split()[3])
                        self.atoms_index_j.append(SAE.get_atomic_symbol0(zz))
                        self.position.append([x,y,z])

                    if i == self.num:
                        break

                self.position = np.array(self.position)


        # すべてのサイトの原子数
        self.natom = len(self.position)

       #########################
       #test print atom_index_j
       #########################
       #j=0
       #for i in scaled_position:
       #    print atoms_index_j[j],i
       #    j += 1

    def get_ispin(self):
        return self.ispin

    def get_allsite(self):
        return self.allsite

    def get_energygpho(self):
        return self.energygpho

    def get_absorber(self):
        self.absorber = self.absorber if hasattr(self, 'absorber') else 1
        return self.absorber

    def get_convolution(self):
        return self.convolution

    def get_conv_out(self):
        self.conv_out = self.conv_out if hasattr(self,'conv_out') else None
        return self.conv_out

    def get_calculation(self):
        self.calculation = self.calculation if hasattr(self,'calculation') else None
        return self.calculation

    def get_filout(self):
        self.filout = self.filout if hasattr(self, 'filout') else None
        return self.filout

    def get_position(self):
        return self.position

    def get_natom(self):
        return self.natom

    def get_atoms_index_j(self):
        try:
            self.atoms_index_j = self.atoms_index_j
        except:
            self.atoms_index_j = []
        return self.atoms_index_j

################################################################################
def options():
#   name = 'POSCAR.inp'
    name = 'read_pdb.inp'

    parser = optparse.OptionParser()

    parser.add_option(  '-i','--input', dest='INPUT', default=name,)
    options,args = parser.parse_args()

    if options.INPUT: name=options.INPUT
    if len(args) > 0: name=args[0]

    return name

################################################################################
if __name__ == '__main__':

    name = options()
    out = ReadFdmInp(name)

    absorber = out.get_absorber()
    filout = out.get_filout()
    atoms_index_j = out.get_atoms_index_j()
    natom = out.get_natom()
    position = out.get_position()
    energygpho = out.get_energygpho()
    ispin = out.get_ispin()

    allsite = out.get_allsite()
    calculation = out.get_calculation()
    convolution = out.get_convolution()
    conv_out = out.get_conv_out()

    print 'allsite    :',allsite
    print 'absorber   :',absorber
    print 'energygpho :',energygpho
    print 'ispin      :',ispin
    print 'filout     :',filout
    print 'natom      :',natom

    for i in range(natom):
         print " %s %14.10f %14.10f %14.10f" \
                 %(atoms_index_j[i],position[i,0],position[i,1],position[i,2])

    if convolution:
        print ""
        print "convolution:",convolution
        print 'calculation:',calculation
        print 'conv_out   :',conv_out
#       print "NAME",name


