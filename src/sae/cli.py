"""Small code-specific CLI; scientific operations remain on library objects."""

import argparse
import json
import sys
from sae.errors import SAEError


def main(argv=None):
    parser = argparse.ArgumentParser(prog="sae")
    commands = parser.add_subparsers(dest="code", required=True)
    for code in ("openmx", "hilapw", "vasp"):
        sub = commands.add_parser(code)
        actions = sub.add_subparsers(dest="action", required=True)
        inspect = actions.add_parser("inspect", help="show input geometry/settings")
        inspect.add_argument("path")
        if code == "vasp":
            inspect.add_argument(
                "--species", nargs="+", help="species for VASP 4 files"
            )
        if code == "openmx":
            edit = actions.add_parser("set", help="set one input parameter")
            edit.add_argument("path")
            edit.add_argument("name")
            edit.add_argument("value")
            edit.add_argument("output")
            edit.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.code == "openmx":
            from sae.openmx import Input

            doc = Input.read(args.path)
            if args.action == "set":
                doc.set_parameter(args.name, args.value).write(
                    args.output, overwrite=args.overwrite
                )
                return 0
            data = {
                "code": "OpenMX",
                "system": doc.get_parameter("System.Name"),
                "species": doc.species,
                "sites": len(doc.structure),
                "volume_angstrom3": doc.structure.volume,
            }
        elif args.code == "hilapw":
            from sae.hilapw import Input

            doc = Input.read(args.path)
            data = {
                "code": "HiLAPW",
                "title": doc.title,
                "nspin": doc.nspin,
                "space_group": doc.space_group,
                "listed_sites": len(doc.sites),
                "lattice_parameters_native": doc.lattice_parameters.tolist(),
                "kpoints": doc.kpoints.tolist(),
            }
        else:
            from sae.vasp import Poscar

            doc = Poscar.read(args.path, species=args.species)
            data = {
                "code": "VASP",
                "title": doc.title,
                "sites": len(doc.structure),
                "volume_angstrom3": doc.structure.volume,
            }
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except (SAEError, ValueError, OSError) as error:
        print("sae: {}".format(error), file=sys.stderr)
        return 2
