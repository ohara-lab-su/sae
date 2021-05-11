#!/usr/bin/env python
# cofing:utf-8
"""
吸着エネルギー
"""

import StructureAnalysisEnvironment as SAE

result = SAE.io.ReadVaspOutcar('Pd02_01_35A/OUTCAR')
Pd = SAE.io.ReadVaspOutcar('Pd02_01_35A_atom/OUTCAR')
ZrO2 = SAE.io.ReadVaspOutcar('ZrO2_35A/OUTCAR')

energy = result.toten - (Pd.toten + ZrO2.toten)
adsorption_energy = "{:3f}".format(energy)

print("ISPIN  = %s" % result.ispin)
print("LORBIT = %s" % result.lorbit)
print("NSW    = %s" % result.nsw)
print("IBRION = %s" % result.ibrion)
print("")
print("ENCUT  = %s" % result.encut)
print("")
print("EFERMI = %s" % result.efermi)
print("TOTEN  = %s" % result.toten)
print("VOLUME = %s" % result.volume)
print("")
print("Pd/ZrO2 TOTEN  = %s" % result.toten)
print("Pd      TOTEN  = %s" % Pd.toten)
print("ZrO2    TOTEN  = %s" % ZrO2.toten)
print("---------------")
print("Adsorption Energy = %s" % adsorption_energy)
print("")