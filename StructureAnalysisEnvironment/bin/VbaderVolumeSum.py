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

    logger = SAE.util.logger.Logger(loglevel='debug')
    op = options()
    atom_list_str = op[0]
    outname = op[1]

    # 引数は string なので int に直す
    atom_list = list(map((lambda x: int(x)), atom_list_str))

    logger.info('')
    logger.info('***************************************')
    logger.info('SUM Bader Volume')
    logger.info(atom_list)
    logger.info(outname)
    logger.info('***************************************')
    logger.info('')

    util = SAE.io.UtilBader(logger=logger)
    chgdata = util.sum_bader_volume(atom_list)
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
    wbv.poscar_info = poscar_info
    wbv.write_bader_volume(outname)


