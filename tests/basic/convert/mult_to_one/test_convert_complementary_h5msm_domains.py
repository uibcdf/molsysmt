"""Compose declared complementary domains before selecting their shared axes."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.molecular_system_validation import assess_molecular_system
from molsysmt._private.smonitor import (
    MultipleMolecularSystemsError,
    StructuralInconsistencyError,
)
from molsysmt.native import MolSys, Structures


@pytest.fixture
def split_system(tmp_path):
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        selection=list(range(10)),
        structure_indices=[0, 8, 3],
    )
    source.chemical_states.append_state()
    source._set_structure_chemical_state_indices([0, 1, None])
    source.interactions = {
        "synthetic": msm.Interactions.from_records(
            [
                {
                    "structure_index": 2,
                    "interaction_type": "synthetic_pair",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [4]},
                    ],
                    "measurements": {"distance": 0.4},
                    "evidence": "synthetic",
                }
            ],
            n_atoms=10,
            n_structures=3,
            evaluated_structure_indices=[0, 2],
            method="synthetic",
            measure_units={"distance": "nm"},
            software={"producer": "original-version"},
        )
    }
    chemistry_file = str(tmp_path / "topology_chemistry.h5msm")
    structures_file = str(tmp_path / "structures.h5msm")
    msm.h5msm.write_layers(
        chemistry_file,
        topology=source.topology,
        chemical_states=source.chemical_states,
        associations=[
            {
                "axis": "atom",
                "source": "chemical_states",
                "target": "topology",
                "source_name": None,
                "target_name": None,
                "indices": "identity",
            }
        ],
    )
    msm.h5msm.write_layers(structures_file, structures=source.structures)
    return source, chemistry_file, structures_file


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_real_complementary_files_compose_before_nonconsecutive_selection(
    split_system, native, reverse
):
    source, chemistry_file, structures_file = split_system
    inputs = [chemistry_file, structures_file]
    if native:
        inputs = [msm.h5msm.read(path) for path in inputs]
    if reverse:
        inputs.reverse()
    result = msm.convert(
        inputs,
        selection=[4, 0, 1],
        structure_indices=[2, 0],
    )
    assert msm.get(result, n_atoms=True, n_structures=True) == [3, 2]
    assert result.chemical_states is result.topology._chemical_states_domain
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 1, 4]
        ],
    )
    assert (
        result.topology.atoms["atom_id"].tolist()
        == source.topology.atoms.iloc[[0, 1, 4]].atom_id.tolist()
    )
    assert result.chemical_states.n_chemical_states == 2
    old_to_new = {0: 0, 1: 1, 4: 2}
    for state in range(2):
        original = source.chemical_states.get_bonds(chemical_state=state)
        expected_pairs = [
            [old_to_new[int(a)], old_to_new[int(b)]]
            for a, b in original[["atom1_index", "atom2_index"]].itertuples(
                index=False, name=None
            )
            if int(a) in old_to_new and int(b) in old_to_new
        ]
        np.testing.assert_array_equal(
            result.chemical_states.get_bonds(chemical_state=state)[
                ["atom1_index", "atom2_index"]
            ].to_numpy(),
            np.asarray(expected_pairs, dtype=np.int64).reshape(-1, 2),
        )
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert source._get_structure_chemical_state_indices().tolist()[:2] == [0, 1]


def test_composition_remaps_detached_analyses_and_preserves_empty_frames(
    split_system, tmp_path
):
    source, chemistry_file, structures_file = split_system
    analysis_file = str(tmp_path / "analysis.h5msm")
    msm.h5msm.write_layers(analysis_file, interactions=dict(source.interactions))
    output_file = str(tmp_path / "composed.h5msm")
    msm.convert(
        [analysis_file, structures_file, chemistry_file],
        to_form=output_file,
        selection=[4, 0, 1],
        structure_indices=[2, 0, 2],
    )
    restored = msm.h5msm.read(output_file)
    analysis = restored.interactions["synthetic"]
    columns = analysis.to_dict()
    np.testing.assert_array_equal(columns["structure_indices"], [0, 2])
    np.testing.assert_array_equal(columns["evaluated_structure_indices"], [0, 1, 2])
    np.testing.assert_array_equal(analysis.participant_atoms, [0, 2])
    np.testing.assert_array_equal(analysis.structure_source_indices, [2, 0, 2])
    assert analysis.software == {"producer": "original-version"}
    assert analysis.query(structure_indices=[1]).n_interactions == 0
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm")[[2, 0, 2]][
            :, [0, 1, 4]
        ],
    )


def test_full_axes_and_independent_copy_policy(split_system):
    source, chemistry_file, structures_file = split_system
    inputs = [msm.h5msm.read(chemistry_file), msm.h5msm.read(structures_file)]
    result = msm.convert(inputs)
    assert result.structures is not inputs[1].structures
    assert result.topology is not inputs[0].topology
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm"),
    )
    shared = msm.convert(inputs, copy_if_all=False)
    assert shared.structures is inputs[1].structures
    assert shared.topology is not inputs[0].topology
    assert inputs[0].structures is None and inputs[1].topology is None
    assert inputs[0].topology._molsys_owner_ref() is inputs[0]


def test_explicit_state_association_survives_without_invalidating_analyses(
    split_system,
):
    source, _, _ = split_system
    chemistry_and_structures = MolSys._from_partial_domains(
        chemical_states=source.chemical_states.copy(),
        structures=source.structures.copy(),
    )
    chemistry_and_structures._set_structure_chemical_state_indices([0, 1, None])
    chemistry_and_structures.interactions = dict(source.interactions)
    topology = source.topology.copy()
    topology._clear_chemical_states()
    identity = MolSys._from_partial_domains(topology=topology)
    result = msm.convert([identity, chemistry_and_structures], structure_indices=[2, 0])
    state_map = result._get_structure_chemical_state_indices()
    assert pd.isna(state_map[0]) and state_map[1] == 0
    assert result.interactions["synthetic"].n_interactions == 1
    np.testing.assert_array_equal(
        result.interactions["synthetic"].evaluated_structure_indices, [0, 1]
    )
    assert identity.chemical_states is None
    assert identity.topology._chemical_states_domain.n_chemical_states == 0


@pytest.mark.parametrize(
    "defect", ["atoms", "frames", "duplicate_structures", "duplicate_analysis"]
)
def test_incompatible_domains_fail_before_selection_can_hide_them(split_system, defect):
    source, chemistry_file, structures_file = split_system
    identity = msm.h5msm.read(chemistry_file)
    geometry = msm.h5msm.read(structures_file)
    if defect == "atoms":
        geometry = geometry.extract(atom_indices=list(range(9)))
    inputs = [identity, geometry]
    if defect in {"frames", "duplicate_analysis"}:
        analysis = source.interactions["synthetic"]
        if defect == "frames":
            analysis = analysis.remap(structure_indices=[0, 1])
        detached = MolSys._from_partial_domains(interactions={"synthetic": analysis})
        inputs.append(detached)
        if defect == "duplicate_analysis":
            inputs.append(detached)
    elif defect == "duplicate_structures":
        inputs.append(geometry)
    with pytest.raises(StructuralInconsistencyError):
        msm.convert(inputs, selection=[0], structure_indices=[0])
    assert identity.structures is None
    assert geometry.get_n_atoms() == (9 if defect == "atoms" else 10)


def test_complete_files_remain_distinct_systems(split_system, tmp_path):
    source, _, _ = split_system
    paths = [str(tmp_path / f"complete_{i}.h5msm") for i in range(2)]
    for path in paths:
        msm.h5msm.write(source, path)
    with pytest.raises(MultipleMolecularSystemsError):
        msm.convert(paths)


def test_frame_only_domain_has_no_invented_atom_axis(split_system):
    _, chemistry_file, _ = split_system
    frames = Structures()
    frames.append(time=puw.quantity([0, 100, 200], "fs"))
    geometry = MolSys._from_partial_domains(structures=frames)
    result = msm.convert(
        [msm.h5msm.read(chemistry_file), geometry], structure_indices=[2, 0]
    )
    assert result.structures.coordinates is None
    assert result.get_n_atoms() == 10
    np.testing.assert_allclose(
        puw.get_value(result.structures.time, to_unit="ps"), [0.2, 0]
    )


def test_classification_reads_h5msm_metadata_without_materializing_arrays(
    split_system, monkeypatch
):
    _, chemistry_file, structures_file = split_system

    def forbidden(*args, **kwargs):
        raise AssertionError("Classification must inspect metadata, not load domains.")

    monkeypatch.setattr(msm.basic, "get", forbidden)
    monkeypatch.setattr(msm.h5msm, "read", forbidden)
    assessment = assess_molecular_system([chemistry_file, structures_file])
    assert assessment.is_valid_single_system
    assert set(assessment.atom_counts) == {10}


def test_nondefault_units_and_topology_selection_are_applied_after_composition(
    split_system,
):
    source, chemistry_file, structures_file = split_system
    with puw.context(standard_units=["angstrom", "fs"]):
        result = msm.convert(
            [structures_file, chemistry_file],
            selection="atom_index in [0, 1, 4]",
            structure_indices=[2, 0],
        )
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm")[[2, 0]][
            :, [0, 1, 4]
        ],
    )


def test_partial_composition_rejects_mechanics_without_silent_loss(split_system):
    _, chemistry_file, structures_file = split_system
    identity = msm.h5msm.read(chemistry_file)
    geometry = msm.h5msm.read(structures_file)
    identity.molecular_mechanics.forcefield = "declared-model"
    with pytest.raises(StructuralInconsistencyError, match="molecular mechanics"):
        msm.convert([identity, geometry])
    assert identity.molecular_mechanics.forcefield == "declared-model"
