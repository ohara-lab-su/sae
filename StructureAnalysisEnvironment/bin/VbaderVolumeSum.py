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
    parser.add_option('-o','--outname', default='CHGCAR_BvA_SUM',)
    options,  args = parser.parse_args()

    ret = [1,2,3]
    if options.atom:
        ret = atom
    if len(args) > 0:
        ret = args
    return [ret, options.outname]


if __name__ == '__main__':

    op = options()
    atom_list = op[0]
    outname = op[1]
    print('')
    print('***************************************')
    print('SUM Bader Volume')
    print(atom_list)
    print(outname)
    print('***************************************')
    print('')
    volumes = []

    for atom in atom_list:

        # Bader Volume の調査
        print('======================== ReadBaderBcf()')
        # bcf = SAE.io.ReadBaderBcf()
        # volume_list = bcf.search_atomic_volume_num(atom)
        avf = SAE.io.ReadBaderAvf()
        volume_list = avf.search_atomic_volume_num(atom)
        print("volume list = %s" % atom, end="")
        print(volume_list)

        # Bader Volume の足し合わせ
        util = SAE.io.UtilBader()
        util.sum_bader_volume(volume_list)
        volumes.append(util.bader_volume)
        poscar_info = util.poscar_info
        del util

    i = 0
    for atom in atom_list:
        try:
            chgdata = chgdata + volumes[i]
        except:
            chgdata = volumes[i]
        i += 1

    # Bader Volume の書き出し1G
    wbv = SAE.io.WriteBaderVolume()
    wbv.chgdata = chgdata
    wbv.poscar_info = poscar_info
    wbv.write_bader_volume(outname)


