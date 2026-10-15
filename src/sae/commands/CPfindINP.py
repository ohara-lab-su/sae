#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.common.paths import FileDiscovery

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse

if __name__ == "__main__":
    suffix = "inp"
    parser = optparse.OptionParser()
    parser.add_option("-s", "--suffix")
    options, args = parser.parse_args()
    if len(args) > 0:
        suffix = args[0]
    if options.suffix:
        suffix = options.suffix
    try:
        datname = FileDiscovery().find_datfile(suffix)
        print(datname)
    except:
        pass
