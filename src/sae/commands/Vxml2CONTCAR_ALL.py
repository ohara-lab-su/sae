#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.vasp.poscar_writer import PoscarWriter
from sae.vasp.vasprun_fields import VasprunFields

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import optparse


def options():
    XMLFILE = "vasprun.xml"
    parser = optparse.OptionParser()
    parser.add_option("-i", "--input", dest="INPUT", default=XMLFILE)
    options, args = parser.parse_args()
    if options.INPUT:
        XMLFILE = options.INPUT
    if len(args) > 0:
        XMLFILE = args[0]
    return XMLFILE


if __name__ == "__main__":
    XMLFILE = options()
    n_ion_loop, CONTCAR_ALL = VasprunFields().read_vasprun1(XMLFILE)
    (
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t_loop,
        atoms,
        atoms_index,
        position_loop,
        fix_final,
    ) = CONTCAR_ALL
    print("Numver of ION-LOOP:", n_ion_loop)
    for ion_loop in range(n_ion_loop):
        print("Makes CONTCAR." + str(ion_loop + 1) + ".rebuild")
        t = t_loop[:, :, ion_loop]
        position = position_loop[:, :, ion_loop]
        fix = fix_final
        STD = False
        cname = "CONTCAR." + str(ion_loop + 1) + ".rebuild"
        PoscarWriter().print_poscar(
            cname,
            STD,
            title,
            scale,
            natom,
            nion,
            selective,
            direct,
            VASP,
            t,
            atoms,
            atoms_index,
            position,
            fix,
        )
