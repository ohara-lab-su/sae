#!/usr/bin/env python
# coding:utf-8
"""[summary]
Li の体積を持つ BVAt*.dat を Li フォルダ以下に移動する
Bader 体積を足し合わせる

(整理確認用)
"""
import os
import shutil
import StructureAnalysisEnvironment as SAE

if __name__ == '__main__':
    loglevel = 'debug'
    logger = SAE.util.logger.Logger(loglevel=loglevel)

    BVA = 'BvAt'
    dist_dir = 'Li'
    # poscar の順番

    # 46LiI
    # num_P = 27
    # num_S = 108
    # num_Li = 104

    # Li7P3S11
    # num_P = 6
    # num_S = 22
    # num_Li = 14

    # yamada_mm
    num_P = 405
    num_S = 1620
    num_Li = 1215

    atom_list = range(num_P + num_S + 1, num_P + num_S + num_Li + 1)
    # atom_list = [1, 2] # test
    # atom_list = [136, 137]  # test

    # util = SAE.io.UtilBader(logger=logger)
    util = SAE.io.UtilBader(logger=logger)
    chgdata = util.sum_bader_volume(atom_list, split_chgcar=True)

    ngx_max = util.ngx_max
    ngy_max = util.ngy_max
    ngz_max = util.ngz_max
    poscar_info = util.poscar_info

    # Bader Volume の書き出し
    wbv = SAE.io.WriteBaderVolume(logger=logger)
    wbv.chgdata = chgdata
    wbv.ngx_max = ngx_max
    wbv.ngy_max = ngy_max
    wbv.ngz_max = ngz_max

    # print(chgdata)
    # print(type(chgdata))
    # print(chgdata.shape)
    # print(type(chgdata[0,0,139]))

    wbv.poscar_info = poscar_info
    # wbv.write_bader_volume('CHGCAR_Li')
    wbv.write_bader_volume('CHGCAR_Li_136_137')
