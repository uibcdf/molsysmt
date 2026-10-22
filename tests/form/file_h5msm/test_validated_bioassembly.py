"""Persist normally validated biological operations without extra geometry axes."""

from copy import deepcopy

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import Structures
from tests.native.test_molsys import build_minimal_molsys


def _operation(scope="common", array_translations=False):
    rotation = np.array([[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
    return {
        "chain_indices": [0, 1] if scope == "common" else [[0], [1]],
        "rotations": np.stack([np.eye(3), rotation]),
        "translations": (
            puw.quantity([[0.0, 0.0, 0.0], [10.0, 20.0, 30.0]], "angstrom")
            if array_translations
            else [
                puw.quantity([0.0, 0.0, 0.0], "nm"),
                puw.quantity([10.0, 20.0, 30.0], "angstrom"),
            ]
        ),
    }


@pytest.mark.parametrize("scope", ["common", "per_operation"])
@pytest.mark.parametrize("array_translations", [False, True])
def test_validated_constructor_round_trips_operations_and_units(
    tmp_path, scope, array_translations
):
    incoming = {"1": _operation(scope, array_translations)}
    rotations = incoming["1"]["rotations"].copy()
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        source = Structures(
            coordinates=puw.quantity(np.zeros((1, 4, 3)), "nm"), bioassembly=incoming
        )
        normalized = source.bioassembly["1"]
        assert np.asarray(normalized["rotations"]).shape == (2, 3, 3)
        assert puw.get_value(normalized["translations"], to_unit="nm").shape == (2, 3)
        # Repeated ordinary construction must be idempotent and leave the caller alone.
        second = Structures(bioassembly=incoming)
        third = Structures(bioassembly=source.bioassembly)
        filename = tmp_path / "assembly.h5msm"
        msm.h5msm.write_layers(filename, structures=source)
        restored = msm.convert(filename, to_form="molsysmt.MolSys").structures
    for item in (source, second, third, restored):
        assembly = item.bioassembly["1"]
        np.testing.assert_array_equal(assembly["rotations"], rotations)
        np.testing.assert_allclose(
            puw.get_value(assembly["translations"], to_unit="nm"),
            [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]],
            rtol=0,
            atol=1e-14,
        )
        chains = assembly["chain_indices"]
        assert np.asarray(chains).shape == ((2,) if scope == "common" else (2, 1))
        np.testing.assert_array_equal(
            chains, [0, 1] if scope == "common" else [[0], [1]]
        )
    np.testing.assert_array_equal(incoming["1"]["rotations"], rotations)
    assert incoming["1"]["chain_indices"] == (
        [0, 1] if scope == "common" else [[0], [1]]
    )
    with h5py.File(filename, "r") as file:
        stored = file["structures/bioassembly/0"]
        assert stored["rotations"].shape == (2, 3, 3)
        assert stored["translations"].attrs["unit"] == "nm"
        assert stored.attrs["chain_scope"] == scope


def test_single_operation_from_original_reproducer_is_serializable(tmp_path):
    source = Structures(
        bioassembly={
            "1": {
                "chain_indices": [[0]],
                "rotations": [np.eye(3)],
                "translations": [puw.quantity([0.0, 0.0, 0.0], "nm")],
            }
        }
    )
    filename = tmp_path / "single.h5msm"
    msm.h5msm.write_layers(filename, structures=source)
    assert msm.h5msm.read(filename).structures.bioassembly["1"]["rotations"].shape == (
        1,
        3,
        3,
    )


def test_empty_translation_matrix_still_requires_length_units():
    with pytest.raises(msm.ArgumentError):
        Structures(
            bioassembly={
                "1": {
                    "chain_indices": [],
                    "rotations": np.empty((0, 3, 3)),
                    "translations": puw.quantity(np.empty((0, 3)), "ps"),
                }
            }
        )


@pytest.mark.parametrize("chains", [[], [[]]])
def test_empty_operations_and_empty_chain_scopes_are_distinct(tmp_path, chains):
    count = len(chains)
    source = Structures(
        bioassembly={
            "1": {
                "chain_indices": chains,
                "rotations": np.repeat(np.eye(3)[None], count, axis=0),
                "translations": puw.quantity(np.zeros((count, 3)), "nm"),
            }
        }
    )
    filename = tmp_path / "empty.h5msm"
    msm.h5msm.write_layers(filename, structures=source)
    restored = msm.h5msm.read(filename).structures.bioassembly["1"]
    assert restored["rotations"].shape == (count, 3, 3)
    assert len(restored["chain_indices"]) == len(chains)


@pytest.mark.parametrize(
    "field,value",
    [
        ("rotations", np.ones((2, 3, 3))),
        ("rotations", np.repeat((-np.eye(3))[None], 2, axis=0)),
        ("rotations", np.full((2, 3, 3), np.nan)),
        ("rotations", np.ones((2, 1, 1, 3, 3))),
        ("rotations", np.ones((2, 3, 3), dtype=complex) * 1j),
        ("translations", [[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]]),
        ("translations", puw.quantity(np.zeros((2, 3)), "ps")),
        ("translations", puw.quantity(np.zeros((1, 3)), "nm")),
        ("translations", puw.quantity(np.ones((2, 1, 3)), "nm")),
        ("translations", puw.quantity(np.full((2, 3), np.inf), "nm")),
        ("chain_indices", [[0]]),
        ("chain_indices", [-1, 0]),
        ("chain_indices", [True, 1]),
        ("chain_indices", [0.5, 1]),
        ("chain_indices", [[0], None]),
    ],
)
def test_invalid_operations_are_rejected_without_mutating_input(field, value):
    incoming = {"1": _operation()}
    incoming["1"][field] = value
    before = deepcopy(incoming)
    with pytest.raises(msm.ArgumentError):
        Structures(bioassembly=incoming)
    # A failed later field must not publish partial rotation/translation normalization.
    assert type(incoming["1"]["chain_indices"]) is type(before["1"]["chain_indices"])
    assert type(incoming["1"]["rotations"]) is type(before["1"]["rotations"])
    assert (
        np.asarray(incoming["1"]["rotations"]).shape
        == np.asarray(before["1"]["rotations"]).shape
    )


@pytest.mark.parametrize("chains", [[0], [0, 1], [[0, 1], [0, 1]]])
def test_validated_dictionary_matches_named_assembly_and_analytical_transform(
    tmp_path, chains
):
    source = build_minimal_molsys(n_structures=1)
    operation = _operation(array_translations=True)
    operation["chain_indices"] = chains
    source.structures = Structures(
        coordinates=source.structures.coordinates, bioassembly={"1": operation}
    )
    direct = msm.build.make_bioassembly(source, bioassembly=operation)
    named = msm.build.make_bioassembly(source, bioassembly="1")
    filename = tmp_path / "built.h5msm"
    msm.h5msm.write(source, filename)
    loaded = msm.convert(filename, to_form="molsysmt.MolSys")
    from_file = msm.build.make_bioassembly(loaded, bioassembly="1")
    xyz = np.arange(12.0).reshape(4, 3)
    if chains == [0]:
        xyz = xyz[:2]
    expected = np.concatenate(
        [xyz, xyz @ operation["rotations"][1].T + [1.0, 2.0, 3.0]]
    )[None]
    for assembled in (direct, named, from_file):
        np.testing.assert_allclose(
            puw.get_value(assembled.structures.get_coordinates(), to_unit="nm"),
            expected,
            rtol=0,
            atol=1e-14,
        )


@pytest.mark.parametrize("chains", [[[0], [1]], [[0], [0, 1]]])
def test_builder_keeps_explicit_limit_on_heterogeneous_chain_scopes(chains):
    operation = _operation()
    operation["chain_indices"] = chains
    with pytest.raises(NotImplementedError):
        msm.build.make_bioassembly(build_minimal_molsys(1), bioassembly=operation)
