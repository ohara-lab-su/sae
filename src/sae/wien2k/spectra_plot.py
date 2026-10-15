# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function


class SpectraPlot:

    def plot_sum_xas(
        self,
        case="case",
        dos_suffix=".dos1ev",
        outname="XAS",
        OPT_EMAX="None",
        OPT_EMIN="None",
        OPT_YMAX="None",
        FLAG_SHOW=True,
    ):
        from sae.wien2k.dos import ReadWienDos
        from sae.wien2k.txspec import ReadWienTxspec
        from sae.wien2k.xspec import ReadWienXspec
        import sys
        import numpy as np
        import matplotlib.pyplot as plt

        if OPT_EMAX:
            print("Emax= %s" % str(OPT_EMAX))
        if OPT_EMIN:
            print("Emin= %s" % str(OPT_EMIN))
        if OPT_YMAX:
            print("Ymax= %s" % str(OPT_YMAX))
        txspec_up = ReadWienTxspec(case=case, suffix=".txspecup")
        txspec_dn = ReadWienTxspec(case=case, suffix=".txspecup")
        unbroad_up = np.array(txspec_up.get_unbroad_xas())
        unbroad_dn = np.array(txspec_dn.get_unbroad_xas())
        unbroad = unbroad_up + unbroad_dn
        xspec_up = ReadWienXspec(case=case, suffix=".xspecup")
        xspec_dn = ReadWienXspec(case=case, suffix=".xspecdn")
        eng_xas = xspec_up.get_eng()
        xas_up = xspec_up.get_xas()
        xas_dn = xspec_dn.get_xas()
        xas = xas_up + xas_dn
        xas_head = xspec_up.get_head()
        unit = "ev"
        name_up = [case + dos_suffix + "up"]
        name_dn = [case + dos_suffix + "dn"]
        print("DOS(up) = %s" % str(name_up[0]))
        print("DOS(dn) = %s" % str(name_dn[0]))
        dos_up = ReadWienDos(name_up)
        dos_dn = ReadWienDos(name_dn)
        efermi = dos_up.get_efermi()
        dos_head = dos_up.get_head()
        eng = dos_up.get_eng()
        eng_emin = dos_up.get_emin()
        eng_emax = dos_up.get_emax()
        norbital = dos_up.get_norbital()
        if norbital == 2:
            mode = "K"
        elif norbital == 3:
            mode = "L"
        print("MODE = %s" % str(mode))
        dos_total_up = np.array(dos_up.get_raw_dos(atom=0, orbit="total-DOS"))
        dos_total_dn = np.array(dos_dn.get_raw_dos(atom=0, orbit="total-DOS"))
        dos_total = dos_total_up + dos_total_dn
        if mode == "K":
            dos_p_up = np.array(dos_up.get_raw_dos(atom=1, orbit="p"))
            dos_p_dn = np.array(dos_dn.get_raw_dos(atom=1, orbit="p"))
            dos_p = dos_p_up + dos_p_dn
        else:
            dos_s_up = np.array(dos_up.get_raw_dos(atom=1, orbit="s"))
            dos_s_dn = np.array(dos_dn.get_raw_dos(atom=1, orbit="s"))
            dos_d_up = np.array(dos_up.get_raw_dos(atom=1, orbit="d"))
            dos_d_dn = np.array(dos_dn.get_raw_dos(atom=1, orbit="d"))
            dos_s = dos_s_up + dos_s_dn
            dos_d = dos_d_up + dos_d_dn
        try:
            out_xspecsum = open(case + ".xspecsum", "w")
        except:
            out_xspecsum.cloase()
            sys.exit("STOP: " + case + ".xspecsum file can'ntopen ")
        for xh in xas_head:
            print("%s" % str(xh), file=out_xspecsum)
        for i in range(len(xas)):
            print(" %9.5f %13.5e" % (eng_xas[i], xas[i]), file=out_xspecsum)
        out_xspecsum.close()
        try:
            out_dos1ev = open(case + ".dos1evsum", "w")
        except:
            out_dos1ev.cloase()
            sys.exit("STOP: " + case + ".dos1evsum file can'ntopen ")
        for dos_h in dos_head[0]:
            print("%s" % str(dos_h), file=out_dos1ev)
        if mode == "K":
            for i in range(len(dos_total)):
                print(
                    " %9.5f %14.8f %14.8f" % (eng[i], dos_p[i], dos_total[i]),
                    file=out_dos1ev,
                )
        else:
            for i in range(len(dos_total)):
                print(
                    " %9.5f %14.8f %14.8f %14.8f"
                    % (eng[i], dos_s[i], dos_d[i], dos_total[i]),
                    file=out_dos1ev,
                )
        out_dos1ev.close()
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = 16
        plt.rcParams["legend.fontsize"] = 14
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        orgx = 0.15
        orgy = 0.08
        off = 0.01
        xsize = 0.75
        ysize0 = 0.83
        if mode == "K":
            ysize = ysize0 / 3.5
            ysize_dos = ysize0 / 4
        else:
            ysize = ysize0 / 4
            ysize_dos = ysize0 / 4.8
        if OPT_EMAX:
            emax = float(OPT_EMAX)
        else:
            emax = eng_emax
        if OPT_EMIN:
            emin = float(OPT_EMIN)
        else:
            emin = eng_emin
        plt.axes([orgx, orgy, xsize, ysize_dos])
        eng = eng - efermi
        plt.plot(eng, dos_total, color="black", linewidth=2, label="total-DOS")
        plt.ylabel("DOS [unit/" + unit + "]")
        plt.xlabel("Energy above Fermi [" + unit + "]")
        plt.axvline(x=0, color="black", linewidth=1)
        plt.xlim([emin, emax])
        plt.ylim(ymin=0)
        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)
        if mode == "K":
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_p, color="black", linewidth=2, label="p")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
        else:
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_s, color="black", linewidth=2, label="s")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_d, color="black", linewidth=2, label="d")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
        orgy = orgy + ysize + off + off + off + off
        plt.axes([orgx, orgy, xsize, ysize])
        plt.plot(eng_xas, xas, color="black", linewidth=2, label="XAS")
        plt.fill_between(eng_xas, xas, color="#cccccc", linewidth=2, label="XAS")
        plt.plot(
            eng_xas,
            unbroad,
            linestyle="-",
            color="green",
            linewidth=0.8,
            label="unbroad",
        )
        plt.yticks([])
        plt.xlabel("Energy above Fermi [" + unit + "]")
        plt.ylabel("Absorption [arb. unit]")
        plt.axvline(x=0, color="black", linewidth=1)
        plt.xlim([emin, emax])
        plt.ylim(ymin=0)
        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        else:
            ymax = xspec_up.get_ymax_xas() * 2.0
            ymax0 = ymax / 10.0
            ymax = ymax + ymax0 * 1.5
            plt.ylim(ymax=ymax)
        plt.savefig(outname + ".eps")
        plt.savefig(outname + ".pdf")
        plt.savefig(outname + ".png")
        if FLAG_SHOW:
            plt.show()
        plt.close("all")

    def plot_xas(
        self,
        case="case",
        dos_suffix=".dos1ev",
        txspec_suffix=".txspec",
        xspec_suffix=".xspec",
        outname="XAS",
        OPT_EMAX="None",
        OPT_EMIN="None",
        OPT_YMAX="None",
        FLAG_SHOW=True,
    ):
        from sae.wien2k.dos import ReadWienDos
        from sae.wien2k.txspec import ReadWienTxspec
        from sae.wien2k.xspec import ReadWienXspec
        import matplotlib.pyplot as plt

        if OPT_EMAX:
            print("Emax= %s" % str(OPT_EMAX))
        if OPT_EMIN:
            print("Emin= %s" % str(OPT_EMIN))
        if OPT_YMAX:
            print("Ymax= %s" % str(OPT_YMAX))
        txspec = ReadWienTxspec(case=case, suffix=txspec_suffix)
        unbroad = txspec.get_unbroad_xas()
        xspec = ReadWienXspec(case=case, suffix=xspec_suffix)
        eng_xas = xspec.get_eng()
        xas = xspec.get_xas()
        unit = "ev"
        name = [case + dos_suffix]
        print("DOS = %s" % str(name[0]))
        dos = ReadWienDos(name)
        efermi = dos.get_efermi()
        eng = dos.get_eng()
        eng_emin = dos.get_emin()
        eng_emax = dos.get_emax()
        norbital = dos.get_norbital()
        if norbital == 2:
            mode = "K"
        elif norbital == 3:
            mode = "L"
        print("MODE = %s" % str(mode))
        dos_total = dos.get_raw_dos(atom=0, orbit="total-DOS")
        if mode == "K":
            dos_p = dos.get_raw_dos(atom=1, orbit="p")
        else:
            dos_s = dos.get_raw_dos(atom=1, orbit="s")
            dos_d = dos.get_raw_dos(atom=1, orbit="d")
        plt.rcParams["font.family"] = "Times New Roman"
        plt.rcParams["font.size"] = 16
        plt.rcParams["legend.fontsize"] = 14
        plt.rcParams["axes.linewidth"] = 1.5
        plt.figure(figsize=(7.0, 9.89))
        orgx = 0.15
        orgy = 0.08
        off = 0.01
        xsize = 0.75
        ysize0 = 0.83
        if mode == "K":
            ysize = ysize0 / 3.5
            ysize_dos = ysize0 / 4
        else:
            ysize = ysize0 / 4
            ysize_dos = ysize0 / 4.8
        if OPT_EMAX:
            emax = float(OPT_EMAX)
        else:
            emax = eng_emax
        if OPT_EMIN:
            emin = float(OPT_EMIN)
        else:
            emin = eng_emin
        plt.axes([orgx, orgy, xsize, ysize_dos])
        eng = eng - efermi
        plt.plot(eng, dos_total, color="black", linewidth=2, label="total-DOS")
        plt.ylabel("DOS [unit/" + unit + "]")
        plt.xlabel("Energy above Fermi [" + unit + "]")
        plt.axvline(x=0, color="black", linewidth=1)
        plt.xlim([emin, emax])
        plt.ylim(ymin=0)
        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)
        if mode == "K":
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_p, color="black", linewidth=2, label="p")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
        else:
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_s, color="black", linewidth=2, label="s")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
            orgy = orgy + ysize_dos + off
            plt.axes([orgx, orgy, xsize, ysize_dos])
            eng = eng - efermi
            plt.plot(eng, dos_d, color="black", linewidth=2, label="d")
            plt.xticks([])
            plt.xlabel("")
            plt.ylabel("")
            plt.axvline(x=0, color="black", linewidth=1)
            plt.xlim([emin, emax])
            plt.ylim(ymin=0)
            leg = plt.legend(fontsize=12)
            leg.get_frame().set_alpha(0.5)
        orgy = orgy + ysize + off + off + off + off
        plt.axes([orgx, orgy, xsize, ysize])
        plt.plot(eng_xas, xas, color="black", linewidth=2, label="XAS")
        plt.plot(
            eng_xas,
            unbroad,
            linestyle="-",
            color="green",
            linewidth=0.8,
            label="unbroad",
        )
        plt.yticks([])
        plt.xlabel("Energy above Fermi [" + unit + "]")
        plt.ylabel("Absorption [arb. unit]")
        plt.axvline(x=0, color="black", linewidth=1)
        plt.xlim([emin, emax])
        plt.ylim(ymin=0)
        leg = plt.legend(fontsize=12)
        leg.get_frame().set_alpha(0.5)
        if OPT_YMAX:
            plt.ylim(ymax=float(OPT_YMAX))
        else:
            ymax = xspec.get_ymax_xas()
            ymax0 = ymax / 10.0
            ymax = ymax + ymax0 * 1.5
            plt.ylim(ymax=ymax)
        plt.savefig(outname + ".eps")
        plt.savefig(outname + ".pdf")
        plt.savefig(outname + ".png")
        if FLAG_SHOW:
            plt.show()
        plt.close("all")
