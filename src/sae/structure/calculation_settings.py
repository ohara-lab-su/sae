# Copyright Kengo NAKADA; SAE class library.
from __future__ import print_function
import os


class CalculationSettings:

    def get_calinfo(self, code="VASP"):
        from sae.vasp.kpoints import ReadVaspKpoints

        NSW = None
        NELM = None
        IBRION = None
        EDIFF = None
        EDIFFG = None
        KP = None
        if code == "VASP" or code == "vasp":
            if os.path.exists("INCAR"):
                module_name = "sae._class_registry"
                if os.path.exists("INCAR"):
                    print("Read VASP INCAR  = INCAR")
                    file_name = "INCAR"
                    class_name = "ReadVaspIncar"
                module = __import__(module_name, globals(), locals(), [class_name], 0)
                klass = getattr(module, class_name)
                incar = klass(file_name)
                NSW = incar.get_nsw()
                NELM = incar.get_nelm()
                IBRION = incar.get_ibrion()
                EDIFF = incar.get_ediff() / 10.0
                EDIFFG = incar.get_ediffg() / 10.0
            if os.path.exists("KPOINTS"):
                kpoints = ReadVaspKpoints("KPOINTS")
                KP = kpoints.get_kpoints_array()
                kx = KP[0:0]
                ky = KP[0:1]
                kz = KP[0:2]
        return (NSW, NELM, IBRION, EDIFF, EDIFFG, KP)
