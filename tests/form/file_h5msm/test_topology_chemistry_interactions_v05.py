"""Preserve sparse analyses with topology and chemistry but no Structures layer."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Topology
from tests.interactions.test_public_molsys_h5msm_workflow import (
    _analysis,
    _assert_queries,
    _assert_same_observations,
)


def _system():
    topology = Topology(n_atoms=11)
    topology.atoms["atom_id"] = ["same", "same"] + [str(i) for i in range(2, 11)]
    topology.add_bonds([[0, 1], [9, 10]])
    states = topology._chemical_states_domain
    states._states[0].state_id = "prepared"
    states._states[0].provenance_index = 3
    states.append_state()
    states._states[1].state_id = "alternative"
    states._set_reference_index(0)
    analysis = _analysis()
    analysis.software.update({"molsysmt": "original-producer-version"})
    analysis.parameters.update({"criterion": "synthetic", "chemical_state": 0})
    return MolSys._from_partial_domains(
        topology=topology,
        chemical_states=states,
        interactions={"review": analysis},
    )


def _assert_analysis_equal(expected, observed):
    assert observed.method == expected.method
    assert observed.parameters == expected.parameters
    assert observed.software == expected.software
    assert observed.source_id == expected.source_id
    assert observed.source_n_atoms == expected.source_n_atoms
    assert observed.source_n_structures == expected.source_n_structures
    assert observed.evaluation_mode == expected.evaluation_mode
    assert observed.participant_roles == expected.participant_roles
    assert observed.relation_types == expected.relation_types
    for name in (
        "atom_source_indices",
        "structure_source_indices",
        "participant_atoms",
        "participant_atom_offsets",
        "relation_participant_offsets",
    ):
        original = getattr(expected, name)
        actual = getattr(observed, name)
        if original is None:
            assert actual is None
        else:
            np.testing.assert_array_equal(actual, original)
    # Remapping may encode the complete atom axis as None; compare its meaning.
    for name, original in expected.evaluation_scope.items():
        actual = observed.evaluation_scope[name]
        if original is None or isinstance(original, str):
            assert actual == original
        else:
            np.testing.assert_array_equal(actual, original)
    original, actual = expected.to_dict(), observed.to_dict()
    for name in (
        "evaluated_structure_indices",
        "occurrence_indices",
        "structure_indices",
        "relation_indices",
        "evidence",
        "image_offsets",
        "image_vectors",
    ):
        if original[name] is None:
            assert actual[name] is None
        else:
            np.testing.assert_array_equal(actual[name], original[name])
    assert observed.measure_units == expected.measure_units
    assert set(actual["measurements"]) == set(original["measurements"])
    for name, values in original["measurements"].items():
        np.testing.assert_array_equal(actual["measurements"][name], values)
    assert len(observed.execution_records) == len(expected.execution_records)
    for original, actual in zip(expected.execution_records, observed.execution_records):
        assert actual["details"] == original["details"]
        np.testing.assert_array_equal(
            actual["structure_indices"], original["structure_indices"]
        )


def _atom_links(names):
    return [
        {
            "axis": "atom",
            "source": "chemical_states",
            "target": "topology",
            "source_name": None,
            "target_name": None,
            "indices": "identity",
        }
    ] + [
        {
            "axis": "atom",
            "source": "interactions",
            "target": "topology",
            "source_name": name,
            "target_name": None,
            "indices": "identity",
        }
        for name in names
    ]


def _frame_link(source, target, indices="identity"):
    return {
        "axis": "structure",
        "source": "interactions",
        "target": "interactions",
        "source_name": source,
        "target_name": target,
        "indices": indices,
    }


@pytest.mark.parametrize("writer", ["write", "convert"])
@pytest.mark.parametrize("reader", ["read", "convert"])
def test_public_no_structures_roundtrip_preserves_named_analyses(
    tmp_path, writer, reader
):
    source = _system()
    filename = str(tmp_path / "no_structures.h5msm")
    if writer == "write":
        msm.h5msm.write(source, filename)
    else:
        msm.convert(source, to_form="file:h5msm", output_filename=filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert set(file) == {
            "topology",
            "chemical_states",
            "interactions",
            "associations",
        }
        assert "bonds" not in file["topology"]
    restored = (
        msm.h5msm.read(filename)
        if reader == "read"
        else msm.convert(filename, to_form="molsysmt.MolSys")
    )
    assert restored.structures is None
    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert restored.chemical_states.n_chemical_states == 2
    assert restored.chemical_states.reference_chemical_state_index == 0
    assert [state.state_id for state in restored.chemical_states._states] == [
        "prepared",
        "alternative",
    ]
    assert restored.chemical_states._states[0].provenance_index == 3
    assert (
        restored.topology.atoms["atom_id"].tolist()
        == source.topology.atoms["atom_id"].tolist()
    )
    assert msm.get(restored, n_structures=True) == 6
    np.testing.assert_array_equal(
        restored.chemical_states.get_bonds()[["atom1_index", "atom2_index"]],
        [[0, 1], [9, 10]],
    )
    _assert_queries(restored.interactions["review"])
    _assert_same_observations(
        source.interactions["review"], restored.interactions["review"]
    )
    _assert_analysis_equal(
        source.interactions["review"], restored.interactions["review"]
    )
    with pytest.raises(ValueError, match="require structures"):
        restored._get_structure_chemical_state_indices()
    assert source.structures is None


@pytest.mark.parametrize(
    "mode,universe,atoms_b",
    [
        ("incident", list(range(11)), None),
        ("incident", list(range(10)), None),
        ("internal", list(range(10)), None),
        ("between", list(range(10)), [3, 4]),
    ],
)
def test_multiple_analyses_keep_empty_coverage_scope_and_original_versions(
    tmp_path, mode, universe, atoms_b
):
    source = _system()
    empty = msm.Interactions.from_records(
        [],
        n_atoms=11,
        n_structures=6,
        evaluated_structure_indices=[1, 4],
        method="evaluated_empty",
        measure_units={"distance": "angstrom"},
        evaluation_mode=mode,
        evaluation_atom_indices=[0, 1],
        evaluation_atom_indices_b=atoms_b,
        evaluation_universe_indices=universe,
        source_id="independently-declared-provenance",
        atom_source_indices=list(range(11)),
        structure_source_indices=[5, 4, 3, 2, 1, 0],
        software={"engine": "version-used-at-calculation"},
        parameters={"cutoff": {"value": 3.5, "unit": "angstrom"}},
        execution={"execution": "chunked", "execution_chunks": 2},
    )
    source.interactions = {"review": source.interactions["review"], "empty": empty}
    filename = str(tmp_path / "multiple.h5msm")
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        msm.h5msm.write(source, filename)
        restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.structures is None
    assert msm.get(restored, n_structures=True) == 6
    assert set(restored.interactions) == {"review", "empty"}
    for name in source.interactions:
        _assert_analysis_equal(source.interactions[name], restored.interactions[name])
    columns = restored.interactions["empty"].query(structure_indices=[1, 3]).to_dict()
    np.testing.assert_array_equal(columns["evaluated_structure_indices"], [1])
    assert columns["occurrence_indices"].shape == (0,)
    assert columns["occurrence_indices"].dtype == np.int64
    assert columns["measurements"]["distance"].shape == (0,)
    assert restored.interactions["empty"].measure_units == {"distance": "angstrom"}
    links = msm.h5msm.read_layers(filename, layers="associations")["associations"]
    assert len(links) == 4
    assert _frame_link("review", "empty") in links


@pytest.mark.parametrize("n_structures", [0, 6])
def test_named_zero_occurrences_and_zero_structure_axis_are_preserved(
    tmp_path, n_structures
):
    source = _system()
    empty = msm.Interactions.from_records(
        [],
        n_atoms=11,
        n_structures=n_structures,
        evaluated_structure_indices=[] if n_structures == 0 else [1, 3],
        method="empty",
        measure_units={"distance": "nm"},
    )
    source.interactions = {"empty": empty}
    filename = str(tmp_path / "empty.h5msm")
    msm.convert(source, to_form="file:h5msm", output_filename=filename)
    restored = msm.h5msm.read(filename)
    assert restored.structures is None
    assert msm.get(restored, n_structures=True) == n_structures
    _assert_analysis_equal(empty, restored.interactions["empty"])


def test_selected_public_roundtrip_keeps_parallel_observations_and_images(tmp_path):
    source = _system()
    original = source.interactions["review"]
    filename = str(tmp_path / "source.h5msm")
    msm.h5msm.write(source, filename)
    output = str(tmp_path / "subset.h5msm")
    msm.convert(
        filename,
        to_form="file:h5msm",
        output_filename=output,
        selection=[2, 0, 1],
        structure_indices=[4, 1, 0, 4],
    )
    observed = msm.convert(output, to_form="molsysmt.MolSys")
    expected = source.extract(atom_indices=[2, 0, 1], structure_indices=[4, 1, 0, 4])
    assert observed.structures is None
    assert observed.topology.atoms["atom_id"].tolist() == ["same", "same", "2"]
    analysis = observed.interactions["review"]
    assert analysis.n_interactions == 5
    assert analysis.query(structure_indices=[0]).to_dict()[
        "occurrence_indices"
    ].tolist() == [0, 1]
    assert analysis.query(structure_indices=[1]).n_interactions == 0
    np.testing.assert_array_equal(analysis.atom_source_indices, [11, 10, 9])
    np.testing.assert_array_equal(analysis.structure_source_indices, [0, 6, 8, 0])
    _assert_analysis_equal(expected.interactions["review"], analysis)
    assert source.interactions["review"] is original
    assert original.n_interactions == 5
    assert original.n_atoms == 11


def test_invalidated_observations_stay_unevaluated_after_no_coordinate_roundtrip(
    tmp_path,
):
    source = _system()
    original = source.interactions["review"]
    current = original.invalidate_structures([4])
    source.interactions = {"review": current}
    filename = str(tmp_path / "invalidated.h5msm")
    msm.h5msm.write(source, filename)
    restored = msm.h5msm.read(filename)
    assert restored.structures is None
    _assert_analysis_equal(current, restored.interactions["review"])
    assert (
        restored.interactions["review"]
        .query(structure_indices=[4])
        .to_dict()["evaluated_structure_indices"]
        .size
        == 0
    )
    assert original.query(structure_indices=[4]).n_interactions == 2


def test_reader_accepts_a_different_identity_tree_between_analysis_frames(tmp_path):
    source = _system()
    analyses = {name: source.interactions["review"] for name in ["a", "b", "c"]}
    links = _atom_links(analyses) + [_frame_link("a", "b"), _frame_link("b", "c")]
    filename = str(tmp_path / "declared.h5msm")
    msm.h5msm.write_layers(
        filename,
        topology=source.topology,
        chemical_states=source.chemical_states,
        interactions=analyses,
        associations=links,
    )
    observed = msm.h5msm.read(filename)
    assert observed.structures is None
    assert set(observed.interactions) == {"a", "b", "c"}
    for name in analyses:
        _assert_queries(observed.interactions[name])


@pytest.mark.parametrize(
    "defect",
    [
        "missing_atom",
        "reordered_atom",
        "missing_frames",
        "reordered_frames",
        "disconnected_frames",
    ],
)
def test_reader_rejects_undeclared_or_nonidentity_shared_axes(tmp_path, defect):
    source = _system()
    analyses = {name: source.interactions["review"] for name in ["a", "b", "c"]}
    links = _atom_links(analyses) + [_frame_link("a", "b"), _frame_link("b", "c")]
    if defect == "missing_atom":
        links.pop(1)
    elif defect == "reordered_atom":
        links[1]["indices"] = [1, 0] + list(range(2, 11))
    elif defect == "missing_frames":
        links = links[:-2]
    elif defect == "disconnected_frames":
        links.pop()
    else:
        links[-1]["indices"] = [1, 0, 2, 3, 4, 5]
    filename = str(tmp_path / "independent.h5msm")
    msm.h5msm.write_layers(
        filename,
        topology=source.topology,
        chemical_states=source.chemical_states,
        interactions=analyses,
        associations=links,
    )
    assert set(
        msm.h5msm.read_layers(filename, layers="interactions")["interactions"]
    ) == set(analyses)
    with pytest.raises(ValueError, match="declared identity links"):
        msm.h5msm.read(filename)
    with pytest.raises(ValueError, match="declared identity links"):
        msm.convert(filename, to_form="molsysmt.MolSys")


def test_reader_preserves_present_empty_layer_distinction(tmp_path):
    source = _system()
    filename = str(tmp_path / "present_empty.h5msm")
    msm.h5msm.write_layers(
        filename,
        topology=source.topology,
        chemical_states=source.chemical_states,
        interactions={},
        associations=_atom_links([]),
    )
    assert msm.h5msm.read_layers(filename, layers="interactions")["interactions"] == {}
    with pytest.raises(ValueError, match="present-empty interaction layer"):
        msm.h5msm.read(filename)


def test_no_coordinate_writer_still_rejects_nonempty_mechanics_before_creating_file(
    tmp_path,
):
    source = _system()
    source.molecular_mechanics.forcefield = "declared-experimental-forcefield"
    filename = str(tmp_path / "mechanics.h5msm")
    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.h5msm.write(source, filename)
    assert not (tmp_path / "mechanics.h5msm").exists()
