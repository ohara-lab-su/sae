# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os


class RmcConfigWriter:

    def print_rmcpot_cfg(
        self,
        cname,
        STD,
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        vasp_version,
        t,
        atoms,
        atoms_index,
        position,
        fix,
    ):
        from sae.geometry.coordinates import CoordinateTransforms
        from sae.rmcpot.cfg_writer import RmcConfigWriter
        from sae.rmcpot.conversion import RmcConversions

        scale, t, natom, direct, position = CoordinateTransforms().conv_scale21(
            scale, t, natom, direct, position
        )
        if not direct:
            scale, t, natom, direct, position = CoordinateTransforms().conv_car2direct(
                scale, t, natom, direct, position
            )
        scale, t, natom, direct, position = RmcConversions().conv_vasp2cfg(
            scale, t, natom, direct, position
        )
        RmcConfigWriter().print_rmcpot_cfg_raw(
            cname, STD, title, t, natom, nion, atoms, position
        )

    def print_rmcpot_cfg_raw(self, cname, STD, title, t, natom, nion, atoms, position):
        t1_x = t[0, 0]
        t1_y = t[1, 0]
        t1_z = t[2, 0]
        t2_x = t[0, 1]
        t2_y = t[1, 1]
        t2_z = t[2, 1]
        t3_x = t[0, 2]
        t3_y = t[1, 2]
        t3_z = t[2, 2]
        if STD:
            out = sys.stdout
        else:
            cfg = open(cname + ".cfg", "w")
        print(title, file=cfg)
        print(cname, file=cfg)
        print("", file=cfg)
        print("", file=cfg)
        moves = 0
        tried = 0
        accepted = 0
        saved = 0
        print("        ", moves, "        ", tried, "        ", accepted, file=cfg)
        print("        ", saved, "        ", "configurations saved", file=cfg)
        print("", file=cfg)
        print("        ", natom, " ", "molecules of all types", file=cfg)
        print("        ", nion, " ", "types of molecules", file=cfg)
        print(
            "        ",
            "1",
            " ",
            "is the largest number of atoms in a molecule",
            file=cfg,
        )
        print("        ", "0", " ", "Euler angles are provided", file=cfg)
        print("", file=cfg)
        print("        ", "F (box is cubic)\t", file=cfg)
        print("        ", "  Defining vectors are:", file=cfg)
        print("        ", "  %13.9f %13.9f %13.9f" % (t1_x, t1_y, t1_z), file=cfg)
        print("        ", "  %13.9f %13.9f %13.9f" % (t2_x, t2_y, t2_z), file=cfg)
        print("        ", "  %13.9f %13.9f %13.9f" % (t3_x, t3_y, t3_z), file=cfg)
        print("", file=cfg)
        for j in range(int(nion)):
            print("        ", atoms[j], " ", "molecules of types  ", j + 1, file=cfg)
            print("        ", "1", " ", "atomic sites", file=cfg)
            print("        ", "     ", "0.000000   0.000000   0.000000", file=cfg)
            print("", file=cfg)
        for j in range(natom):
            print(
                "%15.12f %15.12f %15.12f"
                % (position[j, 0], position[j, 1], position[j, 2]),
                file=cfg,
            )
        cfg.close()
