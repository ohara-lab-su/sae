#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.rmcpot.cfg_fields import RmcConfigFields
from sae.rmcpot.cfg_writer import RmcConfigWriter

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np

if __name__ == "__main__":
    cname = "igzo_coll"
    nloop, natom, nion = RmcConfigFields().read_cfg_coll_param(cname)
    t = np.zeros((3, 3))
    atoms = np.zeros(nion, dtype=int)
    ion_site = np.zeros(natom, dtype=int)
    position_loop = np.zeros((nloop, natom, 3))
    header, comment, scale, direct = RmcConfigFields().read_cfg_coll(
        cname, nloop, t, natom, nion, atoms, ion_site, position_loop
    )
    for loop in range(nloop):
        name = cname + "_" + str(loop)
        print("split --> " + name)
        position = np.zeros((natom, 3))
        for ion in range(natom):
            position[ion, 0] = position_loop[loop, ion, 0]
            position[ion, 1] = position_loop[loop, ion, 1]
            position[ion, 2] = position_loop[loop, ion, 2]
        STD = False
        RmcConfigWriter().print_rmcpot_cfg(
            name, STD, comment, t, natom, nion, atoms, position
        )
