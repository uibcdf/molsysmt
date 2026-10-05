"""Protect the sparse-result boundary against silent index coercion."""

import copy

import numpy as np
import pytest
from argdigest.core.errors import UnknownArgumentError

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


def _record(structure=0):
    return {
        "structure_index": structure,
        "interaction_type": "hbond",
        "participants": [
            {"role": "donor", "atom_indices": [0]},
            {"role": "hydrogen", "atom_indices": [1]},
            {"role": "acceptor", "atom_indices": [2]},
        ],
        "measurements": {"distance": 0.2},
    }


def _result(records=None, **options):
    arguments = dict(
        n_atoms=3,
        n_structures=3,
        evaluated_structure_indices=[0, 1, 2],
        method="synthetic",
        measure_units={"distance": "nm"},
    )
    arguments.update(options)
    return msm.Interactions.from_records(
        [_record(), _record()] if records is None else records, **arguments
    )


@pytest.fixture(params=["original", "invalidated", "recalculated"])
def result(request):
    original = _result()
    if request.param == "invalidated":
        return original.invalidate_structures([2])
    if request.param == "recalculated":
        return original.replace_structures(
            _result([_record(1)], evaluated_structure_indices=[1])
        )
    return original


@pytest.mark.parametrize("value", [True, np.bool_(False), 1.5, "3", -1])
@pytest.mark.parametrize(
    "name", ["n_atoms", "n_structures", "source_n_atoms", "source_n_structures"]
)
def test_counts_are_integers_without_truncation(name, value):
    with pytest.raises(ArgumentError):
        _result([], **{name: value})


@pytest.mark.parametrize("name", ["structure_indices", "atom_indices"])
@pytest.mark.parametrize("value", [[True], [0.9], [[0]], "all"])
def test_queries_reject_invalid_local_indices_on_every_storage_route(
    result, name, value
):
    coverage = result.evaluated_structure_indices.copy()
    with pytest.raises(ValueError):
        result.query(**{name: value})
    np.testing.assert_array_equal(result.evaluated_structure_indices, coverage)


def test_between_rejects_boolean_exclusive_on_every_storage_route(result):
    with pytest.raises(ArgumentError):
        result.between([0], [2], exclusive="false")


@pytest.mark.parametrize("field", ["structure", "atom", "image"])
def test_record_indices_are_checked_before_integer_encoding(field):
    record = _record()
    if field == "structure":
        record["structure_index"] = 0.9
    elif field == "atom":
        record["participants"][0]["atom_indices"] = [0.9]
    else:
        record["images"] = [[2**32, 0, 0], [0, 0, 0], [0, 0, 0]]
    with pytest.raises(ValueError, match="integer"):
        _result([record])


@pytest.mark.parametrize(
    "column,value",
    [
        ("participant_atoms", np.asarray([0.9, 1, 2])),
        ("occurrence_evidence", np.asarray([0.9, 0])),
        ("n_atoms", 3.5),
    ],
)
def test_typed_constructor_refuses_float_columns_before_casting(column, value):
    original = _result()
    payload = msm.convert(original, to_form="molsysmt.InteractionsDict")
    # The typed decoder must use the same checked constructor as direct users.
    malformed = copy.deepcopy(payload)
    malformed.data[column] = value
    with pytest.raises((ValueError, ArgumentError), match="integer"):
        msm.convert(malformed, to_form="molsysmt.Interactions")


def test_generators_are_consumed_once_and_empty_selections_keep_integer_shapes(result):
    yielded = []

    def records():
        for index in (0, 2):
            yielded.append(index)
            yield _record(index)

    generated = _result(records())
    assert yielded == [0, 2]
    assert generated.n_interactions == 2
    empty = result.query(structure_indices=[], atom_indices=[]).to_dict()
    assert empty["occurrence_indices"].dtype == np.int64
    assert empty["occurrence_indices"].shape == (0,)
    empty_array = result.query(structure_indices=np.array([])).to_dict()
    assert empty_array["evaluated_structure_indices"].dtype == np.int64
    assert empty_array["evaluated_structure_indices"].shape == (0,)
    selected = result.query(
        np.asarray([2, 0, 2]), interaction_types=(x for x in ["hbond"])
    )
    np.testing.assert_array_equal(
        selected.to_dict()["evaluated_structure_indices"],
        [index for index in [2, 0] if index in result.evaluated_structure_indices],
    )


def test_invalid_skip_flags_fail_even_on_the_bypass_route(result, tmp_path):
    calls = [
        lambda: result.query(skip_digestion="yes"),
        lambda: result.between([0], [2], skip_digestion=1),
        lambda: result.remap(skip_digestion=1),
        lambda: result.to_dict(skip_digestion=1),
        lambda: result.relation(0, skip_digestion=1),
        lambda: result.invalidate_structures([0], skip_digestion=1),
        lambda: result.replace_structures(_result(), skip_digestion=1),
        lambda: result.save(tmp_path / "invalid.h5i", skip_digestion=1),
        lambda: msm.Interactions.load(tmp_path / "invalid.h5i", skip_digestion=1),
        lambda: _result([], skip_digestion=1),
    ]
    for call in calls:
        with pytest.raises(ArgumentError):
            call()
    assert not (tmp_path / "invalid.h5i").exists()


def test_valid_skip_and_path_inputs_preserve_round_trip_and_parallel_handles(
    result, tmp_path
):
    normal = result.query([1, 0], [0], "incident", "hbond").to_dict()
    skipped = result.query(
        [1, 0], [0], "incident", "hbond", skip_digestion=True
    ).to_dict()
    np.testing.assert_array_equal(
        normal["occurrence_indices"], skipped["occurrence_indices"]
    )
    path = tmp_path / "observations.h5i"
    result.save(path)
    loaded = msm.Interactions.load(path)
    np.testing.assert_array_equal(
        loaded.to_dict()["occurrence_indices"], result.to_dict()["occurrence_indices"]
    )
    np.testing.assert_array_equal(
        loaded.evaluated_structure_indices, result.evaluated_structure_indices
    )


def test_typo_cannot_silently_replace_structure_selection(result):
    with pytest.raises(UnknownArgumentError, match="structure_indicies"):
        result.query(structure_indicies=[0])
