"""python examples/edit_hilapw.py sets.in revised.in"""

import argparse
from sae.hilapw import Input


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source")
    parser.add_argument("destination")
    args = parser.parse_args()
    calculation = Input.read(args.source)
    calculation.set_kpoints([8, 8, 8]).write(args.destination)


if __name__ == "__main__":
    main()
