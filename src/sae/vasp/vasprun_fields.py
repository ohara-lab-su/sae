# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import gzip
import xml.etree.ElementTree as ET
import numpy as np
import optparse


class VasprunFields:

    def read_vasprun0(self, XMLFILE):
        if os.path.exists(XMLFILE):
            f = XMLFILE
            ZIP_FLAG = False
        elif os.path.exists(XMLFILE + ".gz"):
            f = gzip.open(XMLFILE + ".gz")
            ZIP_FLAG = True
        else:
            sys.exit("STOP: " + XMLFILE + " or " + XMLFILE + ".gz file not found")
        try:
            tree = ET.parse(f)
        except:
            if ZIP_FLAG:
                sys.exit("can't parse " + XMLFILE + ".gz")
            else:
                sys.exit("can't parse " + XMLFILE)
        finally:
            if ZIP_FLAG:
                f.close()
        root = tree.getroot()
        program = root.findtext("generator/i[@name='program']")
        version = root.findtext("generator/i[@name='version']")
        subversion = root.findtext("generator/i[@name='subversion']")
        SYSTEM = root.findtext("incar/i[@name='SYSTEM']")
        INCAR_TAG = []
        INCAR_TEXT = []
        for i in root.find("incar"):
            INCAR_TAG.append(i.attrib.get("name"))
            INCAR_TEXT.append(i.text)
        INCAR = [INCAR_TAG, INCAR_TEXT]
        generation = root.find("kpoints/generation").get("param")
        divition = root.find("kpoints/generation/v[@name='divisions']").text
        KPOINTS = []
        KPOINTS.append("K-POINTS")
        KPOINTS.append("0")
        KPOINTS.append(generation)
        KPOINTS.append(divition)
        for es in root.find("kpoints/varray[@name='kpointlist']"):
            KPOINTS.append(es.text)
        n_ion_loop = len(root.findall("calculation"))
        natom = int(root.findtext("atominfo/atoms"))
        nion = int(root.findtext("atominfo/types"))
        atoms = np.zeros(nion, dtype=int)
        atoms_index = np.zeros(nion, dtype="S2")
        number = 0
        local_nion = 1
        for es in root.findall("atominfo/array[@name='atoms']/set/rc"):
            index_FLAG = True
            for rc in es:
                if index_FLAG:
                    name = str(rc.text)
                    index_FLAG = False
                else:
                    number_tmp = int(rc.text)
                    if number_tmp == number:
                        local_nion += 1
                    else:
                        local_nion = 1
                        number = number_tmp
            atoms[number - 1] = local_nion
            atoms_index[number - 1] = name
        t_initial = np.zeros((3, 3))
        j = 0
        for e in root.find(
            "structure[@name='initialpos']/crystal/varray[@name='basis']"
        ):
            tmp = e.text.split()
            t_initial[0, j] = tmp[0]
            t_initial[1, j] = tmp[1]
            t_initial[2, j] = tmp[2]
            j += 1
        position_initial = np.zeros((natom, 3))
        j = 0
        for e in root.find("structure[@name='initialpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_initial[j, 0] = tmp[0]
            position_initial[j, 1] = tmp[1]
            position_initial[j, 2] = tmp[2]
            j += 1
        fix_initial = np.zeros((natom, 3), dtype="S")
        selective = False
        if root.find("structure[@name='initialpos']").findall(
            "varray[@name='selective']"
        ):
            selective = True
        if selective:
            j = 0
            for e in root.find(
                "structure[@name='initialpos']/varray[@name='selective']"
            ):
                tmp = e.text.split()
                fix_initial[j, 0] = str(tmp[0])
                fix_initial[j, 1] = str(tmp[1])
                fix_initial[j, 2] = str(tmp[2])
                j += 1
        t_final = np.zeros((3, 3))
        j = 0
        for e in root.find("structure[@name='finalpos']/crystal/varray[@name='basis']"):
            tmp = e.text.split()
            t_final[0, j] = tmp[0]
            t_final[1, j] = tmp[1]
            t_final[2, j] = tmp[2]
            j += 1
        position_final = np.zeros((natom, 3))
        j = 0
        for e in root.find("structure[@name='finalpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_final[j, 0] = tmp[0]
            position_final[j, 1] = tmp[1]
            position_final[j, 2] = tmp[2]
            j += 1
        fix_final = np.zeros((natom, 3), dtype="S")
        selective = False
        if root.find("structure[@name='finalpos']").findall(
            "varray[@name='selective']"
        ):
            selective = True
        if selective:
            j = 0
            for e in root.find("structure[@name='finalpos']/varray[@name='selective']"):
                tmp = e.text.split()
                fix_final[j, 0] = str(tmp[0])
                fix_final[j, 1] = str(tmp[1])
                fix_final[j, 2] = str(tmp[2])
                j += 1
        title = SYSTEM
        scale = 1.0
        VASP = 5
        direct = True
        POSCAR = [
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
        ]
        CONTCAR = [
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
        ]
        return [INCAR, KPOINTS, POSCAR, CONTCAR]

    def read_vasprun1(self, XMLFILE):
        if os.path.exists(XMLFILE):
            f = XMLFILE
            ZIP_FLAG = False
        elif os.path.exists(XMLFILE + ".gz"):
            f = gzip.open(XMLFILE + ".gz")
            ZIP_FLAG = True
        else:
            sys.exit("STOP: " + XMLFILE + " or " + XMLFILE + ".gz file not found")
        try:
            tree = ET.parse(f)
        except:
            if ZIP_FLAG:
                sys.exit("can't parse " + XMLFILE + ".gz")
            else:
                sys.exit("can't parse " + XMLFILE)
        finally:
            if ZIP_FLAG:
                f.close()
        root = tree.getroot()
        program = root.findtext("generator/i[@name='program']")
        version = root.findtext("generator/i[@name='version']")
        subversion = root.findtext("generator/i[@name='subversion']")
        SYSTEM = root.findtext("incar/i[@name='SYSTEM']")
        n_ion_loop = len(root.findall("calculation"))
        natom = int(root.findtext("atominfo/atoms"))
        nion = int(root.findtext("atominfo/types"))
        atoms = np.zeros(nion, dtype=int)
        atoms_index = np.zeros(nion, dtype="S2")
        number = 0
        local_nion = 1
        for es in root.findall("atominfo/array[@name='atoms']/set/rc"):
            index_FLAG = True
            for rc in es:
                if index_FLAG:
                    name = str(rc.text)
                    index_FLAG = False
                else:
                    number_tmp = int(rc.text)
                    if number_tmp == number:
                        local_nion += 1
                    else:
                        local_nion = 1
                        number = number_tmp
            atoms[number - 1] = local_nion
            atoms_index[number - 1] = name
        fix_final = np.zeros((natom, 3), dtype="S")
        selective = False
        if root.find("structure[@name='finalpos']").findall(
            "varray[@name='selective']"
        ):
            selective = True
        if selective:
            j = 0
            for e in root.find("structure[@name='finalpos']/varray[@name='selective']"):
                tmp = e.text.split()
                fix_final[j, 0] = str(tmp[0])
                fix_final[j, 1] = str(tmp[1])
                fix_final[j, 2] = str(tmp[2])
                j += 1
        t_loop = np.zeros((3, 3, n_ion_loop))
        ion_loop = 0
        for cal in root.findall("calculation/structure/crystal/varray[@name='basis']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                t_loop[0, j, ion_loop] = tmp[0]
                t_loop[1, j, ion_loop] = tmp[1]
                t_loop[2, j, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        ion_loop = 0
        position_loop = np.zeros((natom, 3, n_ion_loop))
        for cal in root.findall("calculation/structure/varray[@name='positions']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                position_loop[j, 0, ion_loop] = tmp[0]
                position_loop[j, 1, ion_loop] = tmp[1]
                position_loop[j, 2, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        title = SYSTEM
        scale = 1.0
        VASP = 5
        direct = True
        CONTCAR_ALL = [
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
        ]
        return [n_ion_loop, CONTCAR_ALL]

    def read_vasprun2(self, XMLFILE):
        if os.path.exists(XMLFILE):
            f = XMLFILE
            ZIP_FLAG = False
        elif os.path.exists(XMLFILE + ".gz"):
            f = gzip.open(XMLFILE + ".gz")
            ZIP_FLAG = True
        else:
            sys.exit("STOP: " + XMLFILE + " or " + XMLFILE + ".gz file not found")
        try:
            tree = ET.parse(f)
        except:
            if ZIP_FLAG:
                sys.exit("can't parse " + XMLFILE + ".gz")
            else:
                sys.exit("can't parse " + XMLFILE)
        finally:
            if ZIP_FLAG:
                f.close()
        root = tree.getroot()
        program = root.findtext("generator/i[@name='program']")
        version = root.findtext("generator/i[@name='version']")
        subversion = root.findtext("generator/i[@name='subversion']")
        SYSTEM = root.findtext("incar/i[@name='SYSTEM']")
        INCAR_TAG = []
        INCAR_TEXT = []
        for i in root.find("incar"):
            INCAR_TAG.append(i.attrib.get("name"))
            INCAR_TEXT.append(i.text)
        INCAR = [INCAR_TAG, INCAR_TEXT]
        generation = root.find("kpoints/generation").get("param")
        divition = root.find("kpoints/generation/v[@name='divisions']").text
        KPOINTS = []
        KPOINTS.append("K-POINTS")
        KPOINTS.append("0")
        KPOINTS.append(generation)
        KPOINTS.append(divition)
        for es in root.find("kpoints/varray[@name='kpointlist']"):
            KPOINTS.append(es.text)
        n_ion_loop = len(root.findall("calculation"))
        natom = int(root.findtext("atominfo/atoms"))
        nion = int(root.findtext("atominfo/types"))
        atoms = np.zeros(nion, dtype=int)
        atoms_index = np.zeros(nion, dtype="S2")
        number = 0
        local_nion = 1
        for es in root.findall("atominfo/array[@name='atoms']/set/rc"):
            index_FLAG = True
            for rc in es:
                if index_FLAG:
                    name = str(rc.text)
                    index_FLAG = False
                else:
                    number_tmp = int(rc.text)
                    if number_tmp == number:
                        local_nion += 1
                    else:
                        local_nion = 1
                        number = number_tmp
            atoms[number - 1] = local_nion
            atoms_index[number - 1] = name
        t_initial = np.zeros((3, 3))
        j = 0
        for e in root.find(
            "structure[@name='initialpos']/crystal/varray[@name='basis']"
        ):
            tmp = e.text.split()
            t_initial[0, j] = tmp[0]
            t_initial[1, j] = tmp[1]
            t_initial[2, j] = tmp[2]
            j += 1
        position_initial = np.zeros((natom, 3))
        j = 0
        for e in root.find("structure[@name='initialpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_initial[j, 0] = tmp[0]
            position_initial[j, 1] = tmp[1]
            position_initial[j, 2] = tmp[2]
            j += 1
        fix_initial = np.zeros((natom, 3), dtype="S")
        selective = False
        if root.find("structure[@name='initialpos']").findall(
            "varray[@name='selective']"
        ):
            selective = True
        if selective:
            j = 0
            for e in root.find(
                "structure[@name='initialpos']/varray[@name='selective']"
            ):
                tmp = e.text.split()
                fix_initial[j, 0] = str(tmp[0])
                fix_initial[j, 1] = str(tmp[1])
                fix_initial[j, 2] = str(tmp[2])
                j += 1
        t_final = np.zeros((3, 3))
        j = 0
        for e in root.find("structure[@name='finalpos']/crystal/varray[@name='basis']"):
            tmp = e.text.split()
            t_final[0, j] = tmp[0]
            t_final[1, j] = tmp[1]
            t_final[2, j] = tmp[2]
            j += 1
        position_final = np.zeros((natom, 3))
        j = 0
        for e in root.find("structure[@name='finalpos']/varray[@name='positions']"):
            tmp = e.text.split()
            position_final[j, 0] = tmp[0]
            position_final[j, 1] = tmp[1]
            position_final[j, 2] = tmp[2]
            j += 1
        fix_final = np.zeros((natom, 3), dtype="S")
        selective = False
        if root.find("structure[@name='finalpos']").findall(
            "varray[@name='selective']"
        ):
            selective = True
        if selective:
            j = 0
            for e in root.find("structure[@name='finalpos']/varray[@name='selective']"):
                tmp = e.text.split()
                fix_final[j, 0] = str(tmp[0])
                fix_final[j, 1] = str(tmp[1])
                fix_final[j, 2] = str(tmp[2])
                j += 1
        t_loop = np.zeros((3, 3, n_ion_loop))
        ion_loop = 0
        for cal in root.findall("calculation/structure/crystal/varray[@name='basis']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                t_loop[0, j, ion_loop] = tmp[0]
                t_loop[1, j, ion_loop] = tmp[1]
                t_loop[2, j, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        ion_loop = 0
        position_loop = np.zeros((natom, 3, n_ion_loop))
        for cal in root.findall("calculation/structure/varray[@name='positions']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                position_loop[j, 0, ion_loop] = tmp[0]
                position_loop[j, 1, ion_loop] = tmp[1]
                position_loop[j, 2, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        ion_loop = 0
        force_loop = np.zeros((natom, 3, n_ion_loop))
        for cal in root.findall("calculation/varray[@name='forces']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                force_loop[j, 0, ion_loop] = tmp[0]
                force_loop[j, 1, ion_loop] = tmp[1]
                force_loop[j, 2, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        ion_loop = 0
        stress_loop = np.zeros((natom, 3, n_ion_loop))
        for cal in root.findall("calculation/varray[@name='stress']"):
            j = 0
            for e in cal:
                tmp = e.text.split()
                stress_loop[j, 0, ion_loop] = tmp[0]
                stress_loop[j, 1, ion_loop] = tmp[1]
                stress_loop[j, 2, ion_loop] = tmp[2]
                j += 1
            ion_loop += 1
        e_wo_entrp_loop = np.zeros(n_ion_loop)
        e_fr_energy_loop = np.zeros(n_ion_loop)
        i = 0
        for e in root.findall("calculation/energy/i[@name='e_wo_entrp']"):
            e_wo_entrp_loop[i] = e.text
            i += 1
        i = 0
        for e in root.findall("calculation/energy/i[@name='e_fr_energy']"):
            e_fr_energy_loop[i] = e.text
            i += 1
        title = SYSTEM
        scale = 1.0
        VASP = 5
        direct = True
        ENERGY_ALL = [e_wo_entrp_loop, e_fr_energy_loop]
        FORCE_ALL = [force_loop, stress_loop]
        POSCAR = [
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
        ]
        CONTCAR = [
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
        ]
        CONTCAR_ALL = [
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
        ]
        return [n_ion_loop, POSCAR, CONTCAR, CONTCAR_ALL, FORCE_ALL, ENERGY_ALL]
