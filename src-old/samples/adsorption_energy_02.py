#!/usr/bin/env python
# cofing:utf-8
"""
様々なエネルギーを作成する
"""

import StructureAnalysisEnvironment as SAE

def total_energy(cluster_prefix):
    """ 全エネルギーを返す
    """
    result = SAE.io.ReadVaspOutcar('%s/OUTCAR' % cluster_prefix)
    return result.toten


def ad_energy(cluster_prefix, lattice_name, debug=False):
    cell = SAE.io.ReadVaspOutcar('%s/OUTCAR' % cluster_prefix)
    Pd = SAE.io.ReadVaspOutcar('%s_atom/OUTCAR' % cluster_prefix)
    ZrO2 = SAE.io.ReadVaspOutcar('%s/OUTCAR' % lattice_name)

    energy = cell.toten - (Pd.toten + ZrO2.toten)

    if debug:
        adsorption_energy = "{:.2f}".format(energy)
        print("%s/ZrO2 TOTEN  = %s" % (cluster_prefix, cell.toten))
        print("%s      TOTEN  = %s" % (cluster_prefix, Pd.toten))
        print("ZrO2    TOTEN  = %s" % ZrO2.toten)
        print("---------------")
        print("Adsorption Energy = %s" % adsorption_energy)
    return energy

# 2021.05.10 明らかに違うものを見ている
    # "Pd04_01",
    # "Pd07_01",

list = (
    "Pd02_01",
    "Pd03_01",
    "Pd05_01",
    "Pd06_01",
    "Pd13_01",
    "Pd19_01",
    )

ad_data = dict()
toten_data = dict()
cluster_data = dict()

print("")
for name in list:
    ad_data[name] = ad_energy(name + '_35A', "ZrO2_35A")
    toten_data[name] = total_energy(name + '_35A')
    cluster_data[name] = total_energy(name + '_35A_atom')
    print("%s: %s  %s  %s" % (
        name,
        "{:.3f}".format(toten_data[name]),
        "{:8.3f}".format(cluster_data[name]),
        "{:8.3f}".format(ad_data[name])
      ))

print("")