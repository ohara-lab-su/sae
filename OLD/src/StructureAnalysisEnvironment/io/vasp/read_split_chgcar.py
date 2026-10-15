#!/usr/bin/env python
# 主にテスト用
# BvAt ファイルを、構造情報と 原子情報を分ける
# 2022/03/14

import sys
import os

try:
    # sys.path.append('../..')
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import StructureAnalysisEnvironment as SAE
    from StructureAnalysisEnvironment.Method import Method
except ImportError:
    import StructureAnalysisEnvironment as SAE
    from StructureAnalysisEnvironment.Method import Method

try:
    from ...copyright import *
except Exception:
    from StructureAnalysisEnvironment.copyright import *


head = '_POSCAR'
foot = '_BvAt2026.dat'

# Header 部分の取り出し
header = SAE.io.ReadVaspChgcarHeader(head)
header_data = header.get_poscar_info()

# Footer
chgcar = SAE.io.ReadVaspChgcarFooter(foot, header_data)

print(chgcar.title)
print(chgcar.scale)
print(chgcar.t)
print(chgcar.vasp_version)
print(chgcar.nion)
print(chgcar.atoms)
print(chgcar.atoms_index)
print(chgcar.natom)
print(chgcar.selective)
print(chgcar.direct)
print('----')
print(chgcar.get_poscar_info())
