#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
# K.NAKADA, kengo.nakada@gmail.com
#
# 2018.08.21
#  Python2/3 両対応
#
# 2015.02.17
#   一般的なpythonルールに合わせて PFformat クラスを ReadPfformat に変更
#   およびそれに合わせた class のコンストラクタとメッソドの整備
#
#   1) コンストラクタでファイルリード
#   2) コンストラクタでPFformatの分解 --> 各クラス変数へそのまま全部放り込み
#
# 2014.12.17
#    PF format (9809 format) を読み込む
#     ライブラリ兼基本テストプログラム
#
#    標準試料の透過法のデータのみしかsampleデータにないので
#    (テストしてないので)たぶんそれしか動く保証はない
#
#    CAMAC scaler モードは未テストなので動く保証はない
#
################################################################################
################################################################################
# from __future__ import print_function
# import re
# import optparse
# import copy
################################################################################
################################################################################
#   pf.write_pf()
################################################################################
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import gzip
import numpy as np
import codecs


############################################################################
# read file
#
############################################################################
# write Header of PF format
#
############################################################################
# write PF format
#
class ReadPfformat(object):

    ########################################################################
    # read PF format
    #
    #   self.BL     = tmp[1:6]
    #####################
    # for CAMAC scaler
    #
    #####################
    # for Ortec 974
    #
    #####################
    # DATA
    def __init__(self, name):
        if os.path.exists(name):
            GZIP = False
        elif os.path.exists(name + ".gz"):
            GZIP = True
        else:
            sys.exit("STOP: " + name + " or " + name + ".gz file not found")
        try:
            if GZIP:
                tmp = gzip.open(name + ".gz")
            else:
                tmp = open(name)
            datfile = tmp.read()
        except:
            tmp.close()
            sys.exit("STOP: " + name + " does'nt open")
        finally:
            tmp.close()
        self.datlines = datfile.split("\n")
        self.num = len(self.datlines) - 1
        # 1H,I5,5X,T21,A5
        tmp = self.datlines[0]
        # I5: フォーマット識別コード
        self.IFCD = tmp[1:6]
        # PF フォーマット外ヘッダデータ
        self.BL0 = tmp[11:19]
        # A5: ステーション名
        self.BL = tmp[20:25]
        # 1H,A14,2X,A14,A14
        tmp = self.datlines[1]
        # A14: データファイル名
        self.FN = tmp[1:15]
        # A14: 開始日時
        self.YMD1 = tmp[17:31]
        # A14: 終了日時
        self.YMD2 = tmp[34:48]
        # 1H,A80
        tmp = self.datlines[2]
        # A80: コメント
        self.SAMP = str(tmp[1:80])
        self.SAMP = self.SAMP.rstrip()
        # 1H,'**',F5.1,'**', 2X, F6.1, '**',F6.1,'**'
        tmp = self.datlines[3]
        # F5.1: 電子(陽電子)ビームのエネルギー GeV 単位
        self.ERING = float(tmp[8:13])
        # F6.1: 備蓄電流
        self.CRING1 = float(tmp[19:25])
        # F6.1
        self.CRING2 = float(tmp[31:37])
        # 1H,'12345678',3X,A10,4X,'123',F8.5,'12',4X,'*',F9.5
        tmp = self.datlines[4]
        # A10:  分光結晶面(Mono)
        self.XTAL = tmp[10:20]
        # F8.5: 分光結晶の格子面間隔 (Ang)
        self.D = float(tmp[27:35])
        # F9.5: 測定開始時前の現在角(Initial angle) (deg)
        self.PANG = float(tmp[55:64])
        # 1H,A5,4X,A13,'12',I2,'1',3X,'Repetition=',I3,5X,'*',I5A
        tmp = self.datlines[5]
        # A13: 測定モード Transmisson, Fluorescene 等
        self.CMODE = str(tmp[10:23])
        self.CMODE = self.CMODE.lstrip()
        # I2:  測定モードのコード 2:透過法, 3:蛍光法, 4:電子吸量法
        self.MODE = int(tmp[24:26])
        # I3:  測定の繰り返し回数(Repetition)
        self.IREP = int(tmp[41:44])
        # I5:  1測定中のデーター数(Points)
        self.NPT = int(tmp[56:61])
        tmp = self.datlines[6]
        # A14: 使用したパラメータファイル名
        self.PFN = tmp[14:28]
        # I1:  パラメーターの単位
        self.IAE = int(tmp[42:43])
        # I5:  ブロック数
        self.NBLK = int(tmp[56:61])
        tmp = self.datlines[7]
        tmp = self.datlines[8]
        self.K = np.zeros(self.NBLK, dtype="5S")
        self.block = np.zeros((self.NBLK, 2))
        self.STEP = np.zeros(self.NBLK)
        self.RTIME = np.zeros(self.NBLK)
        self.NUM = np.zeros(self.NBLK)
        for i in range(self.NBLK):
            # 1H, I5, 5X, 2F10.2, F13.2, F11.2, I10
            tmp = self.datlines[9 + i]
            # I5: ブロックの番号(K)
            self.K[i] = tmp[1:6]
            # F10.5: ブロックの区切りの角度(度単位)orエネルギー単位
            self.block[i, 0] = tmp[11:21]
            # F10.5: ブロックの区切りの角度(度単位)orエネルギー単位
            self.block[i, 1] = tmp[21:31]
            # F13.2 or 1PG13.6E: データ点毎の送り角度/エネルギー
            self.STEP[i] = tmp[31:44]
            # F11.2: ブロック点内の測定時間
            self.RTIME[i] = tmp[44:55]
            # I10: ブロック内のデータ点数
            self.NUM[i] = tmp[55:65]
        line = 8 + self.NBLK
        # 1H,'**',I2,'*', 5X,'**',I2
        tmp = self.datlines[line + 1]
        line = line + 1
        # I2: 測定に用いラスケーラ(1:CAMAC, 0:ORTEC974, -1:novice mode)
        self.ICA = int(tmp[7:9])
        # I2: 測定に用いたでたチャンネルの数
        self.NDCH = int(tmp[21:23])
        # MODEM: Jチェンネルの測定モード
        #         1:I0, 2:透過, 3:蛍光, 4:電子吸量, 5:その他
        if self.ICA > 0:
            # Mode
            tmp = self.datlines[line + 1]
            line = line + 1
            self.MODEM = np.zeros((self.NDCH, 2), dtype=int)
            self.OFFS = np.zeros((self.NDCH, 2), dtype=float)
            for j in range(self.NDCH):
                tmp = self.datlines[line + 1]
                a10 = int((j - 1) * 10)
                start = a10 + 30
                end = a10 + 40
                self.MODEM[j, 0] = tmp[start:end]
            for j in range(self.NDCH):
                tmp = self.datlines[line + 1]
                start = end
                end = start + 10
                self.MODEM[j, 1] = tmp[start:end]
            line = line + 1
            for j in range(self.NDCH):
                tmp = self.datlines[line + 1]
                a10 = int((j - 1) * 10)
                start = a10 + 30
                end = a10 + 40
                self.OFFS[j, 0] = tmp[start:end]
            for j in range(self.NDCH):
                tmp = self.datlines[line + 1]
                start = end
                end = start + 10
                self.OFFS[j, 1] = tmp[start:end]
            line = line + 1
        if self.ICA <= 0:
            # Mode
            tmp = self.datlines[line + 1]
            line = line + 1
            self.MODEM = np.zeros(self.NDCH, dtype=int)
            self.OFFS = np.zeros(self.NDCH, dtype=float)
            for j in range(1, self.NDCH):
                # Mode
                tmp = self.datlines[line + 1]
                a10 = int((j - 1) * 10)
                self.MODEM[j] = tmp[a10 + 30 : a10 + 40]
            line = line + 1
            for j in range(1, self.NDCH):
                # Mode
                tmp = self.datlines[line + 1]
                a10 = int((j - 1) * 10)
                self.OFFS[j] = tmp[a10 + 30 : a10 + 40]
            line = line + 1
        self.ANGM = np.zeros(self.NPT)
        self.ANGE = np.zeros(self.NPT)
        self.DWT = np.zeros(self.NPT)
        self.IDTM = np.zeros((self.NPT, self.NDCH))
        line = line + 1
        for i in range(self.NPT):
            tmp = self.datlines[line + i]
            self.ANGM[i] = tmp[0:10]
            self.ANGE[i] = tmp[10:20]
            self.DWT[i] = tmp[20:30]
            if self.ICA > 0:
                self.NDCH0 = 0
            if self.ICA <= 0:
                self.NDCH0 = 1
            for j in range(self.NDCH0, self.NDCH):
                a10 = int((j - 1) * 10)
                self.IDTM[i, j] = tmp[a10 + 30 : a10 + 40]

    def write_head(self, *args):
        num_args = len(args)
        if num_args >= 1:
            outfile = args[0]
            #               out = codecs.open(outfile,'w','utf-8')
            try:
                out = codecs.open(outfile, "a", "utf-8")
            except:
                out.close()
                sys.exit("STOP:" + outfile + " can'nt open")
        else:
            out = sys.stdout
        print("ステーション名                  :", self.BL, file=out)
        print("測定開始日                      :", self.YMD1, file=out)
        print("測定終了日時                    :", self.YMD2, file=out)
        print("コメント(試料名)                :", self.SAMP, file=out)
        print("電子(陽電子)ビームのエネルギー  :", str(self.ERING) + " GeV", file=out)
        print("蓄積電流(測定開始時)            :", str(self.CRING1) + " mA", file=out)
        print("蓄積電流(測定終了時)            :", str(self.CRING2) + " mA", file=out)
        print("分光結晶面                      :", self.XTAL, file=out)
        print("分光結晶面の格子面間隔          :", str(self.D) + " Ang", file=out)
        print("測定開始前の現在角              :", str(self.PANG) + " Deg", file=out)
        print("測定モード                      :", self.CMODE, file=out)
        if self.MODE == 2:
            print("測定モードのコード              : 透過法", file=out)
        if self.MODE == 3:
            print("測定モードのコード              : 蛍光法", file=out)
        if self.MODE == 4:
            print("測定モードのコード              : 電子吸量法", file=out)
        print("測定の繰り返し回数              :", self.IREP, file=out)
        print("1測定中のデータ点数             :", self.NPT, file=out)
        print("使用したパラメータファイル名    :", self.PFN, file=out)
        if self.IAE == 1:
            print("パラメータの単位                : 角度", file=out)
        if self.IAE == 2:
            print("パラメータの単位                : エネルギー", file=out)
        print("ブロック数                      :", self.NBLK, file=out)
        print("", file=out)
        if self.IAE == 1:
            print(
                " "
                + "Block      Init-ang  final-ang     Step/deg     Time/s       Num",
                file=out,
            )
            for i in range(self.NBLK):
                print(
                    " %5d     %10.5f%10.5f%13.6f%11.2f%10d"
                    % (
                        i + 1,
                        self.block[i, 0],
                        self.block[i, 1],
                        self.STEP[i],
                        self.RTIME[i],
                        self.NUM[i],
                    ),
                    file=out,
                )
        if self.IAE == 2:
            print(
                " "
                + "Block      Init-ang  final-Eng     Step/deg     Time/s       Num",
                file=out,
            )
            for i in range(self.NBLK):
                print(
                    " %5d     %10.5f%10.5f%13.2f%11.2f%10d"
                    % (
                        i + 1,
                        self.block[i, 0],
                        self.block[i, 1],
                        self.STEP[i],
                        self.RTIME[i],
                        self.NUM[i],
                    ),
                    file=out,
                )
        print("", file=out)
        if self.ICA == 1:
            print("測定に用いたスケーラ            : CAMAC", file=out)
        if self.ICA == 0:
            print("測定に用いたスケーラ            : ORTEC 974", file=out)
        if self.ICA == -1:
            print("測定に用いたスケーラ            : novice mode", file=out)
        print("ブロック数                      :", self.NBLK, file=out)
        print("測定に用いたデータチャンネルの数:", self.NDCH, file=out)
        print("", file=out)
        print(" " + "Angle(c)  Angle(o)    time/s", file=out, end="")
        if self.ICA == 0:
            for j in range(self.NDCH0, self.NDCH):
                print("%10d" % (j + 1), file=out, end="")
            print("", file=out)
            print(" " + "    Mode         0         0", file=out, end="")
            for j in range(self.NDCH0, self.NDCH):
                print("%10d" % self.MODEM[j], file=out, end="")
            print("", file=out)
            print(" " + "  Offset         0         0", file=out, end="")
            for j in range(self.NDCH0, self.NDCH):
                print("%10.3f" % self.OFFS[j], file=out, end="")
            print("", file=out)
        out.close()

    # write DATA
    def write_pf(self, *args):
        num_args = len(args)
        if num_args >= 1:
            outfile = args[0]
            #               out = codecs.open(outfile,'w','utf-8')
            try:
                out = codecs.open(outfile, "a", "utf-8")
            except:
                out.close()
                sys.exit("STOP:" + outfile + " can'nt open")
        else:
            out = sys.stdout
        print(" %5s     %8s %5s" % (self.IFCD, self.BL0, self.BL), file=out)
        print(" %14s  %14s - %14s" % (self.FN, self.YMD1, self.YMD2), file=out)
        print(" " + self.SAMP, file=out)
        print(
            " Ring : %5.1f GeV  %6.1f mA - %6.1f mA"
            % (self.ERING, self.CRING1, self.CRING2),
            file=out,
        )
        print(
            " Mono :   %10s    D= %8.5f A    Initial angle=%9.5f deg"
            % (self.XTAL, self.D, self.PANG),
            file=out,
        )
        print(
            " %5s    %13s(%2d)   Repetition=%3d     Points=%5d"
            % (self.BL, self.CMODE, self.MODE, self.IREP, self.NPT),
            file=out,
        )
        if self.IAE == 1:
            print(
                " Param file : %14s  angle axis (%1d)     Block =%5d"
                % (self.PFN, self.IAE, self.NBLK),
                file=out,
            )
        if self.IAE == 2:
            print(
                " Param file : %14s  energy axis (%1d)     Block =%5d"
                % (self.PFN, self.IAE, self.NBLK),
                file=out,
            )
        print("", file=out)
        if self.IAE == 1:
            print(
                " "
                + "Block      Init-ang  final-ang     Step/deg     Time/s       Num",
                file=out,
            )
            for i in range(self.NBLK):
                print(
                    " %5d     %10.5f%10.5f%13.6f%11.2f%10d"
                    % (
                        i + 1,
                        self.block[i, 0],
                        self.block[i, 1],
                        self.STEP[i],
                        self.RTIME[i],
                        self.NUM[i],
                    ),
                    file=out,
                )
        if self.IAE == 2:
            print(
                " "
                + "Block      Init-ang  final-Eng     Step/deg     Time/s       Num",
                file=out,
            )
            for i in range(self.NBLK):
                print(
                    " %5d     %10.5f%10.5f%13.2f%11.2f%10d"
                    % (
                        i + 1,
                        self.block[i, 0],
                        self.block[i, 1],
                        self.STEP[i],
                        self.RTIME[i],
                        self.NUM[i],
                    ),
                    file=out,
                )
        if self.ICA > 0:
            self.ICA_CHAR = "CAMCA"
        if self.ICA <= 0:
            self.ICA_CHAR = "Ortec"
        print(
            " %5s(%2d)     NDCH =%2d" % (self.ICA_CHAR, self.ICA, self.NDCH), file=out
        )
        print("  " + "Angle(c)  Angle(o)    time/s", file=out, end="")
        if self.ICA == 0:
            for j in range(self.NDCH0, self.NDCH):
                print("%10d" % (j + 1), file=out, end="")
            print("")
            print("  " + "    Mode         0         0", file=out, end="")
            for j in range(self.NDCH0, self.NDCH):
                print("%10d" % self.MODEM[j], file=out, end="")
            print("", file=out)
            print("  " + "  Offset         0         0", file=out, end="")
            for j in range(self.NDCH0, self.NDCH):
                print("%10.3f" % self.OFFS[j], file=out, end="")
            print("", file=out)
        for i in range(self.NPT):
            print(
                "%10.5f%10.5f%10.3f" % (self.ANGM[i], self.ANGE[i], self.DWT[i]),
                file=out,
                end="",
            )
            for j in range(self.NDCH0, self.NDCH):
                print("%10d" % self.IDTM[i, j], file=out, end="")
            print("", file=out)
