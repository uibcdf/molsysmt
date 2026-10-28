"""Exercise path widths, source indices and valid no-match graph queries."""

from copy import deepcopy
from itertools import product

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.fixture
def graph_system():
    builder = msm.MolSysBuilder()
    for name, kind in [
        ("C0", "C"),
        ("H1", "H"),
        ("N2", "N"),
        ("H3", "H"),
        ("O4", "O"),
        ("C5", "C"),
    ]:
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2, 3, 4, 5], group_name="LIG")
    for first, second in [(0, 2), (2, 1), (0, 3)]:
        builder.add_bond(first, second)
    return builder.build()


@pytest.mark.parametrize(
    "path",
    [
        [[], [2]],
        [[4], []],
        [[0], [], [1]],
        [[0], [2], []],
        [[], []],
        [[], [], []],
        [[]],
        [[4], [5]],
        [[0], [4], [5]],
        ['atom_type=="Xe"', 'atom_type=="H"'],
        ['atom_type=="N"', 'atom_type=="Xe"'],
        np.empty((2, 0), dtype=np.int64),
    ],
)
def test_no_matching_walk_retains_integer_source_axis_and_width(graph_system, path):
    before = deepcopy(path)
    result = msm.topology.get_covalent_paths(graph_system, path=path)
    assert result.shape == (0, len(path))
    assert result.dtype == np.dtype(np.int64)
    if isinstance(path, np.ndarray):
        np.testing.assert_array_equal(path, before)
    else:
        assert path == before


@pytest.mark.parametrize("selection", [[0], [], [4, 5], "atom_type=='O'"])
def test_selection_can_remove_an_endpoint_without_changing_result_width(
    graph_system, selection
):
    result = msm.topology.get_covalent_paths(
        graph_system, path=[[0], [2]], selection=selection
    )
    assert result.shape == (0, 2)
    assert result.dtype == np.dtype(np.int64)


@pytest.mark.parametrize(
    "path",
    [
        [[0, 2], [1, 2, 3]],
        [[2], [0], [2]],
        [[4, 0]],
        [[2, 0], [0, 1, 2, 3]],
        [np.array([0, 2], dtype=np.int32), np.array([1, 3], dtype=np.int64)],
    ],
)
def test_nonempty_walks_match_independent_declared_edge_oracle(graph_system, path):
    edges = {frozenset(pair) for pair in [(0, 2), (2, 1), (0, 3)]}
    expected = sorted(
        tuple(walk)
        for walk in product(*path)
        if all(frozenset(pair) in edges for pair in zip(walk, walk[1:]))
    )
    before_pairs = msm.get(graph_system, bonded_atom_pairs=True)
    result = msm.topology.get_covalent_paths(graph_system, path=path)
    assert sorted(map(tuple, result.tolist())) == expected
    assert result.shape == (len(expected), len(path))
    assert result.dtype == np.dtype(np.int64)
    assert msm.get(graph_system, bonded_atom_pairs=True) == before_pairs


@pytest.mark.parametrize(
    "path",
    [
        None,
        [],
        (),
        np.array(0),
        np.empty((0, 2), dtype=int),
        np.ones((1, 1, 1), dtype=int),
        [None, [0]],
        [[[0]], [2]],
    ],
)
def test_invalid_path_specifications_raise_public_argument_error(graph_system, path):
    with pytest.raises(ArgumentError):
        msm.topology.get_covalent_paths(graph_system, path=path)


@pytest.mark.parametrize(
    "path",
    [
        [[], [-1]],
        [[], [6]],
        [[], [0.5]],
        [[], [True]],
        [[], [True, 1]],
        [[], [np.bool_(False), 2]],
        [[], "atom_type==="],
    ],
)
def test_empty_position_does_not_hide_invalid_other_positions(graph_system, path):
    with pytest.raises(ArgumentError):
        msm.topology.get_covalent_paths(graph_system, path=path)


def test_custom_hydrogen_free_donor_returns_two_column_empty_result(graph_system):
    pairs = msm.interactions.hbonds.get_donor_atoms(
        graph_system,
        inclusion_rules=("atom_type=='O'",),
        default_inclusion_rules=False,
        default_exclusion_rules=False,
    )
    assert pairs.shape == (0, 2)
    assert pairs.dtype == np.dtype(np.int64)


def test_valid_interleaved_donor_pairs_preserve_their_source_correspondence(
    graph_system,
):
    pairs = msm.interactions.hbonds.get_donor_atoms(
        graph_system,
        inclusion_rules=("atom_type=='N'",),
        default_inclusion_rules=False,
        default_exclusion_rules=False,
    )
    np.testing.assert_array_equal(pairs, [[2, 1]])


@pytest.mark.parametrize(
    "form", ["molsysmt.Topology", "molsysmt.TopologyDict", "file:h5msm"]
)
def test_supported_graph_forms_preserve_matches_and_empty_width(
    graph_system, form, tmp_path
):
    topology = msm.convert(graph_system, to_form="molsysmt.Topology")
    target = str(tmp_path / "graph.h5msm") if form == "file:h5msm" else form
    source = msm.convert(topology, to_form=target)
    pairs = msm.topology.get_covalent_paths(
        source, path=[[2], [1]], selection=[1, 2, 4]
    )
    np.testing.assert_array_equal(pairs, [[2, 1]])
    empty = msm.topology.get_covalent_paths(source, path=[[4], []])
    assert empty.shape == (0, 2)
    assert empty.dtype == np.dtype(np.int64)


def test_string_positions_match_numeric_candidates_in_declared_syntax(graph_system):
    numeric = msm.topology.get_covalent_paths(graph_system, path=[[2], [1, 3]])
    native = msm.topology.get_covalent_paths(
        graph_system, path=['atom_type=="N"', 'atom_type=="H"']
    )
    np.testing.assert_array_equal(native, numeric)
    pytest.importorskip("mdtraj")
    external = msm.topology.get_covalent_paths(
        graph_system,
        path=["element N", "element H"],
        selection="index 1 2 3",
        syntax="MDTraj",
    )
    np.testing.assert_array_equal(external, numeric)
    with pytest.raises(ArgumentError):
        msm.topology.get_covalent_paths(graph_system, path=[[], [1.5]], syntax="MDTraj")


def test_readonly_candidate_arrays_are_not_changed(graph_system):
    candidates = np.array([[2, 0], [1, 3]], dtype=np.int32)
    candidates.flags.writeable = False
    before = candidates.copy()
    pairs = msm.topology.get_covalent_paths(graph_system, path=candidates)
    assert sorted(map(tuple, pairs)) == [(0, 3), (2, 1)]
    np.testing.assert_array_equal(candidates, before)
    assert candidates.dtype == np.dtype(np.int32)
    assert not candidates.flags.writeable


def test_trusted_delegation_retains_valid_empty_and_nonempty_contract(graph_system):
    pairs = msm.topology.get_covalent_paths(
        graph_system, path=[[2], [1]], skip_digestion=True
    )
    np.testing.assert_array_equal(pairs, [[2, 1]])
    empty = msm.topology.get_covalent_paths(
        graph_system, path=[[], [1]], skip_digestion=True
    )
    assert empty.shape == (0, 2)


@pytest.mark.parametrize(
    "selector", [2, np.int32(2), (2,), range(2, 3), np.array([2], dtype=object)]
)
def test_equivalent_integer_candidate_representations(graph_system, selector):
    pairs = msm.topology.get_covalent_paths(graph_system, path=[selector, [1]])
    np.testing.assert_array_equal(pairs, [[2, 1]])
