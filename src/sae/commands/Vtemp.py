#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import sys
import os

if __name__ == "__main__":
    name_out = "OUTCAR"
    name_osz = "OSZICAR"
    module_name = "sae._class_registry"
    if os.path.exists(name_osz) or os.path.exists(name_osz + ".gz"):
        class_name = "ReadVaspOszicar"
        name = name_osz
    else:
        class_name = "ReadVaspOutcar"
        name = name_out
    try:
        module = __import__(module_name, globals(), locals(), [class_name], 0)
    except:
        module = __import__(module_name, fromlist=[class_name])
    klass = getattr(module, class_name)
    outfile = klass(name)
    t_FLAG = outfile.get_md_mode()
    if not t_FLAG:
        sys.exit("STOP: current is non MD mode")
    temperature = outfile.get_temperature()
    etotal = outfile.get_etotal()
    n_ion_loop = outfile.get_n_ion_loop()
    for i in range(n_ion_loop):
        print("%5d %6.2f  %15.8f" % (i + 1, temperature[i], etotal[i]))
