"""
Unit and regression test for the get module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
import numpy as np


# Get on molsysmt.MolSys

def test_get_molsysmt_MolSys_1():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    output = msm.get(molsys, target='atom', indices=[32,33,34], name=True)
    true_output = np.array(['N', 'CA', 'C'], dtype=object)
    assert np.all(output == true_output)

def test_get_molsysmt_MolSys_2():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    names, group_indices, group_names = msm.get(molsys, target='atom', indices=[32,33,34], name=True, group_index=True, group_name=True)
    true_names = np.array(['N', 'CA', 'C'], dtype=object)
    true_group_indices = np.array([4, 4, 4])
    true_group_names = np.array(['ILE', 'ILE', 'ILE'], dtype=object)
    assert np.all(names == true_names) and np.all(group_indices == true_group_indices) and np.all(group_names == true_group_names)

def test_get_molsysmt_MolSys_3():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    n_groups = msm.get(molsys, target='atom', indices=[32,33,34], n_groups=True)
    true_n_groups = 1
    assert n_groups == true_n_groups

def test_get_molsysmt_MolSys_4():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    names, atom_indices, atom_names = msm.get(molsys, target='group', indices=[10,11,12],
                                            name=True, atom_index=True, atom_name=True)
    true_names = np.array(['LYS', 'CYS', 'ASN'], dtype=object)
    true_atom_indices = np.array([np.array([77, 78, 79, 80, 81, 82, 83, 84, 85]),
       np.array([86, 87, 88, 89, 90, 91]),
       np.array([92, 93, 94, 95, 96, 97, 98, 99])], dtype=object)
    true_atom_names = np.array([np.array(['N', 'CA', 'C', 'O', 'CB', 'CG', 'CD', 'CE', 'NZ'], dtype=object),
       np.array(['N', 'CA', 'C', 'O', 'CB', 'SG'], dtype=object),
       np.array(['N', 'CA', 'C', 'O', 'CB', 'CG', 'OD1', 'ND2'], dtype=object)],
      dtype=object)

    check_names = np.all(names==true_names)
    check_atom_indices = np.all([np.all(ii==jj) for ii,jj in zip(atom_indices, true_atom_indices)])
    check_atom_names = np.all([np.all(ii==jj) for ii,jj in zip(atom_names, true_atom_names)])

    assert check_names and check_atom_indices and check_atom_names

def test_get_molsysmt_MolSys_5():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    n_atoms = msm.get(molsys, target='group', indices=[10,11,12], n_atoms=True)
    assert np.all(n_atoms==np.array([9, 6, 8]))

def test_get_molsysmt_MolSys_6():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    indices, component_indices = msm.get(molsys, target='group', indices=[550, 551, 552],
                                    index=True, component_index=True)
    true_indices = np.array([550, 551, 552])
    true_component_indices = np.array([55, 56, 57])

    check_indices = np.all(indices==true_indices)
    check_component_indices = np.all(component_indices==true_component_indices)

    assert check_indices and check_component_indices

def test_get_molsysmt_MolSys_7():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    n_components = msm.get(molsys, target='group', indices=[550, 551, 552], n_components=True)
    true_n_components = 3
    assert n_components==true_n_components

def test_get_molsysmt_MolSys_8():
    molsys = msm.demo.classes.TcTIM_in_pdbid_1tcd(to_form='molsysmt.MolSys')
    indices, component_indices = msm.get(molsys, target='component', indices=[55, 56, 57],
                                    index=True, group_index=True)
    true_indices = np.array([55, 56, 57])
    true_component_indices = np.array([[550], [551], [552]], dtype=object)

    check_indices = np.all(true_indices==indices)
    check_component_indices = np.all([np.all(ii==jj) for ii,jj in zip(component_indices, true_component_indices)])


