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
import sys
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
    INCAR, KPOINTS, POSCAR, CONTCAR = VasprunFields().read_vasprun0(XMLFILE)
    (
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t_initial,
        atoms,
        atoms_index,
        position_initial,
        fix_initial,
    ) = POSCAR
    (
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        VASP,
        t_final,
        atoms,
        atoms_index,
        position_final,
        fix_final,
    ) = CONTCAR
    INCAR_TAG, INCAR_TEXT = INCAR
    try:
        out = open("INCAR.rebuild", "w")
        print("Makes INCAR.rebuild")
        for i in range(len(INCAR_TAG)):
            print(INCAR_TAG[i], "=", INCAR_TEXT[i], file=out)
    except:
        out.close()
        sys.exit("STOP: INCAR.rebuild can't open")
    finally:
        out.close()
    try:
        out = open("KPOINTS.rebuild", "w")
        print("Makes KPOINTS.rebuild")
        for i in range(len(KPOINTS)):
            print(KPOINTS[i], file=out)
    except:
        out.close()
        sys.exit("STOP: KPOINTS.rebuild can't open")
    finally:
        out.close()
    print("Makes POSCAR.rebuild")
    STD = False
    cname = "POSCAR.rebuild"
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
        t_initial,
        atoms,
        atoms_index,
        position_initial,
        fix_initial,
    )
    print("Makes CONTCAR.rebuild")
    STD = False
    cname = "CONTCAR.rebuild"
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
        t_final,
        atoms,
        atoms_index,
        position_final,
        fix_final,
    )
