"""Chemical endpoints must survive relabelling and inventory permutations."""

import numpy as np
import pytest

import molsysmt as msm


@pytest.mark.parametrize(
    "labels", [["3", "2", "1"], ["alpha", "beta", "gamma"], ["x", "x", "x"]]
)
def test_oxt_assessment_ignores_group_id_labels(labels):
    molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    msm.set(molsys, element="group", group_id=labels)
    assert msm.build.get_missing_terminal_cappings(molsys) == {2: ["OXT"]}


@pytest.mark.parametrize("labels", [["3", "2", "1"], ["alpha", "beta", "gamma"]])
def test_oxt_addition_follows_the_same_chemical_endpoint(labels):
    molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    msm.set(molsys, element="group", group_id=labels)
    before = msm.pyunitwizard.get_value(
        molsys.structures.coordinates, to_unit="nm"
    ).copy()
    result = msm.build.add_missing_terminal_cappings(molsys)
    groups = result.topology.atoms.loc[
        result.topology.atoms["atom_name"] == "OXT", "group_index"
    ].tolist()
    assert groups == [2]
    assert msm.build.get_missing_terminal_cappings(result) == {}
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm"), before
    )


def test_capped_endpoint_does_not_depend_on_cap_labels():
    molsys = msm.build.build_peptide("AceAlaValProNme", engine="MolSysMT")
    msm.set(molsys, element="group", group_id=["z", "d", "c", "b", "a"])
    assert msm.build.get_missing_terminal_cappings(molsys) == {}


def test_a_cyclic_backbone_has_no_free_carboxyl_terminus():
    molsys = msm.build.build_peptide("AlaValPro", engine="MolSysMT")
    atoms = molsys.topology.atoms
    first_n = int(
        atoms[(atoms["group_index"] == 0) & (atoms["atom_name"] == "N")].index[0]
    )
    last_c = int(
        atoms[(atoms["group_index"] == 2) & (atoms["atom_name"] == "C")].index[0]
    )
    molsys.chemical_states.add_bonds([[last_c, first_n]])
    assert msm.build.get_missing_terminal_cappings(molsys) == {}
