"""Protecting peptide candidates against false adjacency and chain mixing."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures


def _alanines(chains, nitrogen_positions=None, atom_order=None):
    """Make complete heavy-atom alanines without declaring any covalent edges."""
    names = ("N", "CA", "C", "O", "CB")
    lines = []
    for group_index, chain in enumerate(chains):
        carbon = 3.4 * group_index
        nitrogen = carbon - 2.0
        if nitrogen_positions and group_index in nitrogen_positions:
            nitrogen = nitrogen_positions[group_index]
        positions = (
            (nitrogen, 0.0, 0.0),
            (carbon - 1.0, 0.0, 0.0),
            (carbon, 0.0, 0.0),
            (carbon, 1.2, 0.0),
            (carbon - 1.0, 0.0, 1.5),
        )
        for offset, (name, (x, y, z)) in enumerate(zip(names, positions)):
            serial = 5 * group_index + offset + 1
            lines.append(
                f"ATOM  {serial:5d} {name:^4} ALA {chain}{group_index + 1:4d}    "
                f"{x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{0.0:6.2f}          {name[0]:>2}  "
            )
        if group_index + 1 < len(chains) and chains[group_index + 1] != chain:
            lines.append("TER")
    if atom_order is not None:
        assert all(line.startswith("ATOM") for line in lines)
        lines = [lines[index] for index in atom_order]
    return msm.convert(
        "\n".join([*lines, "END", ""]),
        to_form="molsysmt.MolSys",
        get_missing_bonds=False,
    )


def _intragroup_edges(groups):
    # An independent heavy-atom ALA oracle: N-CA, CA-C, CA-CB, C-O.
    return sorted(
        [
            [5 * group + a, 5 * group + b]
            for group in groups
            for a, b in ((0, 1), (1, 2), (1, 4), (2, 3))
        ]
    )


def test_separate_chains_do_not_acquire_a_peptide_bond():
    source = _alanines(["A", "B"])
    coordinates = puw.get_value(msm.get(source, coordinates=True), to_unit="angstrom")
    assert msm.get(source, element="group", chain_index=True) == [0, 1]
    assert msm.build.get_missing_bonds(source, pbc=False) == _intragroup_edges([0, 1])
    assert msm.get(source, n_bonds=True) == 0
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, coordinates=True), to_unit="angstrom"),
        coordinates,
    )


@pytest.mark.parametrize("selection", ["group_index in [0, 2]", [2, 10]])
def test_selection_gap_does_not_create_adjacency(selection):
    source = _alanines(["A", "A", "A"], nitrogen_positions={2: 1.4})
    expected = _intragroup_edges([0, 2]) if isinstance(selection, str) else []
    assert (
        msm.build.get_missing_bonds(source, selection=selection, pbc=False) == expected
    )


def test_nearby_nonadjacent_group_is_not_a_peptide_neighbor():
    source = _alanines(["A", "A", "A"], nitrogen_positions={2: 1.4})
    expected = sorted([*_intragroup_edges([0, 1, 2]), [2, 5]])
    assert msm.build.get_missing_bonds(source, pbc=False) == expected


@pytest.mark.parametrize("selection", ["all", [2, 5], "group_index in [0, 1]"])
def test_adjacent_amino_acid_groups_in_one_chain_keep_their_candidate(selection):
    source = _alanines(["A", "A"])
    expected = (
        [[2, 5]]
        if isinstance(selection, list)
        else sorted([*_intragroup_edges([0, 1]), [2, 5]])
    )
    assert (
        msm.build.get_missing_bonds(source, selection=selection, pbc=False) == expected
    )


def test_distance_threshold_can_reject_an_adjacent_candidate():
    source = _alanines(["A", "A"])
    assert msm.build.get_missing_bonds(source, max_bond_length="100 pm", pbc=False) == (
        _intragroup_edges([0, 1])
    )


def test_group_ids_do_not_define_index_adjacency():
    source = _alanines(["A", "A"])
    msm.set(source, element="group", group_id=["10", "99"])
    assert msm.build.get_missing_bonds(source, selection=[2, 5], pbc=False) == [[2, 5]]
    assert msm.get(source, element="group", group_id=True) == ["10", "99"]


def test_ambiguous_group_chain_membership_is_not_used_for_a_peptide_candidate():
    source = _alanines(["A", "B"])
    msm.set(source, element="atom", chain_index=[0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    assert set(msm.get(source, element="group", chain_index=True)[0]) == {0, 1}
    assert msm.build.get_missing_bonds(source, pbc=False) == _intragroup_edges([0, 1])


def test_missing_group_chain_membership_is_not_used_for_a_peptide_candidate():
    source = _alanines(["A", "A"])
    msm.set(source, element="atom", selection=[0, 1, 2, 3, 4], chain_index=[None] * 5)
    assert msm.get(source, element="group", chain_index=True) == [None, 0]
    assert msm.build.get_missing_bonds(source, pbc=False) == _intragroup_edges([0, 1])


@pytest.mark.parametrize("structure_index", [0, 1])
def test_structure_index_selects_the_candidate_geometry(structure_index):
    source = _alanines(["A", "A"])
    first = puw.get_value(msm.get(source, coordinates=True), to_unit="angstrom")[0]
    second = first.copy()
    second[5, 0] = 8.6
    source.structures = Structures(
        coordinates=puw.quantity(np.stack([first, second]), "angstrom"),
        structure_id=["10", "200"],
    )
    expected = _intragroup_edges([0, 1])
    if structure_index == 0:
        expected = sorted([*expected, [2, 5]])
    assert (
        msm.build.get_missing_bonds(source, structure_index=structure_index, pbc=False)
        == expected
    )


def test_empty_atom_selection_has_no_candidates():
    source = _alanines(["A", "A"])
    assert msm.build.get_missing_bonds(source, selection=[], pbc=False) == []


def test_atom_reordering_preserves_explicit_peptide_pair_correspondence():
    permutation = [0, 5, 7, 10, 12, 1, 6, 11, 2, 3, 4, 8, 9, 13, 14]
    reordered = _alanines(["A", "A", "A"], atom_order=permutation)
    assert msm.get(reordered, element="atom", atom_id=True) == [
        str(index + 1) for index in permutation
    ]
    inverse = {original: new for new, original in enumerate(permutation)}
    original_pairs = [*_intragroup_edges([0, 1, 2]), [2, 5], [7, 10]]
    expected = sorted(sorted([inverse[a], inverse[b]]) for a, b in original_pairs)
    assert msm.build.get_missing_bonds(reordered, pbc=False) == expected


@pytest.mark.parametrize("pbc", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_paired_peptide_distance_respects_pbc_and_user_units(pbc, unit):
    source = _alanines(["A", "A"], nitrogen_positions={1: 8.6})
    msm.set(source, box=puw.quantity(np.eye(3)[None] * 10.0, "angstrom"))
    coordinates = msm.get(source, coordinates=True)
    msm.set(source, coordinates=puw.convert(coordinates, to_unit=unit))
    expected = _intragroup_edges([0, 1])
    if pbc:
        expected = sorted([*expected, [2, 5]])
    with puw.context(standard_units=[unit, "ps"]):
        assert msm.build.get_missing_bonds(source, pbc=pbc) == expected


def test_h5msm_input_uses_the_same_chain_constraints(tmp_path):
    source = _alanines(["A", "B"])
    filename = str(tmp_path / "separate_chains.h5msm")
    msm.convert(source, to_form=filename)
    assert msm.build.get_missing_bonds(filename, pbc=False) == _intragroup_edges([0, 1])


def test_add_missing_bonds_preserves_the_chain_boundary_and_source_copy():
    source = _alanines(["A", "B"])
    result = msm.build.add_missing_bonds(source, in_place=False)
    assert msm.get(result, bonded_atom_pairs=True) == _intragroup_edges([0, 1])
    assert msm.get(source, n_bonds=True) == 0


def test_existing_declared_bonds_are_not_removed_or_returned_as_missing():
    source = _alanines(["A", "B"])
    source.topology.add_bonds([[2, 5]])
    assert msm.build.get_missing_bonds(source, pbc=False) == _intragroup_edges([0, 1])
    assert msm.get(source, bonded_atom_pairs=True) == [[2, 5]]
