# Copyright Kengo NAKADA; SAE class library.
import sys
import os


class StructureWriter:

    def write(
        self,
        cell,
        outname=None,
        suffix=None,
        code="VASP",
        calinfo=None,
        sort=False,
        STD=False,
        MOL=False,
        FRAC=True,
    ):
        from sae.fdmnes.structure_writer import FdmnesStructureWriter
        from sae.openmx.dat_writer import OpenMXInputWriter
        from sae.pwscf.inp_writer import PWscfInputWriter
        from sae.rmcpot.cfg_writer import RmcConfigWriter
        from sae.structure.calculation_settings import CalculationSettings
        from sae.vasp.poscar_writer import PoscarWriter

        if code.upper() == "VASP":
            if outname is None:
                outname = "POSCAR"
            if cell.vasp_version is None:
                cell.vasp_version = 5
            PoscarWriter().print_poscar(
                outname,
                STD,
                cell.title,
                cell.scale,
                cell.natom,
                cell.nion,
                cell.selective,
                cell.direct,
                cell.vasp_version,
                cell.t,
                cell.atoms,
                cell.atoms_index,
                cell.position,
                cell.fix,
            )
        if code.upper() == "FDMNES" or code.upper() == "FDM":
            if outname is None:
                outname = "read_pdb.inp"
            FdmnesStructureWriter().print_fdmnes1(
                outname=outname, cell=cell, STD=STD, MOL=MOL
            )
            if not STD:
                FdmnesStructureWriter().print_fdmnes_inp1(
                    outname=outname, cell=cell, MOL=MOL
                )
        if code.upper() == "OPENMX" or code.upper() == "MX":
            if outname is None:
                outname = "openemx"
            if calinfo is not None:
                NSW, NELM, IBRION, EDIFF, EDIFFG, KP = (
                    CalculationSettings().get_calinfo(code=calinfo)
                )
            else:
                NSW = None
                NELM = None
                IBRION = None
                EDIFF = None
                EDIFFG = None
                KP = None
            OpenMXInputWriter().print_mx_dat(
                outname,
                STD,
                cell.title,
                cell.scale,
                cell.natom,
                cell.nion,
                cell.selective,
                cell.direct,
                cell.vasp_version,
                cell.t,
                cell.atoms,
                cell.atoms_index,
                cell.position,
                cell.fix,
                cell.atoms_index_j,
                NSW=NSW,
                NELM=NELM,
                IBRION=IBRION,
                EDIFF=EDIFF,
                EDIFFG=EDIFFG,
                KP=KP,
                FRAC=FRAC,
            )
        if (
            code.upper() == "RMC_POT"
            or code.upper() == "RMC"
            or code.upper() == "RMCPOT"
        ):
            if outname is None:
                outname = "rmcpot"
            RmcConfigWriter().print_rmcpot_cfg(
                outname,
                STD,
                cell.title,
                cell.scale,
                cell.natom,
                cell.nion,
                cell.selective,
                cell.direct,
                cell.vasp_version,
                cell.t,
                cell.atoms,
                cell.atoms_index,
                cell.position,
                cell.fix,
            )
        if (
            code.upper() == "PWSCF"
            or code.upper() == "QE"
            or code.upper() == "QUANTUMESPRESSO"
        ):
            if outname is None:
                outname = "scf.in"
            PWscfInputWriter().print_pwscf_scf(
                outname,
                STD,
                cell.title,
                cell.scale,
                cell.natom,
                cell.nion,
                cell.selective,
                cell.direct,
                cell.vasp_version,
                cell.t,
                cell.atoms,
                cell.atoms_index,
                cell.position,
                cell.fix,
                cell.atoms_index_j,
            )
