"""Checking reference bond indices independently of reference-helper prose."""

import inspect

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import InternalAlgorithmError

# Literal selected reference edges, expressed in the original name order.
CASES = (
    ("", "ALA", ("N", "CA", "C", "O", "CB"), ((0, 1), (1, 2), (1, 4), (2, 3))),
    (
        "amino_acid",
        "ALA",
        ("N", "CA", "C", "O", "CB"),
        ((0, 1), (1, 2), (1, 4), (2, 3)),
    ),
    ("ion", "SO4", ("S", "O1", "O2"), ((0, 1), (0, 2))),
    ("saccharide", "NAG", ("C1", "C2", "C3"), ((0, 1), (1, 2))),
    ("small_molecule", "ATP", ("PG", "O1G", "O2G"), ((0, 1), (0, 2))),
    ("terminal_capping", "ACE", ("CH3", "C", "O"), ((0, 1), (1, 2))),
    ("water", None, ("O", "H1", "H2"), ((0, 1), (0, 2))),
)


def _function(case):
    family = case[0]
    owner = getattr(msm.element.group, family) if family else msm.element.group
    return owner.get_bonded_atom_pairs


def _call(case, names, **kwargs):
    function = _function(case)
    return (
        function(names, **kwargs)
        if case[1] is None
        else function(case[1], names, **kwargs)
    )


def _expected(case, names, indices, sorted_output):
    original = case[2]
    labels = dict(
        zip(names, range(len(names)) if indices is None else indices, strict=True)
    )
    edges = list(case[3])
    if case[0] == "water" and list(names) != list(original):
        edges.reverse()
    pairs = [[labels[original[left]], labels[original[right]]] for left, right in edges]
    if case[0] != "water":
        pairs = [sorted(pair) for pair in pairs]
    return sorted(pairs) if sorted_output else pairs


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("container", [list, tuple, np.asarray])
@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("sorted_output", [False, True])
@pytest.mark.parametrize("reverse_names", [False, True])
def test_reference_pairs_use_local_or_explicit_indices(
    case, container, explicit, sorted_output, reverse_names
):
    names = container(case[2][::-1] if reverse_names else case[2])
    indices = (
        container([1040, 1009, 1030, 1007, 1012][: len(names)]) if explicit else None
    )
    original_names = list(names)
    original_indices = None if indices is None else list(indices)
    result = _call(case, names, atom_indices=indices, sorted=sorted_output)
    assert result == _expected(case, names, indices, sorted_output)
    assert isinstance(result, list)
    assert all(isinstance(pair, list) and len(pair) == 2 for pair in result)
    assert all(
        isinstance(index, (int, np.integer)) for pair in result for index in pair
    )
    assert list(names) == original_names
    if indices is not None:
        assert list(indices) == original_indices


@pytest.mark.parametrize("case", CASES)
def test_reference_lookup_does_not_mutate_readonly_strided_inputs(case):
    names_storage = np.asarray(
        [value for name in case[2] for value in (name, "unused")]
    )
    labels = [1040, 1009, 1030, 1007, 1012][: len(case[2])]
    index_storage = np.asarray([value for label in labels for value in (label, -99)])
    names, indices = names_storage[::2], index_storage[::2]
    names.setflags(write=False)
    indices.setflags(write=False)
    before_names, before_indices = names_storage.copy(), index_storage.copy()
    result = _call(case, names, atom_indices=indices)
    assert result == _expected(case, names, indices, True)
    np.testing.assert_array_equal(names_storage, before_names)
    np.testing.assert_array_equal(index_storage, before_indices)
    assert not names.flags.writeable and not indices.flags.writeable


@pytest.mark.parametrize("case", CASES)
def test_return_help_describes_the_integer_pair_contract(case):
    returns = inspect.getdoc(_function(case)).split("Returns\n-------\n", 1)[1]
    assert returns.splitlines()[0].startswith("list of list of int")
    # The numerical assertion ties the described endpoint type to actual values.
    assert _call(case, list(case[2])) == _expected(case, list(case[2]), None, True)


@pytest.mark.parametrize("case", CASES)
def test_known_empty_queries_return_empty_lists(case):
    assert _call(case, []) == []
    assert _call(case, [], atom_indices=[]) == []


def test_water_keeps_oxygen_first_even_for_descending_labels():
    water = msm.element.group.water.get_bonded_atom_pairs
    assert water(["H2", "O", "H1"], atom_indices=[20, 100, 10], sorted=False) == [
        [100, 20],
        [100, 10],
    ]
    assert water(["H2", "O", "H1"], atom_indices=[20, 100, 10], sorted=True) == [
        [100, 10],
        [100, 20],
    ]
    assert water(["O", "H1"]) == []


def test_amino_acid_duplicate_names_expand_existing_reference_edges():
    result = msm.element.group.amino_acid.get_bonded_atom_pairs(
        "ALA", ["N", "CA", "N"], atom_indices=[1040, 1009, 1030]
    )
    assert result == [[1009, 1030], [1009, 1040]]


def test_ion_duplicate_names_use_the_first_occurrence():
    result = msm.element.group.ion.get_bonded_atom_pairs(
        "SO4", ["S", "O1", "S"], atom_indices=[1040, 1009, 1030]
    )
    assert result == [[1009, 1040]]


def test_amino_acid_unknown_and_unmatched_queries_return_none(capsys):
    function = msm.element.group.amino_acid.get_bonded_atom_pairs
    assert function("not_a_group", ["N", "CA"]) is None
    assert function("ALA", ["not", "atoms"]) is None
    capsys.readouterr()


def test_ion_unknown_and_unmatched_queries_keep_distinct_outcomes():
    function = msm.element.group.ion.get_bonded_atom_pairs
    assert function("not_a_group", ["K"]) == []
    assert function("K", "K", atom_indices=42) == []
    with pytest.raises(InternalAlgorithmError):
        function("not_a_group", ["N", "H"])
    assert function("SO4", ["not", "atoms"]) is None


def test_dispatcher_keeps_unsupported_and_unknown_results(capsys):
    function = msm.element.group.get_bonded_atom_pairs
    assert function("DA", []) is None
    assert function("not_a_group", []) is None
    capsys.readouterr()
