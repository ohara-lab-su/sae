"""Identical operations in separate processes; OLD is the reference."""

import json
import sys
from pathlib import Path
import numpy as np

mode, case = sys.argv[1:]
new = mode == "new"


def plain(value):
    if isinstance(value, np.ndarray):
        return {
            "dtype": str(value.dtype),
            "shape": list(value.shape),
            "values": plain(value.tolist()),
        }
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if isinstance(value, bytes):
        return {"bytes": value.hex()}
    if isinstance(value, np.generic):
        return plain(value.item())
    if isinstance(value, dict):
        return {k: plain(v) for k, v in value.items()}
    return value


result = {}
if case.startswith("vasp"):
    from sae.vasp.poscar import ReadVaspPoscar
    from sae.structure.writer import StructureWriter

    write = StructureWriter().write
    if new:
        from sae import VASP

        obj = VASP("POSCAR")
        cell = obj.structure
    else:
        obj = cell = ReadVaspPoscar("POSCAR")
    result["rotation"] = obj.conv_rot_euler(0.1, 0.2, 0.3)
    if case == "vasp-convert":
        obj.conv_direct2car()
        obj.conv_scale21()
    if case == "vasp-supercell":
        try:
            obj.conv_supercell((2, 1, 2))
        except ValueError as error:
            result["unchanged_exception"] = str(error)
        for name in (
            "scale",
            "t",
            "position",
            "fix",
            "natom",
            "atoms",
            "ion",
            "direct",
        ):
            result[name] = getattr(cell, name)
        Path("result.json").write_text(
            json.dumps(plain(result), sort_keys=True, indent=2)
        )
        sys.exit(0)
    obj.print_poscar("result.vasp", STD=False)
    for code in ("FDMNES", "OPENMX", "RMC_POT"):
        try:
            if new:
                obj.write(outname="converted_" + code, code=code)
            else:
                write(cell, outname="converted_" + code, code=code)
            result[code] = "ok"
        except (Exception, SystemExit) as error:
            result[code] = {"exception": type(error).__name__, "message": str(error)}
    for name in ("scale", "t", "position", "fix", "natom", "atoms", "ion", "direct"):
        result[name] = getattr(cell, name)
elif case in ("fdmnes-xas", "fdmnes-conv", "fdmnes-output"):
    import importlib
    import shutil
    import sae as original_package

    samples = Path(original_package.__file__).parent / "sample_input"
    for path in samples.glob("Fe*.txt"):
        shutil.copyfile(str(path), path.name)
    entries = {
        "fdmnes-xas": (
            "ReadFdmTxt",
            "read_xas",
            "Fe.txt",
            ["get_eng", "get_xas", "get_efermi"],
        ),
        "fdmnes-conv": (
            "ReadFdmConv",
            "read_convolution",
            "Fe_conv.txt",
            ["get_eng", "get_xas"],
        ),
        "fdmnes-output": (
            "ReadFdmBav",
            "read_output",
            "Fe_bav.txt",
            ["get_nspin", "get_natom", "get_position", "get_t"],
        ),
    }
    name, factory, filename, getters = entries[case]
    try:
        if new:
            from sae import FDMNES

            owner = FDMNES()
            obj = getattr(owner, factory)(filename)
        else:
            raise RuntimeError("This driver runs only the migrated library")
            obj = getattr(module, name)(filename)
        for getter in getters:
            result[getter] = getattr(obj, getter)()
    except (Exception, SystemExit) as error:
        result["unchanged_exception"] = {
            "type": type(error).__name__,
            "message": str(error),
        }
elif case == "fdmnes":
    from ase.io.vasp import read_vasp
    from sae.fdmnes.inp_writer import WriteFdmInp

    atoms = read_vasp("POSCAR")
    if new:
        from sae import FDMNES

        obj = FDMNES()
        obj.prepare_writer(atoms)
    else:
        obj = WriteFdmInp(atoms)
    result["defaults"] = [
        obj.get_radius(),
        obj.get_fileout(),
        obj.get_e_range(),
        obj.get_rmt(),
    ]
    obj.set_radius(6)
    obj.set_rmt(1.5)
    obj.set_fileout("Pd")
    obj.write_fdmnes(name="structure", STD=False, MOL=True)
    obj.write_fdmnes_inp(name="result.inp", absorber=1, radius=6, rmt=1.5, MOL=True)
    result["parameters"] = [obj.get_radius(), obj.get_rmt(), obj.get_fileout()]
elif case.startswith("openmx"):
    from sae.openmx.dat import ReadMxDat
    from sae.structure.writer import StructureWriter

    write = StructureWriter().write
    if new:
        from sae import OpenMX

        obj = OpenMX("case.dat")
        cell = obj.structure
    else:
        obj = cell = ReadMxDat("case.dat")
    for name in ("scale", "t", "position", "fix", "natom", "atoms", "ion", "direct"):
        result[name] = getattr(cell, name)
    if new:
        obj.write(outname="converted", code="VASP")
    else:
        write(cell, outname="converted", code="VASP")
elif case == "hilapw":
    from sae.hilapw.sets import ReadHiSets

    if new:
        from sae import HiLAPW

        obj = HiLAPW("sets.in")
        cell = obj.structure
    else:
        obj = cell = ReadHiSets("sets.in")
    result["title"] = obj.get_title()
    result["position"] = obj.get_position()
    for name in (
        "lattices",
        "atoms",
        "atoms_index",
        "natom",
        "kpoints",
        "sgn",
        "nspin",
    ):
        result[name] = getattr(cell, name)
elif case == "athena":
    from sae.athena.nor import ReadAthenaNor

    if new:
        from sae import Athena

        obj = Athena()
        obj.read_spectrum("case.nor")
    else:
        obj = ReadAthenaNor("case.nor")
    result["initial"] = [obj.get_e0(), obj.get_eng(), obj.get_nor(), obj.get_xas()]
    obj.set_nor(np.array([2.0, 3.0, 4.0]))
    result["changed"] = [obj.get_nor(), obj.get_xas()]
elif case == "pwscf-dos":
    from sae.pwscf.tdos import ReadPwTdos

    if new:
        from sae import PWscf

        obj = PWscf()
        obj.read_tdos("case.dos")
    else:
        obj = ReadPwTdos("case.dos")
    result["dos"] = [obj.get_tdos(0), obj.get_tdos(1)]
else:
    raise ValueError(case)
Path("result.json").write_text(json.dumps(plain(result), sort_keys=True, indent=2))
