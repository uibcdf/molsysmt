"""Native atom membership follows source hierarchy indices, including empty rows."""

import pytest

import molsysmt as msm


@pytest.mark.parametrize("level", ["group", "chain"])
@pytest.mark.parametrize("form", ["molsysmt.Topology", "molsysmt.MolSys"])
def test_group_free_atoms_do_not_create_parent_memberships(level, form):
    from rdkit import Chem

    source = msm.convert(Chem.MolFromSmiles("CCO"), to_form=form)
    indices, members = msm.get(
        source, element=level, **{level + "_index": True, "atom_index": True}
    )
    assert list(indices) == []
    assert members == []


@pytest.mark.parametrize("level", ["group", "chain", "molecule", "entity"])
@pytest.mark.parametrize(
    "selection,expected",
    [("all", [[3], [0, 1, 2]]), ([1, 0, 1], [[0, 1, 2], [3], [0, 1, 2]]), ([], [])],
)
def test_all_memberships_match_explicit_source_element_order(
    level, selection, expected
):
    from rdkit import Chem

    from molsysmt.native.topology import Chains_DataFrame, Groups_DataFrame

    source = msm.convert(Chem.MolFromSmiles("CCO.N"), to_form="molsysmt.MolSys")
    top = source.topology
    top.groups = Groups_DataFrame(n_groups=2)
    top.groups["group_name"] = ["AMN", "ETH"]
    top.groups["group_type"] = ["small molecule", "small molecule"]
    top.groups["molecule_index"] = [0, 1]
    top.atoms["group_index"] = [1, 1, 1, 0]
    top.chains = Chains_DataFrame(n_chains=2)
    top.chains["chain_id"] = ["A", "B"]
    top.atoms["chain_index"] = [1, 1, 1, 0]
    top.molecules["entity_index"] = [0, 1]
    top._molecules_dirty = False
    top._entities_dirty = False
    assert (
        msm.get(source, element=level, selection=selection, atom_index=True) == expected
    )
    assert source.get(element=level, selection=selection, atom_index=True) == expected


def test_empty_and_unassigned_groups_remain_distinct():
    from rdkit import Chem

    from molsysmt.native.topology import Groups_DataFrame

    top = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.Topology")
    top.groups = Groups_DataFrame(n_groups=3)
    top.atoms["group_index"] = [1, None, 1]
    assert msm.get(top, element="group", atom_index=True) == [[], [0, 2], []]


@pytest.mark.parametrize("level", ["molecule", "entity"])
def test_unassigned_atoms_are_not_attached_to_the_last_parent(level):
    from rdkit import Chem

    from molsysmt.native.topology import Groups_DataFrame

    top = msm.convert(Chem.MolFromSmiles("CCO"), to_form="molsysmt.Topology")
    top.groups = Groups_DataFrame(n_groups=1)
    top.groups["group_name"] = ["LIG"]
    top.groups["molecule_index"] = [0]
    top.atoms["group_index"] = [0, None, 0]
    top._molecules_dirty = False
    assert msm.get(top, element=level, atom_index=True) == [[0, 2]]
