"""
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt import systems
from molsysmt import pyunitwizard as puw
import numpy as np

def test_get_non_bonded_potential_energy_1():

    import molsysmt as msm

    molecular_system = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    U1nb2 = msm.molecular_mechanics.get_non_bonded_potential_energy(molecular_system,
                                                              selection='molecule_name=="BARNASE"',
                                                              selection_2='molecule_name=="BARSTAR"')

    assert puw.get_unit(U1nb2)==puw.unit('kilojoule/mole')

def test_get_non_bonded_potential_energy_2():

    import molsysmt as msm

    molecular_system = msm.convert(msm.systems['Barnase-Barstar']['barnase_barstar.h5msm'])

    U12_groups = msm.molecular_mechanics.get_non_bonded_potential_energy(molecular_system,
                                                              selection='all in groups of group_index in [0,1,2]',
                                                              selection_2='all in groups of group_index in [100,101,102]')

    assert U12_groups.shape==(3,3)
    assert puw.get_unit(U12_groups)==puw.unit('kilojoule/mole')

