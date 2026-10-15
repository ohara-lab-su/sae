#!/usr/bin/env python
# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
from sae.fdmnes.conv import ReadFdmConv
from sae.fdmnes.inp import ReadFdmInp
from sae.fdmnes.sd import ReadFdmSd
from sae.fdmnes.txt import ReadFdmTxt

__author__ = "Kengo NAKADA"
__maintainer__ = "Kengo NAKADA"
__credits__ = ["Kengo NAKADA"]
__email__ = "kengo.nakada@gmail.com"
__copyright__ = "Copyright 2015, Kengo NAKADA"
__license__ = "MIT"
import sys
import os
import optparse
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def options():
    from sae.fdmnes.fdmfile import ReadFdmFdmfile

    parser = optparse.OptionParser()
    parser.add_option("-i", "--inpname", dest="INPUT")
    parser.add_option("-f", "--filout", "--filoutname", dest="filoutname")
    parser.add_option("-c", "--conv", "--convname", dest="convname")
    parser.add_option("-t", "--txt", "--txtname", dest="txtname")
    parser.add_option("-s", "--sd", "--sdname", dest="sdname")
    parser.add_option("--filbav", "--bavname", dest="bavname")
    parser.add_option("--name")
    parser.add_option("--output", "--head", dest="output")
    parser.add_option("-a", "--atom")
    parser.add_option("--emax")
    parser.add_option("--emin")
    parser.add_option("--ymax")
    parser.add_option("--dmax")
    parser.add_option("--dmax_s")
    parser.add_option("--dmax_p")
    parser.add_option("--dmax_d")
    parser.add_option("--dmax_f")
    parser.add_option("--label")
    parser.add_option("--outsuffix")
    parser.add_option("--weight")
    parser.add_option("--xasweight")
    parser.add_option("--txtweight")
    parser.add_option("--dosweight")
    parser.add_option("-b", "--broad", action="store_true", default=False)
    parser.add_option("-x", "--xas", action="store_true", default=False)
    parser.add_option("--total", action="store_true", default=False)
    parser.add_option("--intdos", action="store_true", default=False)
    parser.add_option("--fermi", action="store_true", default=False)
    parser.add_option("--s", action="store_true", default=False)
    parser.add_option("--p", action="store_true", default=False)
    parser.add_option("--d", action="store_true", default=False)
    parser.add_option("--sp", action="store_true", default=False)
    parser.add_option("--spd", action="store_true", default=False)
    parser.add_option("--spdf", action="store_true", default=False)
    parser.add_option("--up", action="store_true", default=False)
    parser.add_option("--dn", "--down", action="store_true", default=False, dest="dn")
    parser.add_option("--spin", action="store_true", default=False)
    parser.add_option("--pdf", action="store_true", default=False)
    parser.add_option("--nw", action="store_true", default=False)
    options, args = parser.parse_args()
    if options.INPUT:
        inpname = options.INPUT
    elif os.path.exists("fdmfile.txt"):
        fdmfiletxt = ReadFdmFdmfile()
        inpname = fdmfiletxt.filout
    else:
        inpname = "read_pdb.inp"
    if not os.path.exists(inpname) or inpname is None:
        sys.exit(inpname + " file not fount")
    if len(args) > 0:
        inpname = args[0]
    if options.name:
        options.convname = options.name
        options.txtname = options.name
        options.sdname = options.name
    return [
        options.output,
        options.outsuffix,
        inpname,
        options.convname,
        options.txtname,
        options.filoutname,
        options.bavname,
        options.sdname,
        options.name,
        options.atom,
        options.label,
        options.emax,
        options.emin,
        options.ymax,
        options.dmax,
        options.dmax_s,
        options.dmax_p,
        options.dmax_d,
        options.dmax_f,
        options.broad,
        options.fermi,
        options.xas,
        options.up,
        options.dn,
        options.spin,
        options.s,
        options.p,
        options.sp,
        options.spd,
        options.spdf,
        options.weight,
        options.dosweight,
        options.xasweight,
        options.txtweight,
        options.total,
        options.intdos,
        options.pdf,
        options.nw,
    ]


if __name__ == "__main__":
    (
        outputname,
        OUTSUFFIX,
        inpname,
        convname,
        txtname,
        filout,
        bavname,
        sdname,
        allname,
        atom,
        LABEL,
        OPT_EMAX,
        OPT_EMIN,
        OPT_YMAX,
        OPT_DMAX,
        OPT_DMAX_S,
        OPT_DMAX_P,
        OPT_DMAX_D,
        OPT_DMAX_F,
        FLAG_BROAD,
        FLAG_FERMI,
        FLAG_XAS,
        FLAG_UP,
        FLAG_DN,
        FLAG_SPIN,
        FLAG_S,
        FLAG_P,
        FLAG_SP,
        FLAG_SPD,
        FLAG_SPDF,
        WE,
        WEDOS,
        WEXAS,
        WETXT,
        FLAG_TOTAL,
        FLAG_INTDOS,
        FLAG_PDF,
        FLAG_NW,
    ) = options()
    plt.rcParams["font.family"] = "Times New Roman"
    plt.rcParams["font.size"] = 15
    plt.rcParams["legend.fontsize"] = 10
    plt.rcParams["axes.linewidth"] = 1.5
    plt.figure(figsize=(7.0, 9.89))
    orgx = 0.17
    orgy = 0.08
    off = 0.015
    xsize = 0.72
    ysize0 = 0.75
    if FLAG_BROAD:
        FLAG_XAS = True
    if OPT_EMAX:
        print("Emax=", OPT_EMAX)
    if OPT_EMIN:
        print("Emin=", OPT_EMIN)
    if FLAG_XAS and OPT_YMAX:
        print("Ymax(XAS)=", OPT_YMAX)
    if OPT_DMAX:
        print("Ymax(DOS)=", OPT_DMAX)
    if OPT_DMAX_S:
        print("Ymax(s-orbit)=", OPT_DMAX_S)
    if OPT_DMAX_P:
        print("Ymax(p-orbit)=", OPT_DMAX_P)
    if OPT_DMAX_D:
        print("Ymax(d-orbit)=", OPT_DMAX_D)
    if OPT_DMAX_F:
        print("Ymax(f-orbit)=", OPT_DMAX_F)
    if WEDOS:
        print("Weight for DOS =", WEDOS)
        WEDOS = float(WEDOS)
    else:
        WEDOS = None
    if WE:
        print("Weight for XAS", WE)
        WEXAS = float(WE)
        WETXT = float(WE)
    if WETXT:
        print("Weight for XAS without convolution =", WETXT)
        WETXT = float(WETXT)
    else:
        WETXT = None
    if WEXAS:
        print("Weight for XAS with convolution =", WEXAS)
        WEXAS = float(WEXAS)
    else:
        WEXAS = None
    inp = ReadFdmInp(inpname)
    if not atom and (not inp.nonexc):
        atom = 0
    if not atom and inp.nonexc:
        atom = 1
    suffix_sd = "_sd" + str(atom) + ".txt"
    suffix_conv = "_conv.txt"
    if allname:
        convolname = allname
        txtname = allname
        sdname = allname
    if not filout:
        filout = inp.filout
    if convname is None:
        convname = filout
    if txtname is None:
        txtname = filout
    if bavname is None:
        bavname = filout
    if sdname is None:
        sdname = filout
    print("")
    print("inpname    (.inp)                  =", inpname)
    print("filoutname                         =", filout)
    print("txtname    (original XAS and Eferm)=", txtname)
    print("convname   (convolution file)      =", convname)
    print("bavname    (log file)              =", bavname)
    print("")
    txt = ReadFdmTxt(txtname, ".txt", weight=WETXT)
    conv = ReadFdmConv(convname, suffix_conv, weight=WEXAS)
    sd = ReadFdmSd(sdname, suffix_sd, weight=WEDOS)
    ispin = inp.ispin
    if ispin >= 2:
        print("")
        print("Current calculation is Magnetic: SPIN MODE")
        print("")
    print("")
    print("E_fermi =", txt.E_Fermi)
    print("E_edge  =", txt.E_edge)
    print("")
    lmax = sd.lmax
    if lmax == 0:
        orbit_list = ["s"]
    elif lmax == 1:
        orbit_list = ["s", "p"]
    elif lmax == 2:
        orbit_list = ["s", "p", "d"]
    elif lmax == 3:
        orbit_list = ["s", "p", "d", "f"]
    else:
        orbit_list = ["s", "p", "d"]
    if FLAG_S:
        orbit_list = ["s"]
    if FLAG_P:
        orbit_list = ["p"]
    if FLAG_SP:
        orbit_list = ["s", "p"]
    if FLAG_SPD:
        orbit_list = ["s", "p", "d"]
    if FLAG_SPDF:
        orbit_list = ["s", "p", "d", "f"]
    norbit = len(orbit_list)
    nspin = 1
    spin_list = [0]
    spin_suffix = [""]
    spin_out = ""
    if FLAG_UP:
        nspin = 1
        spin_list = [0]
        spin_suffix = ["_up", ""]
        spin_out = "_up"
    elif FLAG_DN:
        nspin = 1
        spin_list = [1]
        spin_suffix = ["", "_dn"]
        spin_out = "_dn"
    elif FLAG_SPIN or ispin >= 2:
        FLAG_SPIN = True
        nspin = 2
        spin_list = [1, 0]
        spin_suffix = ["_up", "_dn"]
        spin_out = "_spin"
        norbit = norbit * 2
    if FLAG_TOTAL:
        norbit += 1
    if FLAG_XAS:
        ysize = ysize0 / (norbit + 1)
    else:
        ysize = ysize0 / norbit
    if not inp.get_energygpho() and (not FLAG_FERMI):
        print("Current mode is Fermi")
        print("---> convert to PhotoEnergy")
        print("     + E_edge")
        eng_off = txt.E_edge
    if not inp.get_energygpho() and FLAG_FERMI:
        print("current mode is Fermi")
        print("---> subtract E_fermi")
        print("     - E_fermi")
        eng_off = -txt.E_fermi
    if inp.get_energygpho() and FLAG_FERMI:
        print("current mode is PhotoEnergy")
        print("---> convert to EF0 mode")
        print("     - E_edge - E_fermi")
        eng_off = txt.E_Fermi - txt.E_edge
    if FLAG_FERMI:
        EF0 = 0.0
        label_fermi = "Energy above Fermi [eV]"
    else:
        EF0 = txt.E_edge + txt.E_Fermi
        label_fermi = "Photon Energy [eV]"
    if not OPT_EMAX:
        emax = sd.emax + EF0
        print("EMAX = ", emax)
    if not OPT_EMIN:
        emin = sd.emin + EF0
        print("EMIN = ", emin)
    num = 0
    XTICKS_FLAG = False
    if FLAG_XAS:
        plt.axes([orgx, orgy, xsize, ysize])
        xas = conv.get_xas()
        engx = conv.get_eng() + eng_off
        label = "XAS (with broadening)"
        plt.plot(engx, xas, linewidth=2, color="black", label=label)
        plt.axvline(x=EF0, color="black", linewidth=1)
        xmin_XAS, xmax_XAS, ymin_XAS, ymax_XAS = plt.axis()
        plt.ylim(ymin=0.0)
        if FLAG_BROAD:
            eng_p = txt.eng + eng_off
            for spin in spin_list:
                xas_r = txt.get_xas(spin=spin)
                num += 1
                color = cm.prism(num * 10)
                label = "XAS" + spin_suffix[spin]
                plt.plot(eng_p, xas_r, linewidth=1, color=color, label=label)
                plt.ylim(ymax=ymax_XAS)
                plt.ylim(ymin=0.0)
        if not OPT_EMAX:
            plt.xlim(xmax=emax)
        if not OPT_EMIN:
            plt.xlim(xmin=emin)
        if OPT_EMAX:
            plt.xlim(xmax=float(OPT_EMAX))
        if OPT_EMIN:
            plt.xlim(xmin=float(OPT_EMIN))
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        leg = plt.legend(loc="lower right")
        leg.get_frame().set_alpha(0.5)
        plt.ylabel("Absorption [arb. unit]")
        if not XTICKS_FLAG:
            plt.xlabel(label_fermi)
            XTICKS_FLAG = True
        orgy = orgy + ysize + off
    eng = sd.get_eng() + eng_off
    if FLAG_TOTAL:
        num += 1
        for spin in spin_list:
            plt.axes([orgx, orgy, xsize, ysize])
            tdos = sd.get_tdos(spin=spin)
            if FLAG_INTDOS:
                inttdos = sd.get_inttdos(spin=spin)
            plt.ylabel("TDOS")
            if not XTICKS_FLAG:
                plt.xlabel(label_fermi)
                XTICKS_FLAG = True
            else:
                plt.xticks([])
            color = cm.prism((num + 1) * 10)
            label = "total" + spin_suffix[spin]
            labelt = "INT" + spin_suffix[spin]
            plt.plot(eng, tdos, linewidth=2, color=color, label=label)
            plt.axvline(x=EF0, color="black", linewidth=1)
            if FLAG_SPIN and spin == 1:
                xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                plt.ylim([ymax_dn, 0])
            if FLAG_INTDOS:
                ay = plt.twinx()
                ay.plot(eng, inttdos, linewidth=2, color="black", label=labelt)
                yl = plt.ylabel("INTTDOS")
            if FLAG_INTDOS and FLAG_SPIN and (spin == 1):
                xmin_idn, xmax_idn, ymin_idn, ymax_idn = plt.axis()
                plt.ylim([ymax_idn, 0])
            if not OPT_EMAX:
                plt.xlim(xmax=emax)
            if not OPT_EMIN:
                plt.xlim(xmin=emin)
            if OPT_EMAX:
                plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=float(OPT_EMIN))
            leg = plt.legend(loc="upper right")
            leg.get_frame().set_alpha(0.5)
            orgy = orgy + ysize
        orgy = orgy + off
    orb = 0
    for orbit in orbit_list:
        num += 1
        for spin in spin_list:
            plt.axes([orgx, orgy, xsize, ysize])
            ldos = sd.get_ldos(l=orbit, spin=spin)
            if FLAG_INTDOS:
                intldos = sd.get_intldos(l=orbit, spin=spin)
            if orb == 0:
                plt.ylabel("LDOS")
            if not XTICKS_FLAG:
                plt.xlabel(label_fermi)
                XTICKS_FLAG = True
            else:
                plt.xticks([])
            if LABEL:
                label = LABEL + "-" + orbit
            else:
                label = str(atom) + "-" + orbit
            color = cm.prism((num + 1) * 10)
            label = label + spin_suffix[spin]
            labelt = "INT" + label
            plt.plot(eng, ldos, linewidth=2, color=color, label=label)
            plt.axvline(x=EF0, color="black", linewidth=1)
            if FLAG_SPIN and spin == 1:
                xmin_dn, xmax_dn, ymin_dn, ymax_dn = plt.axis()
                plt.ylim([ymax_dn, 0])
            if FLAG_INTDOS:
                ay = plt.twinx()
                ay.plot(eng, intldos, linewidth=2, color="black", label=labelt)
                if orb == 0:
                    yl = plt.ylabel("INTTDOS")
            if FLAG_INTDOS and FLAG_SPIN and (spin == 1):
                xmin_idn, xmax_idn, ymin_idn, ymax_idn = plt.axis()
                plt.ylim([ymax_idn, 0])
            if not OPT_EMAX:
                plt.xlim(xmax=emax)
            if not OPT_EMIN:
                plt.xlim(xmin=emin)
            if OPT_EMAX:
                plt.xlim(xmax=float(OPT_EMAX))
            if OPT_EMIN:
                plt.xlim(xmin=float(OPT_EMIN))
            if OPT_DMAX:
                plt.ylim(ymax=float(OPT_DMAX))
            if OPT_DMAX_S and orbit == "s":
                plt.ylim(ymax=float(OPT_DMAX_S))
            if OPT_DMAX_P and orbit == "p":
                plt.ylim(ymax=float(OPT_DMAX_P))
            if OPT_DMAX_D and orbit == "d":
                plt.ylim(ymax=float(OPT_DMAX_D))
            if OPT_DMAX_F and orbit == "f":
                plt.ylim(ymax=float(OPT_DMAX_F))
            leg = plt.legend(loc="upper right")
            leg.get_frame().set_alpha(0.5)
            orgy = orgy + ysize
        orb += 1
        orgy = orgy + off
    if FLAG_FERMI:
        fermi = "_fermi"
    else:
        fermi = ""
    if outputname:
        _head = outputname + "_"
        print("output header =", outputname)
    else:
        _head = "LDOS"
    if OUTSUFFIX:
        _outsuffix = str(OUTSUFFIX)
    else:
        _outsuffix = ""
    plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".pdf")
    if FLAG_PDF:
        plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".eps")
        plt.savefig(_head + str(atom) + _outsuffix + spin_out + fermi + ".png")
    if not FLAG_NW:
        plt.show()
    plt.close("all")
