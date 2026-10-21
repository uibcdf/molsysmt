"""Check experimental copy ownership before selecting a native implementation."""

import json

import h5py
import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts import study_native_copy as study
from molsysmt import pyunitwizard as puw


@pytest.fixture(
    params=[(1, False), (3, False), (7, False), (100, False), (1, True), (3, True)]
)
def branch(request):
    source, truth = study._fixture(4, 7)
    return study._Branch(source, *request.param), truth.copy()


def test_forks_isolate_edits_in_both_directions_and_keep_previous_reads(branch):
    source, truth = branch
    clone = source._fork()
    old_read = puw.get_value(clone._get_coordinates(), to_unit="nm")
    assert clone._coordinates.blocks is source._coordinates.blocks
    assert clone._topology is not source._topology

    clone._set_coordinates(puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [3], [1])
    expected = truth.copy()
    expected[3, 1] = [1.0, 2.0, 3.0]
    np.testing.assert_array_equal(
        puw.get_value(clone._get_coordinates(), to_unit="nm"), expected
    )
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )
    np.testing.assert_array_equal(old_read, truth)
    assert source._analyses["pairs"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
        3,
        4,
        5,
    ]
    assert clone._analyses["pairs"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
        4,
        5,
    ]

    grandchild = clone._fork()
    source._set_coordinates(puw.quantity([[[4.0, 5.0, 6.0]]], "nm"), [3], [1])
    np.testing.assert_array_equal(
        puw.get_value(grandchild._get_coordinates(), to_unit="nm"), expected
    )
    np.testing.assert_array_equal(
        puw.get_value(clone._get_coordinates(), to_unit="nm"), expected
    )
    assert grandchild._analyses["pairs"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
        4,
        5,
    ]


def test_queries_preserve_nonconsecutive_repeated_indices_and_empty_axes(branch):
    source, truth = branch
    structures, atoms = [6, 0, 3, 0], [3, 1, 3]
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(structures, atoms), to_unit="nm"),
        truth[structures][:, atoms],
    )
    assert source._get_coordinates([], [0]).shape == (0, 1, 3)
    assert source._get_coordinates([0], []).shape == (1, 0, 3)
    for invalid in ([True], [1.5], [-1], [7]):
        with pytest.raises(ValueError):
            source._get_coordinates(invalid, [0])


def test_owned_input_storage_and_independent_array_metadata(branch):
    source, truth = branch
    for block in source._coordinates.blocks:
        with pytest.raises(ValueError):
            block.flags.writeable = True
    result = puw.get_value(source._get_coordinates(), to_unit="nm")
    result.shape = (7 * 4, 3)
    assert source._get_coordinates().shape == (7, 4, 3)
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )

    incoming = truth.copy()
    coordinates = study._Coordinates(incoming, 3)
    incoming[:] = -10.0
    np.testing.assert_array_equal(coordinates._read(), truth)
    assert incoming.flags.writeable


def test_units_and_chemical_authority_survive_independent_edits(branch):
    source, truth = branch
    clone = source._fork()
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        clone._set_coordinates(
            puw.quantity([[[10.0, 20.0, 30.0]]], "angstrom"), [2], [0]
        )
        assert puw.has_unit(clone._get_coordinates(), "angstrom")
        np.testing.assert_allclose(
            puw.get_value(clone._get_coordinates([2], [0]), to_unit="nm"),
            [[[1.0, 2.0, 3.0]]],
            rtol=0.0,
            atol=1e-14,
        )
    clone._set_formal_charge([1], [1])
    assert source._topology._chemical_states_domain._states[0].atom_attributes[
        "formal_charge"
    ].tolist() == [0, 0, 0, 0]
    assert clone._topology._chemical_states_domain._states[0].atom_attributes[
        "formal_charge"
    ].tolist() == [0, 1, 0, 0]
    assert source._analyses["pairs"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
        3,
        4,
        5,
    ]
    assert clone._analyses["pairs"].evaluated_structure_indices.tolist() == []
    native = clone._to_native()
    assert native.chemical_states is native.topology._chemical_states_domain
    assert native.topology._molsys_owner_ref() is native
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )


def test_fork_metadata_is_independent_without_encoding_or_form_discovery(
    branch, monkeypatch
):
    source, _ = branch

    def forbidden(*args, **kwargs):
        raise AssertionError("Copying must not serialize or discover molecular forms.")

    monkeypatch.setattr(
        "molsysmt.native.interactions_dict._encode_interactions", forbidden
    )
    monkeypatch.setattr(msm, "get_form", forbidden)
    monkeypatch.setattr(msm, "convert", forbidden)
    clone = source._fork()
    clone._analyses["pairs"].parameters["nested"]["cutoff"] = 0.9
    clone._analyses["pairs"].software["fixture"] = "other"
    assert source._analyses["pairs"].parameters == {"nested": {"cutoff": 0.5}}
    assert source._analyses["pairs"].software == {"fixture": "1"}
    assert clone._analyses["pairs"].query(structure_indices=[3, 0]).to_dict()[
        "occurrence_indices"
    ].tolist() == [1, 0]


def test_empty_edits_and_failed_edits_preserve_published_state(branch, monkeypatch):
    source, truth = branch
    coordinates, analyses, topology = (
        source._coordinates,
        source._analyses,
        source._topology,
    )
    assert (
        source._set_coordinates(puw.quantity(np.empty((0, 1, 3)), "nm"), [], [0]) == 0
    )
    source._set_formal_charge([], [])
    assert source._coordinates is coordinates
    assert source._analyses is analyses
    assert source._topology is topology
    for values, structures, atoms in [
        (puw.quantity([[[1.0, 2.0, 3.0]]], "ps"), [0], [0]),
        (puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [0, 1], [0]),
        (puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [7], [0]),
    ]:
        with pytest.raises((ValueError, msm.ArgumentError)):
            source._set_coordinates(values, structures, atoms)
        assert source._coordinates is coordinates
        assert source._analyses is analyses

    def failing(*args, **kwargs):
        raise MemoryError("Simulated validity allocation failure.")

    monkeypatch.setattr(source._analyses["pairs"], "invalidate_structures", failing)
    with pytest.raises(MemoryError):
        source._set_coordinates(puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [0], [0])
    with pytest.raises(MemoryError):
        source._set_formal_charge([0], [1])
    assert source._coordinates is coordinates
    assert source._analyses is analyses
    assert source._topology is topology
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )


def test_edit_detaches_only_touched_blocks_and_preserves_assignment_order(branch):
    source, truth = branch
    clone = source._fork()
    values = np.array([[[1.0, 2.0, 3.0]], [[4.0, 5.0, 6.0]], [[7.0, 8.0, 9.0]]])
    replacement_bytes = clone._set_coordinates(
        puw.quantity(values, "nm"), [6, 0, 6], [2]
    )
    expected = truth.copy()
    expected[0, 2] = [4.0, 5.0, 6.0]
    expected[6, 2] = [7.0, 8.0, 9.0]
    changed_blocks = {0, 6 // source._coordinates.block_size}
    for index, (old, new) in enumerate(
        zip(source._coordinates.blocks, clone._coordinates.blocks)
    ):
        assert (old is new) == (index not in changed_blocks)
    assert replacement_bytes == sum(
        source._coordinates.blocks[index].nbytes for index in changed_blocks
    )
    np.testing.assert_array_equal(
        puw.get_value(clone._get_coordinates(), to_unit="nm"), expected
    )


def test_public_h5msm_roundtrip_preserves_logical_branch_values(branch, tmp_path):
    source, truth = branch
    clone = source._fork()
    clone._set_coordinates(puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [3], [1])
    path = tmp_path / "branch.h5msm"
    with puw.context(standard_units=["angstrom", "ns", "kcal/mol", "K"]):
        msm.convert(clone._to_native(), to_form="file:h5msm", output_filename=str(path))
        with h5py.File(path) as file:
            assert file.attrs["version"] == "0.5"
            assert file["structures/coordinates"].attrs["unit"] == "nm"
        restored = msm.convert(str(path), to_form="molsysmt.MolSys")
        expected = truth.copy()
        expected[3, 1] = [1.0, 2.0, 3.0]
        np.testing.assert_allclose(
            puw.get_value(restored.structures.coordinates, to_unit="nm"),
            expected,
            rtol=1e-6,
            atol=1e-6,
        )
        np.testing.assert_array_equal(
            puw.get_value(restored.structures.time, to_unit="ps"), np.arange(7)
        )
        assert restored.interactions["pairs"].evaluated_structure_indices.tolist() == [
            0,
            1,
            2,
            4,
            5,
        ]
        assert restored.interactions["pairs"].parameters == {"nested": {"cutoff": 0.5}}
        assert restored.interactions["pairs"].software == {"fixture": "1"}
        assert (
            restored.interactions["pairs"].query(structure_indices=[3]).n_interactions
            == 0
        )
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )


def test_coordinate_store_empty_structures_keep_shape():
    store = study._Coordinates(np.empty((0, 4, 3)), 3)
    assert store._read().shape == (0, 4, 3)
    assert store._read([], [0]).shape == (0, 1, 3)


def test_materialized_native_is_editable_and_owns_analysis_metadata(branch):
    source, truth = branch
    native = source._to_native()
    native.interactions["pairs"].parameters["nested"]["cutoff"] = 0.9
    assert source._analyses["pairs"].parameters["nested"]["cutoff"] == 0.5
    msm.set(
        native,
        selection=[0],
        structure_indices=[0],
        coordinates=puw.quantity([[[9.0, 8.0, 7.0]]], "nm"),
    )
    np.testing.assert_array_equal(
        puw.get_value(native.structures.coordinates, to_unit="nm")[0, 0],
        [9.0, 8.0, 7.0],
    )
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )
    assert source._analyses["pairs"].evaluated_structure_indices.tolist() == [
        0,
        1,
        2,
        3,
        4,
        5,
    ]


def test_measurement_keeps_results_and_preparation_scopes_separate():
    events = []

    def prepare():
        events.append("prepare")
        return []

    def operate(subject):
        events.append("operate")
        assert subject == []
        subject.append(1)
        return np.empty(100)

    result = study._measure(prepare, operate, repeats=2)
    assert events == ["prepare", "operate"] * 4
    assert len(result["samples_seconds"]) == 2
    assert result["median_seconds"] >= 0
    assert result["traced_peak_bytes"] >= 800


def test_cli_repeats_public_writes_without_overwriting_external_files(tmp_path):
    output = tmp_path / "measurements.json"
    study.main(
        [
            "--case",
            "4x5",
            "--blocks",
            "1,3",
            "--repeats",
            "2",
            "--io",
            "--output",
            str(output),
        ]
    )
    record = json.loads(output.read_text())
    assert record["units"]["coordinates"] == "nm"
    assert len(record["cases"]) == 5
    for case in record["cases"]:
        assert case["file_bytes"] > 0
        assert (
            len(
                case["operations"]["materialize_and_public_h5msm_write"][
                    "samples_seconds"
                ]
            )
            == 2
        )
        assert case["source_coordinate_bytes"] == 4 * 5 * 3 * 8


def test_shared_base_full_read_fast_path_and_retired_byte_ownership():
    truth = np.arange(7 * 4 * 3, dtype=np.float64).reshape((7, 4, 3))
    hybrid = study._Coordinates(truth, 3, shared_base=True)
    separate = study._Coordinates(truth, 3)
    assert np.shares_memory(hybrid._read(), hybrid.blocks[0])
    assert not np.shares_memory(separate._read(), separate.blocks[0])
    changed = np.zeros((6, 4, 3))
    hybrid_edit, _ = hybrid._replace(changed, np.arange(6), np.arange(4))
    separate_edit, _ = separate._replace(changed, np.arange(6), np.arange(4))
    assert hybrid_edit._base is None
    np.testing.assert_array_equal(hybrid_edit._read()[6], truth[6])
    assert sum(hybrid_edit._byte_owners().values()) == truth.nbytes + changed.nbytes
    assert sum(separate_edit._byte_owners().values()) == truth.nbytes


def test_materialized_branch_preserves_native_distance_workflow(branch):
    source, truth = branch
    clone = source._fork()
    clone._set_coordinates(puw.quantity([[[1.0, 2.0, 3.0]]], "nm"), [3], [1])
    expected = truth.copy()
    expected[3, 1] = [1.0, 2.0, 3.0]
    structures = [3, 0, 3]
    distances = msm.structure.get_distances(
        clone._to_native(),
        selection=[0],
        selection_2=[1],
        structure_indices=structures,
        pbc=False,
    )
    np.testing.assert_allclose(
        puw.get_value(distances, to_unit="nm").reshape(-1),
        np.linalg.norm(expected[structures, 1] - expected[structures, 0], axis=1),
        rtol=1e-12,
        atol=1e-12,
    )


def test_owned_reads_are_mutable_and_do_not_change_either_branch(branch):
    source, truth = branch
    clone = source._fork()
    values = puw.get_value(clone._get_owned_coordinates(), to_unit="nm")
    values[:] = -5.0
    np.testing.assert_array_equal(
        puw.get_value(source._get_coordinates(), to_unit="nm"), truth
    )
    np.testing.assert_array_equal(
        puw.get_value(clone._get_coordinates(), to_unit="nm"), truth
    )
    assert values.flags.owndata


def test_read_campaign_records_owned_and_selected_full_atom_reads(tmp_path):
    output = tmp_path / "reads.json"
    study.main(
        [
            "--case",
            "4x5",
            "--blocks",
            "3",
            "--repeats",
            "1",
            "--reads-only",
            "--output",
            str(output),
        ]
    )
    record = json.loads(output.read_text())
    assert record["campaign"] == "reads_only"
    for case in record["cases"]:
        assert set(case["operations"]) == {
            "selected_read",
            "full_read",
            "owned_full_read",
            "one_structure_read",
            "nonconsecutive_structures_read",
            "full_read_after_edit",
            "block_scan",
        }
        assert case["file_bytes"] is None
