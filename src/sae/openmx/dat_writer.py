# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import sys
import os
import re
import numpy as np


class OpenMXInputWriter:

    def print_mx_dat(
        self,
        datname,
        STD,
        title,
        scale,
        natom,
        nion,
        selective,
        direct,
        vasp_version,
        t,
        atoms,
        atoms_index,
        position,
        fix,
        atoms_index_j,
        NSW=None,
        NELM=None,
        IBRION=None,
        EDIFF=None,
        EDIFFG=None,
        KP=None,
        FRAC=True,
    ):
        from sae.geometry.coordinates import CoordinateTransforms
        from sae.openmx.vps import ReadMxVps
        from sae.openmx.vps_list import ReadMxVpsList

        if vasp_version is None:
            vasp_version = 5
        if KP:
            kx = KP[0:0]
            ky = KP[0:1]
            kz = KP[0:2]
        version_FLAG = False
        if sys.version_info[0] >= 2 and sys.version_info[1] >= 7:
            version_FLAG = True
        DATAPATH = os.environ.get("OPENMXDATAPATH", "")
        if not DATAPATH:
            print("can't found OPENMXDATAPATH environment on yuur system")
            print("please export OPENMXDATAPATH=~/DFT_DATA13")
            print("STOP")
            sys.exit()
        VPSLIST = "openmx_defaults_vpsdata.list"
        DFT_DATA = "DFT_DATA13"
        data = "../" + DFT_DATA
        pot = "PBE"
        ver = "13"
        if not os.path.exists(data):
            data = DATAPATH
        print("DATA PATH %s" % str(data))
        vpspath = data + "/VPS/"
        paopath = data + "/PAO/"
        HOMEPATH = os.environ.get("HOME", "")
        if os.path.exists(VPSLIST):
            vpslistpath = VPSLIST
        elif os.path.exists(data + "/" + VPSLIST):
            vpslistpath = data + "/" + VPSLIST
        elif os.path.exists(HOMEPATH + "/" + DFT_DATA + "/" + VPSLIST):
            vpslistpath = HOMEPATH + "/openmx2/" + DFT_DATA + "/" + VPSLIST
        elif os.path.exists(HOMEPATH + "/openmx1/" + VPSLIST):
            vpslistpath = HOMEPATH + "/openmx1/" + VPSLIST
        else:
            sys.exit("STOP: " + VPSLIST + " file not found")
        OUT = datname
        datfile = open(OUT + ".dat", "w")
        if not STD:
            sys.stdout = datfile
        if direct and (not FRAC):
            (
                scale,
                t,
                natom,
                direct,
                position,
            ) = CoordinateTransforms().conv_direct2carABS(
                scale, t, natom, direct, position
            )
        scale, t, natom, direct, position = CoordinateTransforms().conv_scale21(
            scale, t, natom, direct, position
        )
        vpslist = ReadMxVpsList(vpslistpath)
        electron = np.zeros(natom)
        for j in range(natom):
            num, symbol, cutoff, vps_orbit = vpslist.get_vps_name(atoms_index_j[j])
            opt = re.sub("[0-9\\.]+", "", cutoff)
            fullname = vpspath + symbol + "_" + pot + ver + opt + ".vps"
            vpsfile = ReadMxVps(fullname)
            electron[j] = vpsfile.get_valence_electron() / 2.0
        print("###########################################")
        print("# File Name")
        print("###########################################")
        print("")
        print("System.CurrentDirectory            ./   # default=./")
        print("System.Name                       %s" % str(title))
        print("level.of.stdout                    1    # default=1 (1-3)")
        print("level.of.fileout                   1    # default=1 (0-2)")
        print("DATA.PATH                        %s" % str(data))
        print("")
        print("###########################################")
        print("# Definition of Atomic Species")
        print("#    name PAO VPS")
        print("#    Cu   Cu6.0S-s3p3d3 Cu_PBE13S")
        print("###########################################")
        print("")
        print("Species.Number %s" % str(nion))
        print("<Definition.of.Atomic.Species")
        for i in range(nion):
            atom = re.sub("_.*", "", atoms_index[i])
            atoms_index[i] = atom
            num, symbol, cutoff, vps_orbit = vpslist.get_vps_name(atoms_index[i])
            opt = re.sub("[0-9\\.]+", "", cutoff)
            vps_name = symbol + cutoff + "-" + vps_orbit
            vps_file = vpspath + symbol + "_" + pot + ver + opt + ".vps"
            pao_file = paopath + symbol + cutoff + ".pao"
            if not os.path.exists(pao_file):
                sys.exit("STOP: " + pao_file + " not found")
            if not os.path.exists(vps_file):
                sys.exit("STOP: " + vps_file + " not found")
            vps0 = symbol + cutoff + "-" + vps_orbit
            pao0 = symbol + "_" + pot + ver + opt
            print("  %2s  %13s  %13s " % (symbol, vps0, pao0))
        print("Definition.of.Atomic.Species>")
        print("")
        print("#<Hubbard.U.values                 #  eV")
        print("# Ni  1s 0.0 2s 0.0 1p 0.0 2p 0.0 1d 4.0 2d 0.0")
        print("# O   1s 0.0 2s 0.0 1p 0.0 2p 0.0 1d 0.0")
        print("#Hubbard.U.values>")
        print("")
        print("###########################################")
        print("# Atom")
        print("#    num, name, x,y,z,  up-spin, down-spin")
        print("###########################################")
        print("")
        print("Atoms.Number %s" % str(natom))
        if FRAC:
            print("Atoms.SpeciesAndCoordinates.Unit  FRAC  # Ang|AU|FRAC")
            print("<Atoms.SpeciesAndCoordinates            # Unit=FRAC")
        else:
            print("Atoms.SpeciesAndCoordinates.Unit  Ang   # Ang|AU|FRAC")
            print("<Atoms.SpeciesAndCoordinates            # Unit=Ang.")
        for i in range(natom):
            atom = re.sub("_.*", "", atoms_index_j[i])
            atoms_index_j[i] = atom
            if not version_FLAG:
                print(
                    "%4d  %2s %12.8f %12.8f %12.8f  %12.8f  %12.8f "
                    % (
                        i + 1,
                        atoms_index_j[i],
                        position[i][0],
                        position[i][1],
                        position[i][2],
                        electron[i],
                        electron[i],
                    )
                )
            else:
                myStr = "{:>4}  {:^2} {:12f}  {:12f}  {:12f}   {:12f}  {:12f}"
                print(
                    myStr.format(
                        i + 1,
                        atoms_index_j[i],
                        position[i][0],
                        position[i][1],
                        position[i][2],
                        electron[i],
                        electron[i],
                    )
                )
        print("Atoms.SpeciesAndCoordinates>")
        print("Atoms.UnitVectors.Unit            Ang   # Ang|AU")
        print("<Atoms.UnitVectors                      # Unit=Ang.")
        print("   %12.8f %12.8f %12.8f" % (t[0][0], t[1][0], t[2][0]))
        print("   %12.8f %12.8f %12.8f" % (t[0][1], t[1][1], t[2][1]))
        print("   %12.8f %12.8f %12.8f" % (t[0][2], t[1][2], t[2][2]))
        print("Atoms.UnitVectors>")
        print("")
        print("###########################################")
        print("# SCF or Electronic System")
        print("###########################################")
        print("")
        print("#scf.restart                On")
        print("")
        print("scf.XcType                 GGA-PBE     # LDA|LSDA-CA|LSDA-PW|GGA-PBE")
        print("scf.SpinPolarization       Off         # On|Off|NC")
        print("#scf.SpinOrbit.Coupling     Off         # On|Off")
        print("scf.ElectronicTemperature  300.0       # default=300 (K)")
        print("")
        print("scf.energycutoff           150.0       # default=150 (Ry)")
        print("#scf.Ngrid                  18 18 18    # Ngrid or scf.energycutoff")
        print("#scf.fixed.grid             12 12 12")
        print("")
        print("scf.EigenvalueSolver       band        # DC|Krylov|ON2|Cluster|Band")
        if not KP:
            KP = np.zeros((1, 3))
            KP[0, 0] = 12
            KP[0, 1] = 12
            KP[0, 2] = 12
        print(
            "scf.Kgrid                 %s %s %s     # means 4x4x4"
            % (str(int(KP[0, 0])), str(int(KP[0, 1])), str(int(KP[0, 2])))
        )
        print("scf.Generation.Kpoint     regular      # regular|MP")
        print("")
        EDIFF = EDIFF if "EDIFF" in locals() else 1e-06
        print(
            "scf.criterion             %s       # default=1.0e-6 (Hartree) "
            % str(EDIFF)
        )
        print(
            "scf.lapack.dste            dstevx      # dstegr|dstedc|dstevx, default=dstevx"
        )
        print("")
        print(
            "scf.Mixing.Type           rmm-diisk    # Simple|Rmm-Diis|Gr-Pulay|Kerker|Rmm-Diisk"
        )
        print("scf.Init.Mixing.Weight     0.30        # default=0.30 ")
        print("scf.Mixing.History          5          # default=5")
        print("")
        print("# on-the-fly ( using ./case_SCF_keywords files")
        print("")
        NELM = NELM if "NELM" in locals() else 40
        print("scf.maxIter                 %s         # default=40" % str(NELM))
        print("scf.Min.Mixing.Weight      0.001       # default=0.001 ")
        print("scf.Max.Mixing.Weight      0.400       # default=0.40 ")
        print("#scf.Kerker.factor")
        print("scf.Mixing.StartPulay       6          # default=6")
        print("")
        print("###########################################")
        print("# 1D FFT")
        print("###########################################")
        print("")
        print("#1DFFT.NumGridK             900         # default=900")
        print("#1DFFT.NumGridR             900         # default=900")
        print("#1DFFT.EnergyCutoff        3600.0       # default=3600 (Ry)")
        print("")
        print("###########################################")
        print("# Orbital Optimization")
        print("###########################################")
        print("")
        print(
            "#orbitalOpt.Method           Off        # Off|Unrestricted|Restricted|species"
        )
        print("#orbitalOpt.Opt.Method       EF         # DIIS|EF")
        print("#orbitalOpt.SD.step        0.001        # default=0.001")
        print("#orbitalOpt.HistoryPulay     30         # default=15")
        print("#orbitalOpt.StartPulay       10         # default=1")
        print("#orbitalOpt.InitCoes     Symmetrical    # Symmetrical|Free")
        print("#orbitalOpt.initPrefactor   0.1         # default=0.1")
        print("#orbitalOpt.scf.maxIter      12         # default=12")
        print("#orbitalOpt.MD.maxIter        2         # default=5")
        print("#orbitalOpt.per.MDIter        2         # default=1000000")
        print("")
        print("#orbitalOpt.criterion      1.0e-4       # default=1.0e-4 (Hartree/borh)")
        print("")
        print("#CntOrb.fileout               off       # on|off, default=off")
        print("#Num.CntOrb.Atoms              1        # default=1")
        print("#<Atoms.Cont.Orbitals")
        print("# 1")
        print("#Atoms.Cont.Orbitals>")
        print("")
        print("###########################################")
        print("# SCF Order-N")
        print("###########################################")
        print("")
        print("#orderN.HoppingRanges        7.0        # default=5.0 (Ang) ")
        print("#orderN.NumHoppings           2         # default=2")
        print("")
        print("###########################################")
        print("# MD or Geometry Optimization")
        print("###########################################")
        print("")
        print("# Nomd|Opt|DIIS|BFGS|RF|EF, MD( NVE|NVT_VS|NVT_NH ) or EvsLC")
        NSW = NSW if "NSW" in locals() else 0
        if NSW == 0:
            print("MD.Type                   nomd")
        else:
            IBRION = IBRION if "IBRION" in locals() else 2
            if IBRION != 0:
                print("MD.Type                   Opt")
        print("")
        print("#MD.EvsLC.Step             0.4         # default=0.4%")
        print("#MD.EvsLC.flag            1 1 1        # a,b,c, default=1 1 1")
        print("")
        print("MD.Opt.DIIS.History         3          # default=3")
        print("MD.Opt.StartDIIS           20          # default=3")
        print("MD.Opt.EveryDIIS           200         # default=200")
        print("")
        if NSW > 0:
            print(
                "MD.maxIter                 %s        # default=1 (only MD=1)"
                % str(NSW)
            )
        else:
            print("MD.maxIter                 1       # default=1 (only MD=1)")
        print("MD.TimeStep                1.0         # default=0.5 (fs)")
        EDIFFG = EDIFFG if "EDIFFG" in locals() else EDIFF * 10.0
        print(
            "MD.Opt.criterion          %s       # default=1.0e-4 (Hartree/bohr)"
            % str(EDIFFG)
        )
        print("MD.Opt.DIIS_Mixing         0.5         # default=0.5")
        print("")
        print("scf.ExtCharge.History       2          # default=2")
        print("#<MD>TempControl")
        print("#2")
        print("#100   2   5500.0 0.0")
        print("#600  50    300.0 0.4")
        print("#MD.TempControl>")
        if selective:
            print("")
            print("###########################################")
            print("# MD.Fixed.XYZ")
            print("###########################################")
            print("")
            print("<MD.Fixed.XYZ")
            for i in range(natom):
                if fix[i][0] == "F":
                    fix_x = 1
                else:
                    fix_x = 0
                if fix[i][1] == "F":
                    fix_y = 1
                else:
                    fix_y = 0
                if fix[i][2] == "F":
                    fix_z = 1
                else:
                    fix_z = 0
                print("  %d  %d %d %d" % (i + 1, fix_x, fix_y, fix_z))
            print("MD.Fixed.XYZ>")
        print("")
        print("###########################################")
        print("# Band dispersion")
        print("###########################################")
        print("")
        print("#Band.dispersion              on        # on|off, default=off")
        print("#<Band.KPath.UnitCell")
        print("#3.56  0.00  0.00")
        print("#0.00  3.56  0.00")
        print("#0.00  0.00  3.56")
        print("#Band.KPath.UnitCell>")
        print("## if <Band.KPath.UnitCell does not exist,")
        print("##     the reciprical lattice vector is employed. ")
        print("#Band.Nkpath                5")
        print("#<Band.kpath")
        print("#   25  0.0 0.0 0.0   1.0 0.0 0.0   g X")
        print("#   25  1.0 0.0 0.0   1.0 0.5 0.0   X W")
        print("#   25  1.0 0.5 0.0   0.5 0.5 0.5   W L")
        print("#   25  0.5 0.5 0.5   0.0 0.0 0.0   L g")
        print("#   25  0.0 0.0 0.0   1.0 0.0 0.0   g X")
        print("#Band.kpath>")
        print("")
        print("###########################################")
        print("# MO output")
        print("###########################################")
        print("")
        print("#MO.fileout                       off   # on|off")
        print("#num.HOMOs                         1    # default=2")
        print("#num.LUMOs                         1    # default=2")
        print("#MO.Nkpoint                        2    # default=1 ")
        print("#<MO.kpoint")
        print("#  0.0  0.0  0.0")
        print("#  0.0  0.0  0.2")
        print("#MO.kpoint>")
        print("")
        print("###########################################")
        print("# DOS and PDOS")
        print("###########################################")
        print("")
        print("Dos.fileout                  on        # on|off, default=off")
        print("Dos.Erange              -20.0  10.0    # default = -20 20 ")
        print("#Dos.Kgrid                12 12 12     # default = Kgrid1 Kgrid2 Kgrid3")
        print("")
        print("#DosGauss.fileout             on        # default=off, on|off")
        print("#DosGauss.Num.Mesh           200        # default=200")
        print("#DosGauss.Width              0.2        # default=0.2 (eV)")
        print("")
        print("###########################################")
        print("# output Hamiltonian and overlap (for Developer)")
        print("###########################################")
        print("")
        print("#HS.fileout               off    # on|off, default=off")
        print("")
        print("###########################################")
        print("# Electric Field")
        print("###########################################")
        print("")
        print("#scf.Electric.Field")
        print("")
        print("###########################################")
        print("# Charge Dorping")
        print("###########################################")
        print("")
        print("#scf.system.charge         1.0   # default=0.0")
        print("###########################################")
        print("# ESM (Effective Screening Medium)")
        print("###########################################")
        print(
            "#ESM.switch                   on3      # off, on1=v|v|v, on2=m|v|m, on3=v|v|m, on4=on2+EF"
        )
        print("#ESM.potential.difference     0.0      # default=0.0 (eV)")
        print("")
        print("#ESM.wall.switch              off")
        print("#ESM.wall.position            6.0      # default=10.0 (ang)")
        print("#ESM.wall.height            100.0      # default=100.0 (eV)")
        print("")
        print("#ESM.buffer.range             4.5      # default=10.0 (ang)")
        print("")
        print("###########################################")
        print("# Wannier Function")
        print("###########################################")
        print("")
        print("#Wannier.Func.Calc        on")
        print("#Wannier.Func.Num          4")
        print("#Wannier.Outer.Window.Bottom -14.0")
        print("#Wannier.Outer.Window.Top     0.0")
        print("#Wannier.Inner.Window.Bottom   0.0")
        print("#Wannier.Inner.Window.Top       0.0")
        print("#Wannier.Initial.Guess         on")
        print("#Wannier.Initial.Projectors.Unit FRAC     # AU, ANG or FRAC ")
        print("##proj-sp3 0.25 0.25 0.25 0.0 0.0 -1.0  -1.0 0.0 0.0")
        print("#")
        print("#<Wannier.Initial.Projectors")
        print("#proj-s 0.125 0.125 0.125 0.0 0.0 1.0  1.0 0.0 0.0")
        print("#proj-s -0.375 0.125 0.125 0.0 0.0 1.0 1.0 0.0 0.0")
        print("#proj-s 0.125 -0.375 0.125 0.0 0.0 1.0 1.0 0.0 0.0")
        print("#proj-s 0.125 0.125 -0.375 0.0 0.0 1.0 1.0 0.0 0.0")
        print("#Wannier.Initial.Projectors>")
        print("#")
        print("## Si1-s  1.275 1.275 1.275  0.0 0.0 1.0    1.0 0.0 0.0 ")
        print("## Si1-s  -1.275 -1.275 1.275 0.0 0.0 1.0    1.0 0.0 0.0 ")
        print("## Si1-s  -1.275 1.275 -1.275 0.0 0.0 1.0    1.0 0.0 0.0 ")
        print("## Si1-s  1.275 -1.275 -1.275 0.0 0.0 1.0    1.0 0.0 0.0 ")
        print("#Wannier.Kgrid   8 8 8")
        print("#Wannier.MaxShells   12")
        print("#")
        print("#Wannier.Interpolated.Bands              on   # on|off, default=off ")
        print("#")
        print("#Wannier.Function.Plot                   on   # on|off, default=off")
        print("#Wannier.Function.Plot.SuperCells     1 1 1   # default=0 0 0")
        print("#")
        print("#Wannier.Dis.Mixing.Para     0.5")
        print("#Wannier.Dis.Conv.Criterion    1e-12")
        print("#Wannier.Dis.SCF.Max.Steps    200")
        print("#")
        print("#Wannier.Minimizing.Max.Steps    100")
        print("#Wannier.Minimizing.Scheme     2")
        print("#Wannier.Minimizing.StepLength  2.0")
        print("#Wannier.Minimizing.Secant.Steps         5")
        print("#Wannier.Minimizing.Secant.StepLength    2.0")
        print("#Wannier.Minimizing.Conv.Criterion        1e-10")
        print("#")
        print("#")
        print("#Wannier.Readin.Overlap.Matrix            off")
        print("")
        print("")
        if not STD:
            datfile.close()
            sys.stdout = sys.__stdout__
