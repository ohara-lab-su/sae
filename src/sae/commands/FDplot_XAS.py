#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt
from sae.athena.nor import ReadAthenaNor

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import argparse
import matplotlib.pyplot as plt


def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inp", "--inpname", dest="INPUT")
    parser.add_argument("-f", "--filout", "--filoutname", dest="filout")
    parser.add_argument("-c", "--conv", "--convolution", dest="convname")
    parser.add_argument("-t", "--txt", "--textname", dest="txtname")
    parser.add_argument("-s", "--sd", "--sdname", dest="sdname")
    parser.add_argument("--filbav", "--bavname", dest="bavname")
    parser.add_argument("--name")
    parser.add_argument("--output")
    parser.add_argument("--emax")
    parser.add_argument("--emin")
    parser.add_argument("--ymax")
    parser.add_argument("--dmax")
    parser.add_argument("--l2", action="store_true", default=False)
    parser.add_argument("--l3", action="store_true", default=False)
    parser.add_argument("--l23", action="store_true", default=False)
    parser.add_argument("--fermi", action="store_true", default=False)
    parser.add_argument("-n", "--nonsubtract", action="store_true", default=False)
    parser.add_argument("-b", "--broad", action="store_true", default=False)
    parser.add_argument("--xas", action="store_true", default=False)
    parser.add_argument("-d", "--dos", action="store_true", default=False)
    parser.add_argument("-o", "--obs")
    parser.add_argument("-a", "--absorber", nargs="*")
    parser.add_argument("-w", "--weight")
    parser.add_argument("-x", "--dosweight")
    parser.add_argument("--up", action="store_true", default=False)
    parser.add_argument("--dn", "--down", action="store_true", default=False, dest="dn")
    parser.add_argument("--spin", action="store_true", default=False)
    parser.add_argument("--pdf", action="store_true", default=False)
    parser.add_argument("--nw", action="store_true", default=False)
    options = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.get_filout()
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    if options.name:
        options.convname = options.name
        options.txtname = options.name
        options.sdname = options.name
    return [
        options.output,
        inpname,
        options.convname,
        options.txtname,
        options.filout,
        options.bavname,
        options.sdname,
        options.name,
        options.emax,
        options.emin,
        options.ymax,
        options.dmax,
        options.l2,
        options.l3,
        options.l23,
        options.fermi,
        options.nonsubtract,
        options.broad,
        options.xas,
        options.dos,
        options.obs,
        options.absorber,
        options.weight,
        options.dosweight,
        options.up,
        options.dn,
        options.spin,
        options.pdf,
        options.nw,
    ]


if __name__ == "__main__":
    (
        outputname,
        inpname,
        convolname,
        textname,
        filoutname,
        bavname,
        sdname,
        allname,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_DMAX,
        FLAG_L2,
        FLAG_L3,
        FLAG_L23,
        FLAG_fermi,
        FLAG_subt,
        FLAG_B,
        FLAG_XAS,
        FLAG_DOS,
        OPT_OBS,
        AV,
        WE,
        WEDOS,
        FLAG_UP,
        FLAG_DN,
        FLAG_SPIN,
        FLAG_PDF,
        FLAG_NW,
    ) = options()
    if FLAG_L2 or FLAG_L3:
        print("2-edge mode (L23-mode)")
        if FLAG_L2:
            print("L2-edge mode")
            edge = "L2"
        elif FLAG_L3:
            print("L3-edge mode")
            edge = "L3"
    else:
        edge = "K"
    if FLAG_L2 and FLAG_L3 or FLAG_L23:
        print("L2,L3-edge mode")
    print("inpname")
    print("-------------------------> ", inpname)
    inp = ReadFdmInp(inpname)
    print("filout name")
    print("-------------------------> ", inp.filout)
    if not filoutname:
        calculation = inp.get_calculation()
        if calculation:
            filout = calculation.replace(".txt", "")
        else:
            filout = inp.get_filout()
    else:
        filout = filoutname
    if AV:
        print("--- average mode ---")
        print("Absorber =", AV)
    if WE:
        print("XANES Weight =", WE)
    if WEDOS:
        print("DOS Weight   =", WEDOS)
    if AV:
        print("")
    if allname:
        convolname = allname
        textname = allname
        sdname = allname
    if AV:
        print("")
        print("--- average mode ---")
        print("text base name (.txt)")
        print("------======-------------> ", filout + "_" + str(AV[0]))
        txt = ReadFdmTxt(filout + "_" + str(AV[0]), suffix=".txt", edge=edge)
        print("convolution base name (_conv.txt)")
        print("-----------======--------> ", filout + "_" + str(AV[0]))
        conv = ReadFdmConv(filout + "_" + str(AV[0]), suffix="_conv.txt")
    else:
        if textname is None:
            textname = filout
        if convolname is None:
            convolname = filout
        print("text base name  (.txt)")
        print("-------------------------> ", textname)
        txt = ReadFdmTxt(textname, suffix=".txt", edge=edge)
        print("convolution base name (_conv.txt)")
        print("-------------------------> ", convolname)
        conv = ReadFdmConv(convolname, "_conv.txt")
    if AV:
        if WE:
            conv.xas = conv.average_conv(filout, AV, weight=WE)
            txt.xas = txt.average(filout, AV, weight=WE)
        else:
            conv.xas = conv.average_conv(filout, AV)
            txt.xas = txt.average(filout, AV)
        print("")
    if FLAG_DOS:
        if bavname:
            filbav = bavname
        else:
            filbav = filout
        print("Bav base name (_bav.txt)")
        print("-------------------------> ", filbav)
        if AV:
            sdname = filout
            print("Sdname base (_sd0.txt)")
            print("-------------------------> ", sdname)
            print("")
            if WEDOS:
                sd = ReadFdmSd(
                    sdname,
                    suffix="_sd0.txt",
                    bavname=filbav,
                    inpname=inpname,
                    absorber=AV,
                    weight=WEDOS,
                )
            elif WE:
                sd = ReadFdmSd(
                    sdname,
                    suffix="_sd0.txt",
                    bavname=filbav,
                    inpname=inpname,
                    absorber=AV,
                    weight=WE,
                )
            else:
                sd = ReadFdmSd(
                    sdname,
                    suffix="_sd0.txt",
                    bavname=filbav,
                    inpname=inpname,
                    absorber=AV,
                )
        else:
            if sdname:
                sdname = sdname
            else:
                sdname = filout
            print("Sdname base name (_sd0.txt)")
            print("-------------------------> ", sdname)
            print("")
            sd = ReadFdmSd(sdname, suffix="_sd0.txt", bavname=filbav, inpname=inpname)
        print("")
    if AV:
        outav = open(filout + "_0_conv.txt", "w")
        print("", file=outav)
        for i in range(len(conv.eng)):
            print("  %14.8f %14.8f" % (conv.eng[i], conv.xas[i]), file=outav)
        outav.close()
        print("WRITE: ", filout + "_0_conv.txt", file=outav)
    if AV:
        outtxt = open(filout + "_0.txt", "w")
        print("%s" % txt.header, file=outtxt)
        print("    Energy    <xanes>  ", file=outtxt)
        for i in range(len(txt.eng)):
            print("  %14.3f %14.8f" % (txt.eng[i], txt.xas[i]), file=outtxt)
        outtxt.close()
        print("WRITE: ", filout + "_0.txt", file=outtxt)
    if FLAG_DOS and AV:
        outsd = open(filout + "_0_sd0.txt", "w")
        print("%s" % sd.header, file=outsd)
        for i in range(1, sd.num):
            print("%s" % sd.sd[i], file=outsd)
        outsd.close()
        print("WRITE: ", filout + "_0_sd0.txt", file=outsd)
    if AV:
        print("")
    if OPT_EMAX:
        OPT_EMAX = float(OPT_EMAX)
        print("Emax             =", OPT_EMAX)
    if OPT_EMIN:
        OPT_EMIN = float(OPT_EMIN)
        print("Emin             =", OPT_EMIN)
    if OPT_YMAX:
        OPT_YMAX = float(OPT_YMAX)
        print("Ymax             =", OPT_YMAX)
    if OPT_DMAX:
        OPT_DMAX = float(OPT_DMAX)
        print("Ymax(DOS)        =", OPT_DMAX)
    if FLAG_SPIN:
        print("Enforce spin=2 mode")
    if WE:
        WE = float(WE)
        print("Weight           =", WE)
    if WEDOS:
        WEDOW = float(WEDOS)
        print("Weight for LDOS  =", WEDOS)
    plt.rcParams["font.size"] = 16
    plt.rcParams["legend.fontsize"] = 14
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(8.1, 9.89))
    print("-------------------")
    print("E_edge   =", txt.E_edge)
    print("E_fermi  =", txt.E_Fermi)
    print("-------------------")
    txt_eng = txt.eng
    if not FLAG_subt:
        if not inp.get_energygpho() and (not FLAG_fermi):
            print("current mode is Fermi (E_edge = 0)")
            print("---> convert to PhotoEnergy")
            print("     + E_edge")
            txt_eng = txt.eng + txt.E_edge
            conv.eng = conv.eng + txt.E_edge
        if not inp.get_energygpho() and FLAG_fermi:
            print("current mode is Fermi")
            print("---> subtract E_fermi")
            print("     - E_fermi")
            txt_eng = txt.eng - txt.E_Fermi
            conv.eng = conv.eng - txt.E_Fermi
        if inp.get_energygpho() and FLAG_fermi:
            print("current mode is PhotoEnergy")
            print("---> convert to EF0 mode")
            print("     - E_edge - E_fermi")
            txt_eng = txt.eng - txt.E_Fermi - txt.E_edge
            conv.eng = conv.eng - txt.E_Fermi - txt.E_edge
    if FLAG_DOS:
        plt.subplot(3, 1, 2)
    else:
        plt.subplot(2, 1, 2)
    if not FLAG_B or FLAG_XAS:
        plt.plot(txt_eng, txt.xas, color="green", linewidth=1, label="XAS")
    if not FLAG_XAS:
        plt.plot(conv.eng, conv.xas, color="red", linewidth=3, label="XAS broad")
    plt.ticklabel_format(axis="x", useOffset=False)
    plt.ylabel("Absorption [arb. unit]")
    EF0 = txt.E_edge + txt.E_fermi
    if not FLAG_subt:
        if FLAG_fermi:
            plt.axvline(x=0, color="black", linewidth=1)
        else:
            plt.axvline(x=EF0, color="black", linewidth=1)
    leg = plt.legend(loc="lower right")
    leg.get_frame().set_alpha(0.5)
    if OPT_EMAX:
        plt.xlim(xmax=float(OPT_EMAX))
    if OPT_EMIN:
        plt.xlim(xmin=float(OPT_EMIN))
    if OPT_YMAX:
        plt.ylim(ymax=float(OPT_YMAX))
    xas_xmin, xas_xmax, xas_ymin, xas_ymax = plt.axis()
    if FLAG_DOS:
        plt.subplot(3, 1, 3)
        dos_p = sd.get_ldos(l="p")
        plt.plot(conv.eng, dos_p, linewidth=1, label="absorber-LDOS(p)")
        plt.ticklabel_format(axis="x", useOffset=False)
        if not FLAG_SPIN:
            dos_s = sd.get_ldos(l="s")
            plt.plot(conv.eng, dos_s, linewidth=1, label="absorber-LDOS(s)")
            plt.ticklabel_format(axis="x", useOffset=False)
        else:
            dos_s = sd.get_ldos(l="p", spin="up")
            plt.plot(conv.eng, dos_s, linewidth=1, label="absorber-LDOS(p)  up")
            dos_s = sd.get_ldos(l="p", spin="down")
            plt.plot(conv.eng, dos_s, linewidth=1, label="absorber-LDOS(p)  down")
            plt.ticklabel_format(axis="x", useOffset=False)
        plt.ylabel("DOS [stat/eV]")
        if not FLAG_subt:
            if FLAG_fermi:
                plt.axvline(x=0, color="black", linewidth=1)
            else:
                plt.axvline(x=EF0, color="black", linewidth=1)
        leg = plt.legend(loc="upper right")
        leg.get_frame().set_alpha(0.5)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_DMAX:
            plt.ylim(ymax=float(OPT_DMAX))
    if FLAG_fermi:
        plt.xlabel("Energy above Fermi [eV]")
    else:
        plt.xlabel("Photon Energy [eV]")
    if OPT_OBS:
        if os.path.exists(OPT_OBS):
            obs_file = OPT_OBS
        else:
            obs_file = filout + "_obs.txt.nor"
        if not os.path.exists(obs_file):
            sys.exit("STOP: " + obs_file + " not found")
        nor = ReadAthenaNor(obs_file)
        if FLAG_DOS:
            plt.subplot(3, 1, 1)
        else:
            plt.subplot(2, 1, 1)
        plt.plot(nor.eng, nor.nor, label="obs.")
        plt.xlim([xas_xmin, xas_xmax])
        plt.ticklabel_format(axis="x", useOffset=False)
        leg = plt.legend(loc="lower right")
        leg.get_frame().set_alpha(0.5)
    plt.ylim(ymin=0.0)
    if outputname:
        _head = outputname + "_"
        print("output header = ", outputname)
    else:
        _head = "XAS"
    if allname:
        plt.savefig(_head + "_" + allname + ".pdf")
        if FLAG_PDF:
            plt.savefig(_head + "_" + allname + ".eps")
            plt.savefig(_head + "_" + allname + ".png")
    else:
        plt.savefig(_head + ".pdf")
        if FLAG_PDF:
            plt.savefig(_head + ".eps")
            plt.savefig(_head + ".png")
    if not FLAG_NW:
        plt.show()
    plt.close("all")
