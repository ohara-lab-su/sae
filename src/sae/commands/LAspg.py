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
import sys
import os
import optparse
import math
import numpy as np
import SpaceGroupEnvironment as SGE


def options():
    cname = "sets.in"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=cname)
    options, args = parser.parse_args()
    if options.INPUT:
        cname = options.INPUT
    if len(args) > 0:
        cname = args[0]
    if not os.path.exists(cname):
        sys.exit(cname + " file not found")
    return cname


if __name__ == "__main__":
    cname = options()
    PI = math.pi
    lattices0 = []
    lattices0.extend(SetsFields().read_sets_param())
    spg_name = lattices0[0]
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
    lattice_a = lattices[0]
    lattice_b = lattices[1]
    lattice_c = lattices[2]
    lattice_alpha = lattices[3]
    lattice_beta = lattices[4]
    lattice_gamma = lattices[5]
    gen_type = []
    gen = []
    spg_n, spg_type, spg_ngen = SGE.read_spgrdata(spg_name, gen_type, gen)
    system = SGE.get_system(lattices, spg_name, spg_type)
    TPMT = np.zeros((3, 3))
    SGE.get_tpmt(system, TPMT)
    TCMT = np.zeros((3, 3))
    SGE.get_tcmt(lattices, TCMT)
    BRMT = np.dot(TCMT, TPMT)
    TIMT = np.linalg.inv(TCMT.T) * 2 * PI
    RCMT = np.linalg.inv(BRMT.T) * 2 * PI
    print("== Space Group Name    :", spg_name)
    print("== Space Group Number  :", spg_n)
    print("== Crystal Type        :", spg_type)
    print("== System              :", system)
    print("== Number of Gen       :", spg_ngen)
    for i in range(spg_ngen):
        print(
            " %2d %2d %2d %2d /%2d"
            % (gen_type[i], gen[i][0], gen[i][1], gen[i][2], gen[i][3])
        )
    print("")
    print("TCMT-MATRIX")
    for i in range(3):
        print(" %10.6f %10.6f %10.6f " % (TCMT[i, 0], TCMT[i, 1], TCMT[i, 2]))
    print("")
    print("TPMT-MATRIX")
    for i in range(3):
        print(" %10.6f %10.6f %10.6f " % (TPMT[i, 0], TPMT[i, 1], TPMT[i, 2]))
    print("")
    print("BRMT-MATRIX")
    for i in range(3):
        print(" %10.6f %10.6f %10.6f " % (BRMT[i, 0], BRMT[i, 1], BRMT[i, 2]))
    print("")
    print("TIMT-MATRIX")
    for i in range(3):
        print(" %10.6f %10.6f %10.6f " % (TIMT[i, 0], TIMT[i, 1], TIMT[i, 2]))
    print("")
    print("RCMT-MATRIX")
    for i in range(3):
        print(" %10.6f %10.6f %10.6f " % (RCMT[i, 0], RCMT[i, 1], RCMT[i, 2]))
    print("")
    for ge in range(spg_ngen):
        for i in range(3):
            TAUROT = np.zeros((3, spg_n))
            for j in range(3):
                TAUROT[i, ge] = TAUROT[j, ge] + TCMT[i, j] * gen[ge][j] / gen[ge][3]
    rotation_xyz = np.array(
        [
            [
                ["+x", "+y", "+z"],
                ["-x", "-y", "+z"],
                ["+x", "-y", "-z"],
                ["-x", "+y", "-z"],
                ["+y", "-x", "+z"],
                ["-y", "+x", "+z"],
                ["+x", "+z", "-y"],
                ["+x", "-z", "+y"],
                ["-z", "+y", "+x"],
                ["+z", "+y", "-x"],
                ["+y", "+x", "-z"],
                ["+z", "-y", "+x"],
                ["-x", "+z", "+y"],
                ["-y", "-x", "-z"],
                ["-z", "-y", "-x"],
                ["-x", "-z", "-y"],
                ["+y", "+z", "+x"],
                ["+z", "+x", "+y"],
                ["-y", "-z", "+x"],
                ["+z", "-x", "-y"],
                ["-y", "+z", "-x"],
                ["-z", "-x", "+y"],
                ["+y", "-z", "-x"],
                ["-z", "+x", "-y"],
                ["-x", "-y", "-z"],
                ["+x", "+y", "-z"],
                ["-x", "+y", "+z"],
                ["+x", "-y", "+z"],
                ["-y", "+x", "-z"],
                ["+y", "-x", "-z"],
                ["-x", "-z", "+y"],
                ["-x", "+z", "-y"],
                ["+z", "-y", "-x"],
                ["-z", "-y", "+x"],
                ["-y", "-x", "+z"],
                ["-z", "+y", "-x"],
                ["+x", "-z", "-y"],
                ["+y", "+x", "+z"],
                ["+z", "+y", "+x"],
                ["+x", "+z", "+y"],
                ["-y", "-z", "-x"],
                ["-z", "-x", "-y"],
                ["+y", "+z", "-x"],
                ["-z", "+x", "+y"],
                ["+y", "-z", "+x"],
                ["+z", "+x", "-y"],
                ["-y", "+z", "+x"],
                ["+z", "-x", "+y"],
            ],
            [
                ["+x", "+y", "+z"],
                ["-x", "-y", "+z"],
                ["+x-y", "+x", "+z"],
                ["+y", "-x+y", "+z"],
                ["-x+y", "-x", "+z"],
                ["-y", "+x-y", "+z"],
                ["+x", "+x-y", "-z"],
                ["-y", "-x", "-z"],
                ["-x+y", "+y", "-z"],
                ["+y", "+x", "-z"],
                ["-x", "-x+y", "-z"],
                ["+x-y", "-y", "-z"],
                ["-x", "-y", "-z"],
                ["+x", "+y", "-z"],
                ["-x+y", "-x", "-z"],
                ["-y", "+x-y", "-z"],
                ["+x-y", "+x", "-z"],
                ["+y", "-x+y", "-z"],
                ["-x", "-x+y", "+z"],
                ["+y", "+x", "+z"],
                ["+x-y", "-y", "+z"],
                ["-y", "-x", "+z"],
                ["+x", "+x-y", "+z"],
                ["-x+y", "+y", "+z"],
            ],
            [
                ["+x", "+y", "+z"],
                ["+y", "+z", "+x"],
                ["+z", "+x", "+y"],
                ["-z", "-y", "-x"],
                ["-y", "-x", "-z"],
                ["-x", "-z", "-y"],
                ["-x", "-y", "-z"],
                ["-y", "-z", "-x"],
                ["-z", "-x", "-y"],
                ["+z", "+y", "+x"],
                ["+y", "+x", "+z"],
                ["+x", "+z", "+y"],
            ],
        ]
    )
    rotation_euler = np.array(
        [
            [
                [0, 0, 0],
                [PI, 0, 0],
                [PI, PI, 0],
                [0, PI, 0],
                [-PI / 2, 0, 0],
                [PI / 2, 0, 0],
                [PI / 2, PI / 2, -PI / 2],
                [-PI / 2, PI / 2, PI / 2],
                [PI, PI / 2, PI],
                [0, PI / 2, 0],
                [-PI / 2, PI, 0],
                [0, PI / 2, PI],
                [PI / 2, PI / 2, PI / 2],
                [PI / 2, PI, 0],
                [PI, PI / 2, 0],
                [-PI / 2, PI / 2, -PI / 2],
                [PI / 2, PI / 2, PI],
                [0, PI / 2, PI / 2],
                [-PI / 2, PI / 2, PI],
                [0, PI / 2, -PI / 2],
                [PI / 2, PI / 2, 0],
                [PI, PI / 2, PI / 2],
                [-PI / 2, PI / 2, 0],
                [PI, PI / 2, -PI / 2],
                [0, 0, 0],
                [PI, 0, 0],
                [PI, PI, 0],
                [0, PI, 0],
                [-PI / 2, 0, 0],
                [PI / 2, 0, 0],
                [PI / 2, PI / 2, -PI / 2],
                [-PI / 2, PI / 2, PI / 2],
                [PI, PI / 2, PI],
                [0, PI / 2, 0],
                [-PI / 2, PI, 0],
                [0, PI / 2, PI],
                [PI / 2, PI / 2, PI / 2],
                [PI / 2, PI, 0],
                [PI, PI / 2, 0],
                [-PI / 2, PI / 2, -PI / 2],
                [PI / 2, PI / 2, PI],
                [0, PI / 2, PI / 2],
                [-PI / 2, PI / 2, PI],
                [0, PI / 2, -PI / 2],
                [PI / 2, PI / 2, 0],
                [PI, PI / 2, PI / 2],
                [-PI / 2, PI / 2, 0],
                [PI, PI / 2, -PI / 2],
            ],
            [
                [0, 0, 0],
                [PI, 0, 0],
                [PI / 3, 0, 0],
                [-PI / 3, 0, 0],
                [-2 * PI / 3, 0, 0],
                [2 * PI / 3, 0, 0],
                [PI, PI, 0],
                [PI / 3, PI, 0],
                [-PI / 3, PI, 0],
                [-2 * PI / 3, PI, 0],
                [0, PI, 0],
                [2 * PI / 3, PI, 0],
                [0, 0, 0],
                [PI, 0, 0],
                [PI / 3, 0, 0],
                [-PI / 3, 0, 0],
                [-2 * PI / 3, 0, 0],
                [2 * PI / 3, 0, 0],
                [PI, PI, 0],
                [PI / 3, PI, 0],
                [-PI / 3, PI, 0],
                [-2 * PI / 3, PI, 0],
                [0, PI, 0],
                [2 * PI / 3, PI, 0],
            ],
            [
                [0, 0, 0],
                [-2 * PI / 3, 0, 0],
                [2 * PI / 3, 0, 0],
                [-2 * PI / 3, PI, 0],
                [2 * PI / 3, PI, 0],
                [0, PI, 0],
                [0, 0, 0],
                [-2 * PI / 3, 0, 0],
                [2 * PI / 3, 0, 0],
                [-2 * PI / 3, PI, 0],
                [2 * PI / 3, PI, 0],
                [0, PI, 0],
            ],
        ]
    )
    rotation_inver = np.array(
        [
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
            ],
            [
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
                -1,
            ],
            [1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1],
        ]
    )
    point_group = 0
    sym = 0
    alpha = rotation_euler[point_group][sym][0]
    beta = rotation_euler[point_group][sym][1]
    gamma = rotation_euler[point_group][sym][2]
    rote_eular = np.zeros((3, 3))
    SGE.make_euler_rotation(alpha, beta, gamma, rote_eular)
    print(rote_eular)
    STD = True
    SetsWriter().print_sets(
        cname,
        STD,
        title,
        nspin,
        spg_name,
        lattices,
        nion,
        sg_atoms,
        sg_atoms_index,
        sg_position,
        kinfo,
        kpoints,
    )
