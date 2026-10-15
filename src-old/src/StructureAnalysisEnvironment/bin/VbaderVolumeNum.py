#!/usr/bin/env python
# coding:utf-8
"""
指定した原子の Bader Volume を抜き出す
"""
import optparse
import StructureAnalysisEnvironment as SAE


def options():
    parser = optparse.OptionParser()
    parser.add_option('-a','--atom', )
    parser.add_option('-d','--debug', default=False)
    options,  args = parser.parse_args()

    ret = [1,2,3]
    if options.atom:
        ret = atom
    if len(args) > 0:
        ret = args
    return [ret, options.debug]


if __name__ == '__main__':

    opts = options()
    atom_list = opts[0]
    debug = opts[1]
    if debug:
        logger = SAE.util.logger.Logger(loglevel='debug')
    else:
        logger = SAE.util.logger.Logger(loglevel='info')

    logger.debug('**************************')
    logger.debug('SUM Bader Volume')
    logger.debug(atom_list)
    logger.debug('**************************')
    logger.debug('')
    volumes = []

    for atom in atom_list:

        # Bader Volume の調査
        logger.debug('=== ReadBaderBcf()')
        bcf = SAE.io.ReadBaderBcf()
        volume_list = bcf.search_atomic_volume_num(atom)

    try:
        volume_list
    except:
        pass
    else:
        for i in volume_list:
            print("%s " % i, end="")
        print("")