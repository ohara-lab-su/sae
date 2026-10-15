from sae.bader.bcf import ReadBaderBcf
from sae.common.logger import Logger
#!/usr/bin/env python
# coding:utf-8
"""[summary]
Li の体積を持つ BVAt*.dat を Li フォルダ以下に移動する
(整理確認用)
"""
import os
import shutil


if __name__ == '__main__':
    loglevel = 'info'
    logger = Logger(loglevel=loglevel)

    BVA = 'BvAt'
    dist_dir = 'Li'
    # poscar の順番
    num_P = 27
    num_S = 108
    num_Li = 104

    atom_list = range(num_P + num_S + 1, num_P + num_S + num_Li + 1)
    print(list(atom_list))
    v_list = []
    for atom in atom_list:
        bcf = ReadBaderBcf()
        volume_list = bcf.search_atomic_volume_num(atom)
        if len(volume_list) > 1:
            print("****** volume_list > 1")
            print(volume_list)
        else:
            v_list.append(volume_list[0])

    num_v_list = len(v_list)
    print(num_v_list)
    print(v_list)

    # os.makedirs(dist_dir, exist_ok=True)

    # for volume in v_list:
    #     a = "{:04}".format(volume)
    #     chgname = "%s%s.dat" % (BVA, a)
    #     new_name = "CHGCAR_%s%s.dat" % (BVA, a)
    #     # print(chgname)
    #     shutil.move(chgname, "%s/%s" % (dist_dir, new_name) )
