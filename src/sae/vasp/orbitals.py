# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function


class VaspOrbitals:

    def get_vasp_orbital_info(self, lm):
        orbital_list = [
            "s",
            "p_y",
            "p_z",
            "p_x",
            "d_xy",
            "d_yz",
            "d_3z3-r2",
            "d_xz",
            "d_x2-y2",
        ]
        orbital = orbital_list[lm]
        return orbital
