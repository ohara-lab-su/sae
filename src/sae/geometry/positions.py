# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
from numpy import *


class PositionOperations:

    def move_atoms1(self, scale, t, direct, position, nlist, list_atoms):
        if direct:
            sys.exit("STOP: direct mode")
        for i in range(nlist):
            atom = int(list_atoms[i, 0]) - 1
            new_x = list_atoms[i, 1] / scale
            new_y = list_atoms[i, 2] / scale
            new_z = list_atoms[i, 3] / scale
            position[atom, 0] = position[atom, 0] + new_x
            position[atom, 1] = position[atom, 1] + new_y
            position[atom, 2] = position[atom, 2] + new_z
        return scale

    def move_atoms0(self, scale, t, direct, position, nlist, list_atoms):
        if direct:
            sys.exit("STOP: direct mode")
        for i in range(nlist):
            atom = int(list_atoms[i, 0]) - 1
            new_x = list_atoms[i, 1]
            new_y = list_atoms[i, 2]
            new_z = list_atoms[i, 3]
            position[atom, 0] = position[atom, 0] + new_x
            position[atom, 1] = position[atom, 1] + new_y
            position[atom, 2] = position[atom, 2] + new_z
        return scale
