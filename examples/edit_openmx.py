"""python examples/edit_openmx.py openmx.dat output.dat"""

import argparse
from sae.openmx import Input


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    calculation = Input.read(args.source)
    calculation.set_parameter("scf.maxIter", 200)
    geometry = calculation.structure.translate([0.0, 0.0, 0.1])
    calculation.set_structure(geometry).write(args.destination)


if __name__ == "__main__":
    main()
