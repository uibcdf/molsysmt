"""Rejecting malformed reference maps before looking up chemical templates."""

import importlib

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, ArgumentLengthError

CASES = (
    ("", "ALA", ["N", "CA", "C"]),
    ("amino_acid", "ALA", ["N", "CA", "C"]),
    ("ion", "SO4", ["S", "O1", "O2"]),
    ("saccharide", "NAG", ["C1", "C2", "C3"]),
    ("small_molecule", "ATP", ["PG", "O1G", "O2G"]),
    ("terminal_capping", "ACE", ["CH3", "C", "O"]),
    ("water", None, ["O", "H1", "H2"]),
)


def _function(case):
    owner = getattr(msm.element.group, case[0]) if case[0] else msm.element.group
    return owner.get_bonded_atom_pairs


def _call(case, indices, *, names=None, **kwargs):
    names = case[2] if names is None else names
    function = _function(case)
    return (
        function(names, atom_indices=indices, **kwargs)
        if case[1] is None
        else function(case[1], names, atom_indices=indices, **kwargs)
    )


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize(
    "indices",
    [
        ["10", "20", "30"],
        [1.0, 2.0, 3.0],
        [True, 2, 3],
        np.asarray([True, False, True]),
        [0, -1, 2],
        [[0, 1, 2]],
        [0, [1], 2],
        np.asarray(1),
        "all",
        1,
        [None, 1, 2],
        [0, 1, np.inf],
        [0, 1, 2**63],
    ],
    ids=[
        "strings",
        "floats",
        "mixed-bool",
        "bool-array",
        "negative",
        "matrix",
        "ragged",
        "zero-dimensional",
        "selection-keyword",
        "scalar-many-names",
        "none-entry",
        "infinity",
        "overflow",
    ],
)
def test_bad_map_values_are_catalogued_argument_errors(case, indices):
    with pytest.raises(ArgumentError) as refusal:
        _call(case, indices)
    assert refusal.value.extra["argument"] == "atom_indices"
    assert refusal.value.extra["caller"] == (
        _function(case).__module__ + ".get_bonded_atom_pairs"
    )


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("indices", [[], [10, 20], [10, 20, 30, 40]])
def test_map_length_has_expected_and_actual_diagnostics(case, indices):
    with pytest.raises(ArgumentLengthError) as refusal:
        _call(case, indices)
    assert refusal.value.extra["argument"] == "atom_indices"
    assert refusal.value.extra["expected"] == 3
    assert refusal.value.extra["actual"] == len(indices)


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("kind", ["quantity", "masked", "array-with-units"])
def test_index_maps_do_not_strip_units_or_masks(case, kind):
    class UnitArray(np.ndarray):
        units = "nm"

    if kind == "quantity":
        indices = msm.pyunitwizard.quantity([10, 20, 30], "nm")
    elif kind == "masked":
        indices = np.ma.array([10, 20, 30], mask=[False, True, False])
    else:
        indices = np.asarray([10, 20, 30]).view(UnitArray)
    with pytest.raises(ArgumentError) as refusal:
        _call(case, indices)
    assert refusal.value.extra["argument"] == "atom_indices"


@pytest.mark.parametrize("case", CASES)
def test_invalid_maps_do_not_read_reference_databases(case, monkeypatch):
    reads = []

    def forbidden(*args, **kwargs):
        reads.append(args)
        pytest.fail("Malformed indices reached a reference lookup.")

    for family in (
        "amino_acid",
        "ion",
        "saccharide",
        "small_molecule",
        "terminal_capping",
    ):
        monkeypatch.setattr(
            getattr(msm.element.group, family), "get_group_db", forbidden
        )
    monkeypatch.setattr(msm.element.atom, "get_atom_type_from_atom_name", forbidden)
    with pytest.raises(ArgumentError):
        _call(case, ["a", "b", "c"])
    assert reads == []


@pytest.mark.parametrize("case", CASES)
@pytest.mark.parametrize("indices", [[], (), np.asarray([])])
def test_empty_parallel_maps_keep_known_empty_results(case, indices):
    assert _call(case, indices, names=[]) == []


@pytest.mark.parametrize("case", CASES)
def test_repeated_indices_remain_a_mapping_not_a_permutation(case):
    result = _call(case, [10, 10, 20])
    # The selected templates are two-edge chains, except sulfate/water stars.
    assert result == ([[10, 10], [10, 20]])


@pytest.mark.parametrize("case", CASES)
def test_unsigned_readonly_strided_maps_preserve_input_and_values(case):
    storage = np.asarray([40, 999, 10, 999, 30, 999], dtype=np.uint16)
    indices = storage[::2]
    indices.setflags(write=False)
    before = storage.copy()
    result = _call(case, indices)
    if case[0] == "water":
        expected = [[40, 10], [40, 30]]
    elif case[0] in {"ion", "small_molecule"}:
        expected = [[10, 40], [30, 40]]
    else:
        expected = [[10, 30], [10, 40]]
    assert result == expected
    np.testing.assert_array_equal(storage, before)
    assert not indices.flags.writeable


@pytest.mark.parametrize("family,name", [("amino_acid", "ALA"), ("ion", "K")])
def test_existing_scalar_single_name_routes_remain_supported(family, name):
    assert (
        getattr(msm.element.group, family).get_bonded_atom_pairs(
            name, "N" if family == "amino_acid" else "K", atom_indices=np.int16(42)
        )
        == []
    )
    assert (
        msm.element.group.get_bonded_atom_pairs(
            name, "N" if family == "amino_acid" else "K", atom_indices=42
        )
        == []
    )


@pytest.mark.parametrize("family", ["amino_acid", "ion"])
def test_existing_trusted_skip_routes_keep_valid_maps(family):
    case = next(case for case in CASES if case[0] == family)
    expected = [[10, 20], [10, 30]] if family == "ion" else [[10, 20], [20, 30]]
    assert _call(case, [10, 20, 30], skip_digestion=True) == expected


@pytest.mark.parametrize("case", CASES)
def test_generic_atom_indices_contract_is_not_replaced(case):
    # Importing any template helper must not narrow the shared selection digester.
    _function(case)
    module = importlib.import_module(
        "molsysmt._private.argdigest.argument.atom_indices"
    )
    assert module.digest_atom_indices("all") == "all"
    assert module.digest_atom_indices(None) is None
    assert len(module.digest_atom_indices([[1], [2, 3]])) == 2
