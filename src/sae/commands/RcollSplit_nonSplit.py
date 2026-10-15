#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.rmcpot.cfg_fields import RmcConfigFields
import numpy as np

if __name__ == "__main__":
    cname = "igzo_coll"
    nloop, natom, nion = RmcConfigFields().read_cfg_coll_param(cname)
    t = np.zeros((3, 3))
    atoms = np.zeros(nion, dtype=int)
    atoms_site = np.zeros(natom, dtype=int)
    position_loop = np.zeros((nloop, natom, 3))
    RmcConfigFields().read_cfg_coll(
        cname, nloop, t, natom, nion, atoms, atoms_site, position_loop
    )
