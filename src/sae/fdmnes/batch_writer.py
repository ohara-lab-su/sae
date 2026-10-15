from sae.errors import legacy_error as _legacy_error

#!/usr/bin/env python
# coding:utf-8
"""
fdmfile.txt の作成
項目が 1 個のみ
"""
import sys

# 固定
FDMFILE = "fdmfile.txt"


class BatchWriter(object):
    def __init__(self, inpname="read_pdb.inp"):
        if inpname is not None:
            self.__inpname = inpname

    def write_fdmfile(self, prefix=None, inpname=None):
        """
        :param prefix:  fdmfile.txt の作成場所
        :param inpname:  読み込まれる INP ファイル名
        :return:
        """
        if prefix is None:
            fdmfile = FDMFILE
        else:
            fdmfile = prefix + "/" + FDMFILE

        if inpname is None:
            inpname = self.__inpname

        try:
            out = open(fdmfile, "w")
        except:
            out.close()
            _legacy_error("STOP:" + fdmfile + "file can't open")

        print("! General indata file for FDMNES", file=out)
        print("", file=out)
        print("  1", file=out)
        print("%s" % inpname)


WriteFdmfile = BatchWriter  # historical spelling
