"""Validate supplied classic donor anchors and intact covalent donor-H rows."""

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError

METHODS = ["get_buch_hbonds", "get_luzard_chandler_hbonds"]


@pytest.fixture
def water_system():
    source = msm.convert(Chem.AddHs(Chem.MolFromSmiles("O.O")))
    source.structures.append(
        coordinates=puw.quantity(
            [
                [
                    [0, 0, 0],
                    [0.28, 0, 0],
                    [0.1, 0, 0],
                    [0, 0.1, 0],
                    [0.28, 0.1, 0],
                    [0.28, 0, 0.1],
                ],
                [
                    [0, 0, 0],
                    [0.8, 0, 0],
                    [0.1, 0, 0],
                    [0, 0.1, 0],
                    [0.8, 0.1, 0],
                    [0.8, 0, 0.1],
                ],
                [
                    [0, 0, 0],
                    [0.28, 0, 0],
                    [0, 0.1, 0],
                    [0, 0, 0.1],
                    [0.18, 0, 0],
                    [0.28, 0.1, 0],
                ],
            ],
            "nm",
        )
    )
    return source


def calculate(method, source, **kwargs):
    return getattr(msm.interactions.hbonds, method)(source, pbc=False, **kwargs)


def assert_observations(actual, expected):
    for column, reference in zip(actual, expected):
        assert len(column) == len(reference)
        for observed, wanted in zip(column, reference):
            if puw.is_quantity(wanted):
                np.testing.assert_allclose(
                    puw.get_value(observed, to_unit=puw.get_unit(wanted)),
                    puw.get_value(wanted),
                )
            else:
                np.testing.assert_array_equal(observed, wanted)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("donors", [[0, 1], [[0, 2], [0, 3], [1, 4], [1, 5]]])
@pytest.mark.parametrize("form", ["native", "h5msm", "composite", "rdkit"])
def test_precomputed_roles_match_automatic_on_source_forms(
    water_system, method, donors, form, tmp_path
):
    source = water_system
    if form == "h5msm":
        source = str(tmp_path / "source.h5msm")
        msm.convert(water_system, to_form=source)
    elif form == "composite":
        source = [source.topology, source.chemical_states, source.structures]
    elif form == "rdkit":
        source = msm.convert(source, to_form="rdkit.Mol")
    frames = [2, 1, 0, 2]
    expected = calculate(method, source, structure_indices=frames)
    actual = calculate(
        method, source, donors=donors, acceptors=[0, 1], structure_indices=frames
    )
    assert_observations(actual, expected)
    assert [row.tolist() for row in actual[0]] == [
        [[1, 4, 0]],
        [],
        [[0, 2, 1]],
        [[1, 4, 0]],
    ]


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("pairs", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_precomputed_donors_on_both_selection_sides(
    water_system, method, pairs, reverse
):
    first, second = ([1], [0]) if reverse else ([0], [1])
    left = [[first[0], 4 if reverse else 2]] if pairs else first
    right = [[second[0], 2 if reverse else 4]] if pairs else second
    actual = calculate(
        method,
        water_system,
        selection=first,
        selection_2=second,
        donors=left,
        donors_2=right,
        acceptors=first,
        acceptors_2=second,
        structure_indices=[2, 1, 0],
    )
    expected = calculate(
        method,
        water_system,
        selection=first,
        selection_2=second,
        structure_indices=[2, 1, 0],
    )
    assert_observations(actual, expected)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("donors", [[], np.empty((0, 2), dtype=np.int64)])
def test_empty_precomputed_donors_keep_shaped_results(water_system, method, donors):
    result = calculate(
        method, water_system, donors=donors, acceptors=[1], structure_indices=[2, 0]
    )
    assert result[0].shape == (2, 0, 3) and result[0].dtype == np.int64
    assert all(column.shape == (2, 0) for column in result[1:])


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("argument", ["donors", "donors_2"])
@pytest.mark.parametrize(
    "bad",
    [
        [True],
        [0, True],
        [0.0],
        ["0"],
        [-1],
        [6],
        [[0, 4]],
        [[2, 0]],
        [[0, 1]],
        [[0, 0]],
        [[0, 2, 3]],
        [[[0, 2]]],
        [[0, True]],
        [[0], [1, 4]],
    ],
)
def test_invalid_donor_indices_or_pairs_raise_argument_error(
    water_system, method, argument, bad
):
    with pytest.raises(ArgumentError):
        calculate(method, water_system, **{argument: bad})


@pytest.mark.parametrize("method", METHODS)
def test_readonly_noncontiguous_pairs_deduplicate_without_mutation(
    water_system, method
):
    backing = np.array([[1, 99, 4, 99], [0, 99, 2, 99], [0, 99, 2, 99]], dtype=np.int64)
    pairs = backing[:, ::2]
    pairs.setflags(write=False)
    original = backing.copy()
    atoms = water_system.topology.atoms.copy(deep=True)
    bonds = water_system.chemical_states.get_bonds().copy(deep=True)
    result = calculate(method, water_system, donors=pairs, acceptors=[0, 1])
    assert_observations(result, calculate(method, water_system))
    np.testing.assert_array_equal(backing, original)
    assert not pairs.flags.writeable
    pd.testing.assert_frame_equal(
        atoms, water_system.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        bonds, water_system.chemical_states.get_bonds(), check_frame_type=False
    )


@pytest.mark.parametrize("method", METHODS)
def test_explicit_pairs_remain_a_subset_and_validate_even_outside_selection(
    water_system, method
):
    result = calculate(
        method, water_system, donors=[[0, 3]], acceptors=[1], structure_indices=[0]
    )
    assert result[0].shape == (1, 0, 3)
    with pytest.raises(ArgumentError):
        calculate(method, water_system, selection=[], donors=[[0, 4]])


@pytest.mark.parametrize("method", METHODS)
def test_sparse_output_restriction_is_preserved(water_system, method):
    with pytest.raises(NotImplementedMethodError):
        calculate(
            method, water_system, donors=[[0, 2]], output_type="molsysmt.Interactions"
        )


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("donors", [0, np.int32(0), (0,), range(1)])
def test_single_anchor_inputs_expand_only_existing_covalent_hydrogens(
    water_system, method, donors
):
    result = calculate(
        method, water_system, donors=donors, acceptors=[1], structure_indices=[0]
    )
    np.testing.assert_array_equal(result[0], [[[0, 2, 1]]])
    np.testing.assert_allclose(
        puw.get_value(result[1], to_unit="nm"),
        [[0.18 if method == "get_buch_hbonds" else 0.28]],
    )


@pytest.mark.parametrize("method", METHODS)
def test_supplied_roles_retain_geometry_under_nondefault_units(water_system, method):
    water_system.structures.coordinates = puw.convert(
        water_system.structures.coordinates, to_unit="angstrom"
    )
    puw.configure.set_standard_units(
        ["angstrom", "ps", "K", "mole", "dalton", "e", "kJ/mol", "degrees"]
    )
    result = calculate(
        method, water_system, donors=[[0, 2]], acceptors=[1], structure_indices=[0]
    )
    np.testing.assert_array_equal(result[0], [[[0, 2, 1]]])
    np.testing.assert_allclose(
        puw.get_value(result[1], to_unit="nm"),
        [[0.18 if method == "get_buch_hbonds" else 0.28]],
    )
    if len(result) == 3:
        np.testing.assert_allclose(puw.get_value(result[2], to_unit="radians"), [[0]])


@pytest.mark.parametrize("method", METHODS)
def test_trusted_normalized_pairs_use_the_same_resolution(water_system, method):
    args = dict(
        donors=np.array([[0, 2]], dtype=np.int64),
        acceptors=np.array([1], dtype=np.int64),
        distance_threshold=puw.quantity(
            0.23 if method == "get_buch_hbonds" else 0.35, "nm"
        ),
    )
    if method == "get_luzard_chandler_hbonds":
        args["angle_threshold"] = puw.quantity(np.pi / 6, "radians")
    assert_observations(
        calculate(method, water_system, skip_digestion=True, **args),
        calculate(method, water_system, **args),
    )


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("donors", [[0], [[0, 2]]])
@pytest.mark.parametrize("symbol", [None, "unknown", "X"])
def test_unknown_elements_are_not_accepted_as_heavy_donors(
    water_system, method, donors, symbol
):
    water_system.topology.atoms.loc[0, "atom_type"] = symbol
    with pytest.raises(ArgumentError):
        calculate(method, water_system, donors=donors)
