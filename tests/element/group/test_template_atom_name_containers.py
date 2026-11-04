"""Keeping template reference indices independent of the atom-name container."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, InternalAlgorithmError

CASES = (
    ("saccharide", "NAG", ("C1", "C2", "C3")),
    ("small_molecule", "ATP", ("PG", "O1G", "O2G")),
    ("terminal_capping", "ACE", ("CH3", "C", "O")),
)


def _lookup(case, names, *, dispatcher, **kwargs):
    family, group_name, _ = case
    module = msm.element.group if dispatcher else getattr(msm.element.group, family)
    return module.get_bonded_atom_pairs(group_name, names, **kwargs)


def _expected(case, explicit, sorted_output):
    # Independent selected reference edges: C1-C2/C2-C3, PG-O1G/PG-O2G,
    # and CH3-C/C-O. Explicit labels deliberately reverse endpoint ordering.
    if case[0] == "small_molecule":
        return [[1009, 1040], [1030, 1040]] if explicit else [[0, 1], [0, 2]]
    if not explicit:
        return [[0, 1], [1, 2]]
    if sorted_output:
        return [[1009, 1030], [1009, 1040]]
    return [[1009, 1040], [1009, 1030]]


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("dispatcher", [False, True])
@pytest.mark.parametrize("container", [list, tuple, np.asarray])
@pytest.mark.parametrize("explicit", [False, True])
@pytest.mark.parametrize("sorted_output", [False, True])
def test_lists_tuples_and_arrays_preserve_reference_pairs(
    case, dispatcher, container, explicit, sorted_output
):
    names = container(case[2])
    indices = [1040, 1009, 1030] if explicit else None
    original = list(names)
    result = _lookup(
        case, names, dispatcher=dispatcher, atom_indices=indices, sorted=sorted_output
    )
    assert result == _expected(case, explicit, sorted_output)
    assert isinstance(result, list) and all(isinstance(pair, list) for pair in result)
    assert all(
        isinstance(index, (int, np.integer)) for pair in result for index in pair
    )
    assert list(names) == original
    assert indices is None or indices == [1040, 1009, 1030]


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("dispatcher", [False, True])
def test_strided_readonly_names_and_index_labels_are_preserved(case, dispatcher):
    names_storage = np.asarray(
        [value for name in case[2] for value in (name, "unused")]
    )
    index_storage = np.asarray([1040, -99, 1009, -99, 1030, -99], dtype=np.int64)
    names, indices = names_storage[::2], index_storage[::2]
    names.setflags(write=False)
    indices.setflags(write=False)
    original_names, original_indices = names_storage.copy(), index_storage.copy()
    result = _lookup(case, names, dispatcher=dispatcher, atom_indices=indices)
    assert result == _expected(case, True, True)
    np.testing.assert_array_equal(names_storage, original_names)
    np.testing.assert_array_equal(index_storage, original_indices)


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("dispatcher", [False, True])
@pytest.mark.parametrize("container", [list, tuple, np.asarray])
def test_repeated_names_keep_the_first_occurrence(case, dispatcher, container):
    names = container([case[2][0], case[2][1], case[2][0]])
    result = _lookup(
        case, names, dispatcher=dispatcher, atom_indices=[1040, 1009, 1030]
    )
    assert result == [[1009, 1040]]


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("dispatcher", [False, True])
@pytest.mark.parametrize("container", [list, tuple, np.asarray])
def test_empty_atom_names_keep_empty_reference_pairs(case, dispatcher, container):
    assert _lookup(case, container([]), dispatcher=dispatcher) == []


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("dispatcher", [False, True])
@pytest.mark.parametrize("bad", ["C", np.asarray("C"), [["C", "O"]], [1], ["C", 1]])
def test_nonflat_or_nonstring_names_raise_argument_error(case, dispatcher, bad):
    with pytest.raises(ArgumentError, match="one-dimensional"):
        _lookup(case, bad, dispatcher=dispatcher)


@pytest.mark.parametrize("case", CASES)
def test_unknown_group_and_unmatched_layout_keep_family_behavior(case, capsys):
    family, group_name, names = case
    function = getattr(msm.element.group, family).get_bonded_atom_pairs
    if family == "small_molecule":
        assert function("not_a_group", list(names)) == []
        assert function(group_name, ["unknown_atom"]) == []
    else:
        with pytest.raises(InternalAlgorithmError):
            function("not_a_group", list(names))
        with pytest.raises(InternalAlgorithmError):
            function(group_name, ["unknown_atom"])
    capsys.readouterr()
