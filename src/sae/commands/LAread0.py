#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.hilapw.sets_fields import SetsFields
from sae.hilapw.sets_writer import SetsWriter

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2014, Kengo NAKADA"
__license__ = "MIT"
import numpy as np


def options():
    cname = "sets.in"
    return cname


if __name__ == "__main__":
    cname = options()
    lattices0 = []
    lattices0.extend(SetsFields().read_sets_param())
    sgn_index = lattices0[0]
    nion = lattices0[1]
    sg_natom = lattices0[2]
    lattices = np.zeros(6, dtype=float)
    sg_atoms = np.zeros(nion, dtype=int)
    sg_atoms_index = []
    sg_position = np.zeros((sg_natom, 3), dtype=float)
    kpoints = np.zeros(3, dtype=int)
    title, nspin, kinfo = SetsFields().read_sets(
        cname, lattices, nion, sg_atoms, sg_atoms_index, sg_position, kpoints
    )
    STD = True
    SetsWriter().print_sets(
        cname,
        STD,
        title,
        nspin,
        sgn_index,
        lattices,
        nion,
        sg_atoms,
        sg_atoms_index,
        sg_position,
        kinfo,
        kpoints,
    )
