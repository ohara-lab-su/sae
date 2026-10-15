# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import optparse
import xml.etree.ElementTree as ET
import numpy as np
import math


class VasprunWriter:

    def print_vasprun0(
        self,
        OUTPUT,
        title,
        nloop,
        natom,
        nion,
        atoms,
        atoms_index,
        atoms_index_j,
        t,
        position_loop,
        force_loop,
        energy_loop,
    ):
        PI = math.pi
        SYSTEM = str(title)
        modeling = ET.Element("modeling")
        incar = ET.SubElement(modeling, "incar")
        systemtag = ET.SubElement(incar, "i", {"name": "SYSTEM", "type": "string"})
        systemtag.text = SYSTEM
        ibriontag = ET.SubElement(incar, "i", {"name": "IBRION", "type": "int"})
        ibriontag.text = "2"
        parameters = ET.SubElement(modeling, "parameters")
        separator = ET.SubElement(parameters, "separator", {"name": "general"})
        systemtag = ET.SubElement(separator, "i", {"type": "string", "name": "SYSTEM"})
        systemtag.text = SYSTEM
        atominfo = ET.SubElement(modeling, "atominfo")
        atomstag = ET.SubElement(atominfo, "atoms")
        atomstag.text = str(natom)
        typestag = ET.SubElement(atominfo, "types")
        typestag.text = str(nion)
        array = ET.SubElement(atominfo, "array", {"name": "atoms"})
        dimension = ET.SubElement(array, "dimension", {"dim": "1"})
        dimension.text = "ion"
        field = ET.SubElement(array, "field", {"type": "string"})
        field.text = "element"
        field = ET.SubElement(array, "field", {"type": "int"})
        field.text = "atomtype"
        settag = ET.SubElement(array, "set")
        for i in range(nion):
            for j in range(atoms[i]):
                rc = ET.SubElement(settag, "rc")
                c = ET.SubElement(rc, "c")
                c.text = str(atoms_index[i])
                c = ET.SubElement(rc, "c")
                c.text = str(i + 1)
        array = ET.SubElement(atominfo, "array", {"name": "atomtypes"})
        dimension = ET.SubElement(array, "dimension", {"dim": "1"})
        dimension.text = "type"
        field = ET.SubElement(array, "field", {"type": "int"})
        field.text = "atomspertype"
        field = ET.SubElement(array, "field", {"type": "string"})
        field.text = "element"
        field = ET.SubElement(array, "field")
        field.text = "mass"
        field = ET.SubElement(array, "field")
        field.text = "valence"
        field = ET.SubElement(array, "field", {"type": "string"})
        field.text = "pseudopotential"
        settag = ET.SubElement(array, "set")
        for i in range(nion):
            rc = ET.SubElement(settag, "rc")
            c = ET.SubElement(rc, "c")
            c.text = str(atoms[i])
            c = ET.SubElement(rc, "c")
            c.text = str(atoms_index[i])
            c = ET.SubElement(rc, "c")
            c.text = str(1.0)
            c = ET.SubElement(rc, "c")
            c.text = str(1.0)
            c = ET.SubElement(rc, "c")
            c.text = str("PAW dummy")
        structure = ET.SubElement(modeling, "structure", {"name": "initialpos"})
        crystal = ET.SubElement(structure, "crystal")
        varray = ET.SubElement(crystal, "varray", {"name": "basis"})
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 0])
            + "   {0:.8f}".format(t[1, 0])
            + "   {0:.8f}".format(t[2, 0])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 1])
            + "   {0:.8f}".format(t[1, 1])
            + "   {0:.8f}".format(t[2, 1])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 2])
            + "   {0:.8f}".format(t[1, 2])
            + "   {0:.8f}".format(t[2, 2])
        )
        volume = ET.SubElement(crystal, "i", {"name": "volume"})
        volume.text = "{0:.8f}".format(t[0, 0] * t[1, 1] * t[2, 2])
        t_rec = np.linalg.inv(t) * 2 * PI
        varray = ET.SubElement(crystal, "varray", {"name": "rec_basis"})
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 0])
            + "   {0:.8f}".format(t_rec[1, 0])
            + "   {0:.8f}".format(t_rec[2, 0])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 1])
            + "   {0:.8f}".format(t_rec[1, 1])
            + "   {0:.8f}".format(t_rec[2, 1])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 2])
            + "   {0:.8f}".format(t_rec[1, 2])
            + "   {0:.8f}".format(t_rec[2, 2])
        )
        varray = ET.SubElement(structure, "varray", {"name": "positions"})
        for atom in range(natom):
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(position_loop[0, atom, 0])
                + "   {0:.8f}".format(position_loop[0, atom, 1])
                + "   {0:.8f}".format(position_loop[0, atom, 2])
            )
        for loop in range(nloop):
            calculation = ET.SubElement(modeling, "calculation")
            structure = ET.SubElement(calculation, "structure")
            crystal = ET.SubElement(structure, "crystal")
            varray = ET.SubElement(crystal, "varray", {"name": "basis"})
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t[0, 0])
                + "   {0:.8f}".format(t[1, 0])
                + "   {0:.8f}".format(t[2, 0])
            )
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t[0, 1])
                + "   {0:.8f}".format(t[1, 1])
                + "   {0:.8f}".format(t[2, 1])
            )
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t[0, 2])
                + "   {0:.8f}".format(t[1, 2])
                + "   {0:.8f}".format(t[2, 2])
            )
            t_rec = np.linalg.inv(t) * 2 * PI
            varray = ET.SubElement(crystal, "varray", {"name": "rec_basis"})
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t_rec[0, 0])
                + "   {0:.8f}".format(t_rec[1, 0])
                + "   {0:.8f}".format(t_rec[2, 0])
            )
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t_rec[0, 1])
                + "   {0:.8f}".format(t_rec[1, 1])
                + "   {0:.8f}".format(t_rec[2, 1])
            )
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(t_rec[0, 2])
                + "   {0:.8f}".format(t_rec[1, 2])
                + "   {0:.8f}".format(t_rec[2, 2])
            )
            varray = ET.SubElement(structure, "varray", {"name": "positions"})
            for atom in range(natom):
                v = ET.SubElement(varray, "v")
                v.text = (
                    "{0:.8f}".format(position_loop[loop, atom, 0])
                    + "   {0:.8f}".format(position_loop[loop, atom, 1])
                    + "   {0:.8f}".format(position_loop[loop, atom, 2])
                )
            varray = ET.SubElement(calculation, "varray", {"name": "forces"})
            for atom in range(natom):
                v = ET.SubElement(varray, "v")
                v.text = (
                    "{0:.8f}".format(force_loop[loop, atom, 0])
                    + "   {0:.8f}".format(force_loop[loop, atom, 1])
                    + "   {0:.8f}".format(force_loop[loop, atom, 2])
                )
            e0 = 0.0
            energy = ET.SubElement(calculation, "energy")
            e_fr_energy = ET.SubElement(energy, "i", {"name": "e_fr_energy"})
            e_fr_energy.text = "{0:.8f}".format(energy_loop[loop])
            e_wo_entrp = ET.SubElement(energy, "i", {"name": "e_wo_entrp"})
            e_wo_entrp.text = "{0:.8f}".format(energy_loop[loop])
            e_0_energy = ET.SubElement(energy, "i", {"name": "e_0_energy"})
            e_0_energy.text = "{0:.8f}".format(e0)
        structure = ET.SubElement(modeling, "structure", {"name": "finalpos"})
        crystal = ET.SubElement(structure, "crystal")
        varray = ET.SubElement(crystal, "varray", {"name": "basis"})
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 0])
            + "   {0:.8f}".format(t[1, 0])
            + "   {0:.8f}".format(t[2, 0])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 1])
            + "   {0:.8f}".format(t[1, 1])
            + "   {0:.8f}".format(t[2, 1])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t[0, 2])
            + "   {0:.8f}".format(t[1, 2])
            + "   {0:.8f}".format(t[2, 2])
        )
        volume = ET.SubElement(crystal, "i", {"name": "volume"})
        volume.text = "{0:.8f}".format(t[0, 0] * t[1, 1] * t[2, 2])
        t_rec = np.linalg.inv(t) * 2 * PI
        varray = ET.SubElement(crystal, "varray", {"name": "rec_basis"})
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 0])
            + "   {0:.8f}".format(t_rec[1, 0])
            + "   {0:.8f}".format(t_rec[2, 0])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 1])
            + "   {0:.8f}".format(t_rec[1, 1])
            + "   {0:.8f}".format(t_rec[2, 1])
        )
        v = ET.SubElement(varray, "v")
        v.text = (
            "{0:.8f}".format(t_rec[0, 2])
            + "   {0:.8f}".format(t_rec[1, 2])
            + "   {0:.8f}".format(t_rec[2, 2])
        )
        varray = ET.SubElement(structure, "varray", {"name": "positions"})
        for atom in range(natom):
            v = ET.SubElement(varray, "v")
            v.text = (
                "{0:.8f}".format(position_loop[nloop - 1, atom, 0])
                + "   {0:.8f}".format(position_loop[nloop - 1, atom, 1])
                + "   {0:.8f}".format(position_loop[nloop - 1, atom, 2])
            )
        tree = ET.ElementTree(modeling)
        tree.write(OUTPUT, method="xml")
