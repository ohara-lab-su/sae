from sae.fdmnes.inp_writer import WriteFdmInp
#!/usr/bin/env python
"""
FDMNES のパラメーターを変えて連続実行する
Rmt 半径の変更

1) POSCAR 情報読み込み
2) FDMNES パラメーターセット
3) FDMNES INP 書き出し
4) FDMNES 実行
"""

import os
import shutil
import subprocess
from subprocess import PIPE

from ase.io.vasp import *


command = "fdmnes"
fdm_inp = "read_pdb.inp"
fdm_file = "fdmfile.txt"
base_name = "Pd"
fileout = "Pd"

folder_prefix = "Rmt_"
absorber = 1

Rmt_list = [
    1.4,
    1.5,
    1.6,
    1.7,
]

cwd = os.getcwd()
poscar = cwd + "/POSCAR"

for Rmt in Rmt_list:
    print("")

    # フォルダの作成
    folder_name = folder_prefix + str(Rmt)
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    print("=================================== %s (%s)" % (Rmt, folder_name))

    # POSCAR ファイルを読み込み
    atoms = read_vasp(poscar)
    fdm = WriteFdmInp(atoms)

    # fdmfile を フォルダにコピー
    print("copy fdmfile to %s" % folder_name)
    shutil.copy2(fdm_file, folder_name)

    fdm.write_fdmnes(name="POSCAR", MOL=True)
    fdm.write_fdmnes(name=folder_name + "/POSCAR", STD=False, MOL=True)
    fdm.write_fdmnes_inp(
        name=folder_name + "/" + fdm_inp,
        absorber=absorber,
        fileout=fileout,
        e_range="-15. 0.2  0. 0.5 10. 1. 80.",
        radius=5,
        rmt=Rmt,
        MOL=True,
    )

    # RUN FDMNES
    # 同期（終わるまで次に進まない）
    # 作業フォルダ work にて作業する
    print("**** RUN FDMNES ***")
    proc = subprocess.run(
        command, cwd=folder_name, shell=True, stdout=PIPE, stderr=PIPE, text=True
    )
    date = proc.stdout
    print("STDOUT: {}".format(date))
