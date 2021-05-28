#!/usr/bin/env python
# coding:utf-8
"""
指定した原子の Bader Volume を抜き出して、足し合わせる
原子は複数指定可能で、足し合わせる。
つまり「原子種」ごとなどの好きなグループ毎に Bader Volume を出せる
"""
import optparse
import StructureAnalysisEnvironment as SAE


def options():
    parser = optparse.OptionParser()
    parser.add_option('-a','--atom', )
    options,  args = parser.parse_args()

    ret = [1,2,3]
    if options.atom:
        ret = atom
    if len(args) > 0:
        ret = args
    return ret


if __name__ == '__main__':

    atom_list = options()
    print('**************************')
    print('SUM Bader Volume')
    print(atom_list)
    print('**************************')
    volumes = []

    for atom in atom_list:

        # Bader Volume の調査
        print('=== ReadBaderBcf()')
        bcf = SAE.io.ReadBaderBcf()
        volume_list = bcf.search_atomic_volume_num(atom)
        print("volume list = %s" % atom, end="")
        print(volume_list)

        # Bader Volume の足し合わせ
        util = SAE.io.UtilBader()
        util.sum_bader_volume(volume_list)
        volumes.append(util.bader_volume)
        poscar_info = util.poscar_info
        del util

    for atom in atom_list:
        try:
            chgdata = chgdata + volumes[int(atom)]
        except:
            chgdata = volumes[int(atom)]

    # Bader Volume の書き出し1G
    wbv = SAE.io.WriteBaderVolume()
    wbv.chgdata = chgdata
    wbv.poscar_info = poscar_info
    wbv.write_bader_volume('CHGCAR_BvA_SUM')


