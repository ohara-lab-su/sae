#!/usr/bin/env python
"""
FDMNES のパラメーターを変えて連続実行する

1) POSCAR 情報読み込み
2) FDMNES パラメーターセット
3) FDMNES INP 書き出し
4) FDMNES 実行
"""

import os
import shutil
from typing import AsyncIterator
import subprocess
from subprocess import PIPE

from ase.io.vasp import *
import StructureAnalysisEnvironment as SAE

command = 'fdmnes'
fdm_inp = 'read_pdb.inp'
fdm_file = 'fdmfile.txt'
base_name = "Pd"
fileout = 'Pd'

cluster_list = [
    "Pd02",
    "Pd03",
    "Pd04",
    "Pd05",
    "Pd06",
    "Pd07",
    "Pd13",
    "Pd19",
]

for folder in cluster_list:
    print('')
    print('==============================', folder)
    suffix = folder.replace(base_name, "")
    num = int(suffix)

    # folder にある POSCAR ファイルを読み込み
    atoms = read_vasp(folder + "/POSCAR")
    fdm = SAE.io.WriteFdmInp(atoms)

    # fdmfile を Pd02 フォルダにコピー
    shutil.copy2(fdm_file, folder)

    # copy input file
    for absorber in range(1, num + 1):
        # アブソーバーフォルダ名
        ab_folder = 'absorber_' + "{:02}".format(absorber)

        # クラスー毎のさらにアブソーバー毎の作業フォルダ
        work = folder + '/' + ab_folder

        if not os.path.exists(work):
            os.makedirs(work)
        print('')
        print('==============================', work)

        # Pd02 などのクラスターフォルダーにある POSCAR を absorber folder へコピー
        shutil.copy2(folder + "/POSCAR", work)

        # fdmnes.txt ファイルのコピー
        shutil.copy2(folder + "/" + fdm_file, work)

        fdm.write_fdmnes(name='POSCAR', MOL=True)
        fdm.write_fdmnes(name=work + '/POSCAR', STD=False, MOL=True)
        fdm.write_fdmnes_inp(
            name=work + '/' + fdm_inp,
            absorber=absorber,
            fileout=fileout,
            e_range="-15. 0.2  0. 0.5 10. 1. 80.",
            radius=5,
            MOL=True)

        # RUN FDMNES
        # 同期（終わるまで次に進まない）
        # 作業フォルダ work にて作業する
        print('**** RUN FDMNES ***')
        proc = subprocess.run(command, cwd=work, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        date = proc.stdout
        print('STDOUT: {}'.format(date))
