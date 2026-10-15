# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from ase.io.wien2k import *
from ase import Atoms
import sys
import numpy as np


class FdmnesStructureWriter:

    def print_fdmnes(self, outname="POSCAR", atoms=None, STD=True, MOL=False):
        return

    def print_fdmnes0(self, outname="POSCAR", atoms=None, STD=True, MOL=False):
        from sae.geometry.coordinates import CoordinateTransforms

        if STD:
            out = sys.stdout
        else:
            try:
                out = open(outname + ".fdmnes", "w")
            except:
                out.close()
                sys.exit("STOP:" + outname + ".fdmnes file can't open")
        a, b, c, alpha, beta, gamma, nat = CoordinateTransforms().conv_cellparam0(atoms)
        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)
        print(
            "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma),
            file=out,
        )
        for ii in range(nat):
            zzn = atoms.get_atomic_numbers()[ii]
            pos = atoms.get_scaled_positions()[ii]
            sym = atoms.get_chemical_symbols()[ii]
            print(
                "   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym),
                file=out,
            )
        if not STD:
            out.close()

    def print_fdmnes1(self, outname="POSCAR", cell=None, STD=True, MOL=False):
        from sae.geometry.coordinates import CoordinateTransforms

        if STD:
            out = sys.stdout
        else:
            try:
                out = open(outname + ".fdmnes", "w")
            except:
                out.close()
                sys.exit("STOP:" + outname + ".fdmnes file can't open")
        a, b, c, alpha, beta, gamma, nat = CoordinateTransforms().conv_cellparam1(cell)
        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)
        print(
            "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma),
            file=out,
        )
        for ii in range(nat):
            zzn = cell.atoms_number_j[ii]
            pos = cell.position[ii, :]
            sym = cell.atoms_index_j[ii]
            print(
                "   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym),
                file=out,
            )
        if not STD:
            out.close()

    def print_fdmnes_inp(self, outname="read_pdb.inp", atoms=None, MOL=False):
        return

    def print_fdmnes_inp0(self, outname="read_pdb.inp", atoms=None, MOL=False):
        from sae.geometry.coordinates import CoordinateTransforms

        try:
            out = open(outname, "w")
        except:
            out.close()
            sys.exit("STOP:" + outname + ".fdmnes file can't open")
        a, b, c, alpha, beta, gamma, nat = CoordinateTransforms().conv_cellparam0(atoms)
        print("! FDMNES indata file", file=out)
        print("", file=out)
        print("!Nonexc", file=out)
        print("", file=out)
        print(" Absorber", file=out)
        print("  1", file=out)
        print("! allsite", file=out)
        print("", file=out)
        print(" Filout", file=out)
        print("  Cu", file=out)
        print("", file=out)
        print(
            " Range                        ! Energy range of calculation (eV)", file=out
        )
        print(
            "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy",
            file=out,
        )
        print("! -15. 0.1 50. 1. 200.        !", file=out)
        print("", file=out)
        print("!Energpho", file=out)
        print("", file=out)
        print(" Edge", file=out)
        print("  K", file=out)
        print("! L23", file=out)
        print("", file=out)
        print("!Quadrupole", file=out)
        print("", file=out)
        print(" Relativism", file=out)
        print("", file=out)
        print(" Convolution", file=out)
        print("", file=out)
        print("!No_Fermi", file=out)
        print("!Efermi", file=out)
        print("!  -6.0", file=out)
        print("!Estart", file=out)
        print("! -10.0", file=out)
        print("", file=out)
        print("!SCF", file=out)
        print("!R_self", file=out)
        print("! 5.0", file=out)
        print("!N_self", file=out)
        print("! 100", file=out)
        print("!P_self", file=out)
        print("! 0.05", file=out)
        print("!Delta_E_conv", file=out)
        print("! 0.01", file=out)
        print("", file=out)
        print("!Magnetism", file=out)
        print("!SCF_mag_free", file=out)
        print("", file=out)
        print("!Hubbard", file=out)
        print("! 0.0 6.3 0.0", file=out)
        print("", file=out)
        print("!TDDFT", file=out)
        print("", file=out)
        print("!Green", file=out)
        print("", file=out)
        print(
            " Radius                       ! Radius of the cluster where final state calculation is performed",
            file=out,
        )
        print(
            "   5.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems",
            file=out,
        )
        print("", file=out)
        print(" Memory_save", file=out)
        print("", file=out)
        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)
        print(
            "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma),
            file=out,
        )
        for ii in range(nat):
            zzn = atoms.get_atomic_numbers()[ii]
            pos = atoms.get_scaled_positions()[ii]
            sym = atoms.get_chemical_symbols()[ii]
            print(
                "   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym),
                file=out,
            )
        print("", file=out)
        print(" Density", file=out)
        print("  state_all", file=out)
        print("", file=out)
        print("!Adimp", file=out)
        print("! 0.20", file=out)
        print("", file=out)
        print(" End", file=out)
        print("", file=out)
        out.close()

    def print_fdmnes_inp1(self, outname="read_pdb.inp", cell=None, MOL=False):
        from sae.geometry.coordinates import CoordinateTransforms

        try:
            out = open(outname, "w")
        except:
            out.close()
            sys.exit("STOP:" + outname + ".fdmnes file can't open")
        a, b, c, alpha, beta, gamma, nat = CoordinateTransforms().conv_cellparam1(cell)
        print("! FDMNES indata file", file=out)
        print("", file=out)
        print("!Nonexc", file=out)
        print("", file=out)
        print(" Absorber", file=out)
        print("  1", file=out)
        print("! allsite", file=out)
        print("", file=out)
        print(" Filout", file=out)
        print("  Cu", file=out)
        print("", file=out)
        print(
            " Range                        ! Energy range of calculation (eV)", file=out
        )
        print(
            "  -15. 0.2  0. 0.5 10. 1. 45. ! first energy, step, intermediary energy, step ..., last energy",
            file=out,
        )
        print("! -15. 0.1 50. 1. 200.        !", file=out)
        print("", file=out)
        print("!Energpho", file=out)
        print("", file=out)
        print(" Edge", file=out)
        print("  K", file=out)
        print("! L23", file=out)
        print("", file=out)
        print("!Quadrupole", file=out)
        print("", file=out)
        print(" Relativism", file=out)
        print("", file=out)
        print(" Convolution", file=out)
        print("", file=out)
        print("!No_Fermi", file=out)
        print("!Efermi", file=out)
        print("!  -6.0", file=out)
        print("!Estart", file=out)
        print("! -10.0", file=out)
        print("", file=out)
        print("!SCF", file=out)
        print("!R_self", file=out)
        print("! 5.0", file=out)
        print("!N_self", file=out)
        print("! 100", file=out)
        print("!P_self", file=out)
        print("! 0.05", file=out)
        print("!Delta_E_conv", file=out)
        print("! 0.01", file=out)
        print("", file=out)
        print("!Magnetism", file=out)
        print("!SCF_mag_free", file=out)
        print("", file=out)
        print("!Hubbard", file=out)
        print("! 0.0 6.3 0.0", file=out)
        print("", file=out)
        print("!TDDFT", file=out)
        print("", file=out)
        print("!Green", file=out)
        print("", file=out)
        print(
            " Radius                       ! Radius of the cluster where final state calculation is performed",
            file=out,
        )
        print(
            "   5.0                         ! For a good calculation, this radius must be increased up to 6 or 7 Angstroems",
            file=out,
        )
        print("", file=out)
        print(" Memory_save", file=out)
        print("", file=out)
        if MOL:
            print(" molecule", file=out)
        else:
            print(" Crystal", file=out)
        print(
            "      %8.4f %8.4f %8.4f %8.4f %8.4f %8.4f" % (a, b, c, alpha, beta, gamma),
            file=out,
        )
        for ii in range(nat):
            zzn = cell.atoms_number_j[ii]
            pos = cell.position[ii, :]
            sym = cell.atoms_index_j[ii]
            print(
                "   %2d %8.4f %8.4f %8.4f    ! %s" % (zzn, pos[0], pos[1], pos[2], sym),
                file=out,
            )
        print("", file=out)
        print(" Density", file=out)
        print("  state_all", file=out)
        print("", file=out)
        print("!Adimp", file=out)
        print("! 0.20", file=out)
        print("", file=out)
        print(" End", file=out)
        print("", file=out)
        out.close()
