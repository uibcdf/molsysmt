"""
Unit and regression test for the get_form module of the molsysmt package.
"""

# Import package, test suite, and other packages as needed
import molsysmt as msm
from molsysmt.native import MolSys


def test_get_component_index_1(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.component.get_component_index(molsys, element='group', selection='all',
                                                       redefine_indices=True)
    assert [0 for ii in range(38)] + [1,2] == output[:40]

def test_get_component_index_2(hp35_solvated_molsys):
    molsys = hp35_solvated_molsys
    output = msm.element.component.get_component_index(molsys, element='component', selection='all',
                                                       redefine_indices=True)
    assert [ii for ii in range(1257)] == output


def test_get_component_index_3():
    molsys = MolSys(
        n_atoms=5,
        n_groups=5,
        n_components=5,
        n_molecules=5,
        n_entities=1,
        n_chains=1,
        n_bonds=2,
    )

    molsys.topology.bonds["atom1_index"] = [0, 2]
    molsys.topology.bonds["atom2_index"] = [1, 3]

    output = msm.element.component.get_component_index(
        molsys, element="atom", selection="all", redefine_indices=True
    )
    assert output == [0, 0, 1, 1, 2]


def test_get_component_index_4():
    molsys = MolSys(
        n_atoms=5,
        n_groups=5,
        n_components=5,
        n_molecules=5,
        n_entities=1,
        n_chains=1,
        n_bonds=2,
    )

    molsys.topology.bonds["atom1_index"] = [0, 2]
    molsys.topology.bonds["atom2_index"] = [1, 3]

    output = msm.element.component.get_component_index(
        molsys, element="component", selection="all", redefine_indices=True
    )
    assert output == [0, 1, 2]
