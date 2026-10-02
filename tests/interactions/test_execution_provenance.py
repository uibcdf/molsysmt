"""Protect partial detector recalculation and frame-scoped execution evidence."""

import pickle

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.interactions._hdf5_query import query_named_interactions_file

from .cation_pi.test_get_cation_pi_interactions import _calculate as cation_pi
from .cation_pi.test_get_cation_pi_interactions import _system as cation_system
from .halogen_bonds.test_get_halogen_bonds import _system as halogen_system
from .hbonds.test_attributed_hbonds import METHODS
from .hbonds.test_attributed_hbonds import _calculate as hbonds
from .hbonds.test_attributed_hbonds import _system as hbond_system
from .hydrophobic.test_get_hydrophobic_interactions import _system as hydrophobic_system
from .ionic.test_get_ionic_interactions import _ions
from .metal_coordination.test_get_metal_coordination import _system as metal_system
from .pi_pi.test_get_pi_pi_interactions import _calculate as pi_pi
from .pi_pi.test_get_pi_pi_interactions import _ensemble
from .test_frame_replacement import record, result
from .test_software_provenance import _system as legacy_system
from .water_bridges.test_get_water_bridges import _system as water_system
from .water_bridges.test_two_water_bridges import _chain


def _records(analysis):
    return [(record["structure_indices"].tolist(), record["details"])
            for record in analysis.execution_records]


@pytest.mark.parametrize("family", ["ionic", "pi_pi", "cation_pi", "hydrophobic",
                                  "halogen", "metal", "water", "two_water", *METHODS])
def test_real_detectors_replace_empty_and_observed_frames_across_execution_policies(family, tmp_path):
    if family == "ionic":
        molsys = _ions()
        def calculate(source, **kwargs):
            return msm.interactions.ionic.get_ionic_interactions(source, ".4 nm", **kwargs)
    elif family == "pi_pi":
        molsys, calculate = _ensemble(), pi_pi
    elif family == "cation_pi":
        molsys, calculate = cation_system(points=((0, 0, .35), (0, 0, 2), (0, 0, .35))), cation_pi
    elif family == "hydrophobic":
        molsys, calculate = hydrophobic_system(), msm.interactions.hydrophobic.get_hydrophobic_interactions
    elif family == "halogen":
        molsys, calculate = halogen_system(), msm.interactions.halogen_bonds.get_halogen_bonds
    elif family == "metal":
        molsys, calculate = metal_system(), msm.interactions.metal_coordination.get_metal_coordination
    elif family == "water":
        molsys, calculate = water_system()[0], msm.interactions.water_bridges.get_water_bridges
    elif family == "two_water":
        molsys = _chain()[0]
        def calculate(source, **kwargs):
            return msm.interactions.water_bridges.get_water_bridges(source, order=2, **kwargs)
    else:
        molsys = hbond_system()
        def calculate(source, **kwargs):
            return hbonds(source, family, **kwargs)
    with msm.configure.context(chunk_size=1):
        original = calculate(molsys, pbc=False, heavy_mode="force")
    previous = original.query(structure_indices=[1, 2])
    fresh = calculate(molsys, pbc=False, structure_indices=[2, 1], heavy_mode="off")
    assert original.parameters == fresh.parameters
    assert "execution" not in original.parameters and "execution_chunks" not in original.parameters
    assert _records(original)[0][1]["execution"] == "chunked"
    assert _records(fresh)[0][1]["execution"] == "eager"
    edited = original.invalidate_structures([1, 2]).replace_structures(fresh)
    assert [frames for frames, _ in _records(edited)] == [[0], [1, 2]]
    assert edited.query(structure_indices=1).n_interactions == original.query(structure_indices=1).n_interactions
    assert _records(edited.query(structure_indices=[2, 1, 2])) == _records(fresh)
    assert _records(previous)[0][1]["execution"] == "chunked"
    for frame in range(3):
        before, after = original.query(structure_indices=frame).to_dict(), edited.query(structure_indices=frame).to_dict()
        np.testing.assert_array_equal(after["evidence"], before["evidence"])
        for name in before["measurements"]:
            np.testing.assert_allclose(after["measurements"][name], before["measurements"][name])
    molsys.interactions = {family: edited}
    path = str(tmp_path / "partial.h5msm")
    msm.convert(molsys, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions[family]
    assert _records(restored) == _records(edited)
    assert _records(restored.query(structure_indices=1)) == [([1], _records(fresh)[0][1])]
    projection = query_named_interactions_file(path, family, [2, 1])
    assert [(entry["structure_indices"].tolist(), entry["details"])
            for entry in projection["execution_records"]] == _records(fresh)

    coordinates = msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm")
    msm.set(molsys, structure_indices=[1], coordinates=msm.pyunitwizard.quantity(coordinates[[0]], "nm"))
    retained = molsys.interactions[family]
    assert retained.query(structure_indices=1).to_dict()["evaluated_structure_indices"].size == 0
    recalculated = calculate(molsys, pbc=False, structure_indices=[1], heavy_mode="off")
    updated = retained.replace_structures(recalculated)
    assert updated.query(structure_indices=1).n_interactions == original.query(structure_indices=0).n_interactions > 0
    assert _records(updated.query(structure_indices=1)) == _records(recalculated)


@pytest.mark.parametrize("detector", [msm.interactions.hbonds.get_buch_hbonds,
                                     msm.interactions.hbonds.get_luzard_chandler_hbonds,
                                     msm.interactions.disulfides.get_disulfide_candidates])
def test_legacy_detectors_support_partial_recalculation_without_inventing_execution_details(detector):
    molsys = legacy_system()
    original = detector(molsys, pbc=False, output_type="molsysmt.Interactions")
    fresh = detector(molsys, pbc=False, structure_indices=[1], output_type="molsysmt.Interactions")
    edited = original.replace_structures(fresh)
    assert _records(edited) == [([0], {}), ([1], {})]
    assert edited.query(structure_indices=1).n_interactions == 0


def test_execution_records_follow_edits_repeated_remapping_and_interchange(tmp_path):
    original = result([record(0, .1), record(2, .2)], [0, 1, 2], execution={"execution": "chunked", "execution_chunks": 3})
    fresh = result([record(2, .3)], [1, 2], execution={"execution": "eager", "execution_chunks": 1})
    edited = original.replace_structures(fresh)
    assert _records(edited) == [([0], original.execution_records[0]["details"]),
                                ([1, 2], fresh.execution_records[0]["details"])]
    exposed = edited.execution_records
    exposed[0]["structure_indices"][0] = 4
    exposed[0]["details"]["execution"] = "changed"
    assert _records(edited)[0] == ([0], {"execution": "chunked", "execution_chunks": 3})
    remapped = edited.remap(structure_indices=[2, 0, 1, 2])
    assert [frames for frames, _ in _records(remapped)] == [[1], [0, 2, 3]]
    invalid = edited.invalidate_structures([0])
    assert _records(invalid) == [([1, 2], fresh.execution_records[0]["details"])]
    payload = msm.convert(invalid, to_form="molsysmt.InteractionsDict")
    assert payload.data["version"] == 2
    assert _records(msm.convert(payload, to_form="molsysmt.Interactions")) == _records(invalid)
    assert _records(pickle.loads(pickle.dumps(invalid))) == _records(invalid)
    selected = invalid.query(structure_indices=[1])
    assert _records(pickle.loads(pickle.dumps(selected))) == _records(selected)
    path = tmp_path / "result.h5i"
    invalid.save(path)
    assert _records(msm.Interactions.load(path)) == _records(invalid)
    empty = edited.replace_structures(result([], [0, 1, 2], execution={"execution_chunks": 0}))
    assert empty.n_interactions == 0 and _records(empty) == [([0, 1, 2], {"execution_chunks": 0})]


@pytest.mark.parametrize("frames", [[0, 0, 1], [0], [0, 1, 4]])
def test_execution_records_reject_duplicates_gaps_and_unevaluated_frames(frames):
    with pytest.raises(ValueError):
        result([], [0, 1], execution_records=[{"structure_indices": frames, "details": {}}])


def test_version_one_readers_migrate_only_known_execution_keys(tmp_path):
    old = result([record(0, .1)], [0, 1], parameters={"cutoff": .5})
    payload = msm.convert(old, to_form="molsysmt.InteractionsDict")
    payload.data["version"] = 1
    del payload.data["execution_records"]
    payload.data["parameters"].update(execution="chunked", execution_chunks=2, memory_policy="old")
    payload.data["parameters"]["hbond_parameters"] = {"distance_threshold": .3, "execution_chunks": 4}
    restored = msm.convert(payload, to_form="molsysmt.Interactions")
    assert restored.parameters == {"cutoff": .5, "hbond_parameters": {"distance_threshold": .3}}
    assert _records(restored) == [([0, 1], {"execution": "chunked", "execution_chunks": 2,
                                           "memory_policy": "old", "hbond_execution": {"execution_chunks": 4}})]
    path = tmp_path / "legacy.h5i"
    old.save(path)
    with h5py.File(path, "a") as file:
        import json

        file.attrs["schema_version"] = 1
        del file["execution"]
        metadata = json.loads(file.attrs["metadata"])
        metadata["parameters"] = payload.data["parameters"]
        file.attrs["metadata"] = json.dumps(metadata)
    assert _records(msm.Interactions.load(path)) == _records(restored)


def test_current_codec_rejects_missing_and_corrupt_execution_partition(tmp_path):
    analysis = result([], [0, 1], execution={"execution_chunks": 0})
    payload = msm.convert(analysis, to_form="molsysmt.InteractionsDict")
    payload.data["execution_records"][0]["structure_indices"] = np.array([0])
    with pytest.raises(ValueError, match="partition"):
        msm.convert(payload, to_form="molsysmt.Interactions")
    payload.data["execution_records"] = None
    with pytest.raises(ValueError, match="require execution_records"):
        msm.convert(payload, to_form="molsysmt.Interactions")
    path = tmp_path / "corrupt.h5i"
    analysis.save(path)
    with h5py.File(path, "a") as file:
        file["execution/structure_offsets"][1] = 1
    with pytest.raises(ValueError, match="offsets"):
        msm.Interactions.load(path)
