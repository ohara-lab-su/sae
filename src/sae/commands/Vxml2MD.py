#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
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
    vasprun = VasprunFields().read_vasprun2(XMLFILE)
    n_ion_loop, POSCAR, CONTCAR, CONTCAR_ALL, FORCE_ALL, ENERGY_ALL = vasprun
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
    e_wo_entrp_loop, e_fr_energy_loop = ENERGY_ALL
    force_loop, stress_loop = FORCE_ALL
    t = t_loop[:, :, n_ion_loop - 1]
    position = position_loop[:, :, n_ion_loop - 1]
    for ion_loop in range(n_ion_loop):
        pass
        t = t_loop[:, :, ion_loop]
        position = position_loop[:, :, ion_loop]
        force = force_loop[:, :, ion_loop]
        e_wo_entrp = e_wo_entrp_loop[ion_loop]
        j = 0
        print(natom)
        print("   setp=     ", ion_loop + 1, "     ", "  Energy=", e_wo_entrp)
        for ion in range(nion):
            for atom in range(atoms[ion]):
                print(
                    "   %2s %12.8f %12.8f %12.8f  %12.8f %12.8f %12.8f"
                    % (
                        atoms_index[ion],
                        position[j, 0],
                        position[j, 1],
                        position[j, 2],
                        force[j, 0],
                        force[j, 1],
                        force[j, 2],
                    )
                )
                j += 1
