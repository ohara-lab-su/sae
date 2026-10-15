# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import numpy as np


class Rotations:

    def rotate_z(self, deg):
        r = np.radians(float(deg))
        C = np.cos(r)
        S = np.sin(r)
        R_z = np.matrix(((C, -S, 0), (S, C, 0), (0, 0, 1)))
        return R_z

    def rotate_y(self, deg):
        r = np.radians(float(deg))
        C = np.cos(r)
        S = np.sin(r)
        R_y = np.matrix(((C, 0, S), (0, 1, 0), (-S, 0, C)))
        return R_y

    def rotate_euler(self, alpha, beta, gamma):
        from sae.geometry.rotation import Rotations

        R_alpha_z = Rotations().rotate_z(alpha)
        R_beta_y = Rotations().rotate_y(beta)
        R_gamma_z = Rotations().rotate_z(gamma)
        R_euler = R_alpha_z * R_beta_y * R_gamma_z
        return R_euler
