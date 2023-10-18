"""
Unit and regression test for the get_structure_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.systems import tests as tests_systems
import numpy as np

# Distance between atoms in space and time

def test_get_structure_alignment_molsysmt_MolSys_1():

    molsys_1 = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'], to_form='molsysmt.MolSys',
                           selection='molecule_type=="protein"')
    molsys_2 = msm.structure.translate(molsys_1, translation="[2.0, 0.0, 0.0] nm")
    rmsd = msm.structure.get_rmsd(molsys_2, selection='backbone', reference_molecular_system=molsys_1, reference_selection='backbone')
    check = np.isclose(2.0, msm.pyunitwizard.get_value(rmsd, to_unit='nm')[0])
    assert check

def test_get_structure_alignment_molsysmt_MolSys_2():

    molsys_1 = msm.convert(tests_systems['T4 lysozyme L99A']['181l.msmpk'], to_form='molsysmt.MolSys')
    molsys_1 = msm.extract(molsys_1, selection='molecule_type=="protein"')
    molsys_2 = msm.convert(tests_systems['T4 lysozyme L99A']['1l17.msmpk'], to_form='molsysmt.MolSys')
    molsys_2 = msm.convert(molsys_2, to_form='molsysmt.MolSys', selection='molecule_type=="protein"')
    molsys_2on1 = msm.structure.least_rmsd_align(molsys_2, selection='backbone',
                                      reference_molecular_system=molsys_1,
                                      reference_selection='backbone')
    identity, int2, int1 = msm.topology.get_sequence_identity(molsys_2, reference_molecular_system=molsys_1)
    aux1 = msm.select(molsys_1, selection='group_index==@int1')
    sel1 = msm.select(molsys_1, selection='backbone', mask=aux1)
    aux2 = msm.select(molsys_2, selection='group_index==@int2')
    sel2 = msm.select(molsys_2, selection='backbone', mask=aux2)
    rmsd = msm.structure.get_rmsd(molsys_2on1, selection=sel2, reference_molecular_system=molsys_1, reference_selection=sel1)
    check = np.isclose(0.021333623779354657, msm.pyunitwizard.get_value(rmsd, to_unit='nm')[0])

    assert check


