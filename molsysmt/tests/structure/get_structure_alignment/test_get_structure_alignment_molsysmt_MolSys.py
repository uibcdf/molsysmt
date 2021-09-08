"""
Unit and regression test for the get_structure_alignment module of the molsysmt package on molsysmt MolSys molecular
systems.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np
import math as math

# Distance between atoms in space and time

def test_get_structure_alignment_molsysmt_MolSys_1():
    molsys_1 = msm.demo.classes.T4_Lysozyme_L99A_in_pdbid_181l(to_form='molsysmt.MolSys')
    molsys_1 = msm.extract(molsys_1, selection='molecule_type=="protein"')
    molsys_2 = msm.demo.files['1l17.mmtf']
    molsys_2 = msm.convert(molsys_2, to_form='molsysmt.MolSys', selection='molecule_type=="protein"')
    molsys_2on1 = msm.structure.get_structure_alignment(molsys_2, reference_molecular_system=molsys_1)
    identity, sel1, sel2 = msm.topology.get_sequence_identity(molsys_2, reference_molecular_system=molsys_1,
                                                              target_intersection_set='atom')
    rmsd = msm.structure.get_rmsd(molsys_2on1, selection=sel2, reference_molecular_system=molsys_1, reference_selection=sel1)
    check = math.isclose(0.0653792023815944, msm.puw.get_value(rmsd, to_unit='nm')[0])
    assert check


