"""Protecting peptide-end cap names independently of their connecting atom."""

import pytest

from molsysmt.element.group.terminal_capping import (
    c_terminal_capping_names,
    get_bonded_atom_pairs,
    get_group_db,
    group_names,
    is_c_terminal_capping,
    is_n_terminal_capping,
    is_terminal_capping,
    n_terminal_capping_names,
)


@pytest.mark.parametrize("name", ["ACE", "NME", "NHE", "NH2"])
def test_caps_are_named_after_the_peptide_end(name):
    assert is_terminal_capping(name) is True
    assert is_n_terminal_capping(name) is (name == "ACE")
    assert is_c_terminal_capping(name) is (name != "ACE")


def test_resource_partition_matches_the_public_end_contract():
    assert set(n_terminal_capping_names) == {"ACE"}
    assert set(c_terminal_capping_names) == {"NME", "NHE", "NH2"}
    assert set(group_names) == {"ACE", "NME", "NHE", "NH2"}


@pytest.mark.parametrize("name", ["ace", "nme", "nh2", "ALA", "UNKNOWN", "", None])
def test_unrecognized_or_lowercase_labels_remain_unrecognized(name):
    assert is_terminal_capping(name) is False
    assert is_n_terminal_capping(name) is False
    assert is_c_terminal_capping(name) is False


@pytest.mark.parametrize("name", ["ACE", "NME", "NHE", "NH2"])
def test_every_stored_atom_naming_variant_keeps_its_connectivity(name):
    database = get_group_db(name)
    assert database["name"] == name
    for template in database["topology"]:
        atoms = template["atoms"]
        if name == "ACE":
            expected = [("C", "O"), ("C", "CH3")]
            expected += [
                ("CH3", atom) for atom in atoms if atom not in {"C", "O", "CH3"}
            ]
        elif name == "NME":
            methyl = "CH3" if "CH3" in atoms else "C"
            expected = [("N", methyl), ("N", "H")]
            expected += [
                (methyl, atom) for atom in atoms if atom not in {"N", methyl, "H"}
            ]
        else:
            expected = [("N", "H1"), ("N", "H2")]
        observed = get_bonded_atom_pairs(name, atoms)
        observed_names = {frozenset((atoms[a], atoms[b])) for a, b in observed}
        assert observed_names == {frozenset(pair) for pair in expected}
