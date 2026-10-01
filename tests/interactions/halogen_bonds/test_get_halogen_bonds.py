"""Check four-role directional geometry, sparse scopes and persistence."""

from copy import deepcopy

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MemoryBudgetExceededError


def _system(n_frames=3):
    molsys = msm.convert(Chem.MolFromSmiles("CCl.C=O"), to_form="molsysmt.MolSys")
    xyz = np.array([[-.15, 0, 0], [0, 0, 0], [.36, .12 * np.sqrt(.75), 0], [.30, 0, 0]])
    frames = np.repeat(xyz[None], n_frames, axis=0)
    if n_frames == 3:
        frames[1, [2, 3]] += [0, .5, 0]
    molsys.structures.append(coordinates=puw.quantity(frames, "nm"))
    molsys.structures.structure_id = np.array([f"external-{100-i}" for i in range(n_frames)])
    return molsys


@pytest.mark.parametrize(("mode", "a", "b", "count"), [
    ("internal", [0, 1, 2, 3], None, 2), ("internal", [1, 3], None, 0),
    ("incident", [0], None, 2), ("incident", [1], None, 2),
    ("incident", [2], None, 2), ("incident", [3], None, 2),
    ("between", [0, 1], [2, 3], 2), ("between", [1], [0, 2, 3], 2),
])
def test_all_four_roles_define_scope_and_nonconsecutive_indices(mode, a, b, count):
    molsys = _system()
    result = msm.interactions.halogen_bonds.get_halogen_bonds(
        molsys, selection=a, selection_2=b, selection_mode=mode, structure_indices=[2, 0, 2], pbc=False)
    assert result.n_interactions == count
    assert result.evaluated_structure_indices.tolist() == [0, 2]
    if count:
        assert result.participant_atoms.tolist() == [0, 1, 3, 2]
        assert result.participant_roles == ("donor", "halogen", "acceptor", "acceptor_reference")
        assert result.occurrence_structures.tolist() == [0, 2]
        np.testing.assert_allclose(result.measurements["distance"], .3)
        np.testing.assert_allclose(result.measurements["donor_angle"], np.pi)
        np.testing.assert_allclose(result.measurements["acceptor_angle"], 2 * np.pi / 3)
        assert result.query(atom_indices=[2], mode="incident").n_interactions == 2
        assert result.query(atom_indices=[1, 3], mode="internal").n_interactions == 0
        assert result.query(atom_indices=[1, 3], mode="cross").n_interactions == 2
        assert result.between([1], [3], exclusive=True).n_interactions == 0
    assert not molsys.interactions


def test_units_empty_frames_and_named_typed_persistence_keep_original_attribution(tmp_path):
    molsys = _system()
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = msm.interactions.halogen_bonds.get_halogen_bonds(
            molsys, distance_threshold="3.5 angstroms",
            donor_angle_range=puw.quantity([130, 180], "degrees"),
            acceptor_angle_range=puw.quantity([80, 140], "degrees"), pbc=False)
    assert result.n_interactions == 2
    assert result.query(structure_indices=[1]).to_dict()["occurrence_indices"].shape == (0,)
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]
    assert result.measure_units["distance"] == "nm"
    assert result.measure_units["acceptor_angle"] == "radians"
    items = result.parameters["attribution"]["items"]
    assert {item["doi"] for item in items if "doi" in item} >= {
        "10.1073/pnas.0407607101", "10.1186/s13321-021-00548-6"}
    assert not any(item["id"].startswith("software:prolif:") for item in items)
    molsys.interactions = {"halogens": result}
    path = str(tmp_path / "named.h5msm")
    msm.convert(molsys, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions["halogens"]
    assert restored.parameters == result.parameters
    assert restored.software == result.software
    np.testing.assert_array_equal(restored.to_dict()["occurrence_indices"], result.to_dict()["occurrence_indices"])
    typed = msm.interactions.halogen_bonds.get_halogen_bonds(molsys, pbc=False, output_type="molsysmt.InteractionsDict")
    np.testing.assert_array_equal(msm.convert(typed, to_form="molsysmt.Interactions").participant_atoms, result.participant_atoms)


@pytest.mark.parametrize("box", [np.eye(3), np.array([[1., .1, .05], [0, 1., .1], [0, 0, 1.]]),
                               np.array([[0, 1., 0], [-1., 0, 0], [0, 0, 1.]])])
def test_chain_images_reconstruct_both_angles_and_every_distance(box):
    molsys = _system(n_frames=1)
    xyz = puw.get_value(molsys.structures.coordinates, to_unit="nm").copy()
    lattice = np.array([[1, 0, 0], [0, 0, 0], [-1, 1, 0], [0, 1, 0]])
    xyz[0] += lattice @ box
    molsys.structures.coordinates = puw.quantity(xyz, "nm")
    molsys.structures.box = puw.quantity(box[None], "nm")
    result = msm.interactions.halogen_bonds.get_halogen_bonds(molsys)
    assert result.n_interactions == 1
    observed = xyz[0, result.participant_atoms] + result.image_vectors @ box
    np.testing.assert_array_equal(result.image_vectors, (lattice[0] - lattice)[result.participant_atoms])
    dx, xa, ar = (observed[1] - observed[0], observed[2] - observed[1], observed[3] - observed[2])
    np.testing.assert_allclose(np.linalg.norm(xa), result.measurements["distance"][0])
    np.testing.assert_allclose(np.arccos(np.dot(-dx, xa) / np.linalg.norm(dx) / np.linalg.norm(xa)), result.measurements["donor_angle"][0])
    np.testing.assert_allclose(np.arccos(np.dot(-xa, ar) / np.linalg.norm(xa) / np.linalg.norm(ar)), result.measurements["acceptor_angle"][0])


@pytest.mark.parametrize("form", ["native", "rdkit", "composite", "h5msm"])
def test_geometry_is_form_agnostic(form, tmp_path):
    source = _system()
    if form == "rdkit":
        source = msm.convert(source, to_form="rdkit.Mol")
    elif form == "composite":
        source = [source.topology, source.structures]
    elif form == "h5msm":
        path = str(tmp_path / "input.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.halogen_bonds.get_halogen_bonds(source, pbc=False)
    assert result.n_structures == 3
    assert result.n_interactions == 2
    np.testing.assert_allclose(result.measurements["distance"], .3)


def test_distinct_reference_neighbors_do_not_collapse_to_one_pair():
    source = msm.convert(Chem.MolFromSmiles("CCl.COC"), to_form="molsysmt.MolSys")
    xyz = [[[-.15, 0, 0], [0, 0, 0], [.36, .1, 0], [.30, 0, 0], [.36, -.1, 0]]]
    source.structures.append(coordinates=puw.quantity(xyz, "nm"))
    result = msm.interactions.halogen_bonds.get_halogen_bonds(source, pbc=False)
    assert result.n_interactions == 2
    assert result.occurrence_relations.tolist() == [0, 1]
    assert result.relation(0)["participants"][-1]["atom_indices"].tolist() == [2]
    assert result.relation(1)["participants"][-1]["atom_indices"].tolist() == [4]


@pytest.mark.parametrize("options", [
    {"distance_threshold": .35}, {"distance_threshold": "0 nm"}, {"distance_threshold": "2 ps"},
    {"donor_angle_range": [130, 180]}, {"acceptor_angle_range": puw.quantity([140, 80], "degrees")},
    {"acceptor_angle_range": puw.quantity([0, 4], "radians")},
    {"donor_angle_range": puw.quantity([130], "degrees")},
    {"donor_angle_range": puw.quantity([130, np.nan], "degrees")},
    {"profile": "unknown"}, {"method": "prolif"}, {"output_type": "numpy.ndarray"},
    {"selection_mode": "between"}, {"selection_2": [2]}, {"structure_indices": [3]},
    {"selection_mode": "between", "selection": [0, 1], "selection_2": [1, 2]},
])
def test_invalid_scientific_parameters_fail(options):
    with pytest.raises(msm.ArgumentError):
        msm.interactions.halogen_bonds.get_halogen_bonds(_system(), pbc=False, **options)


def test_undefined_angles_and_invalid_boxes_are_distinguished():
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, 0] = xyz[0, 1]
    source.structures.coordinates = puw.quantity(xyz, "nm")
    empty = msm.interactions.halogen_bonds.get_halogen_bonds(source, pbc=False)
    assert empty.n_interactions == 0 and empty.evaluated_structure_indices.tolist() == [0]
    source.structures.box = puw.quantity(np.zeros((1, 3, 3)), "nm")
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.interactions.halogen_bonds.get_halogen_bonds(source)


def test_chunked_h5msm_projects_selected_frames_without_loading_saved_analyses(monkeypatch, tmp_path):
    source = _system(n_frames=100)
    path = str(tmp_path / "trajectory.h5msm")
    msm.convert(source, to_form=path)
    monkeypatch.setattr(msm.configure, "chunk_size", 7)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2_000_000)
    from molsysmt.form import _h5msm05_modular

    monkeypatch.setattr(_h5msm05_modular, "read_molsys_file", lambda *args, **kwargs: pytest.fail("Full file loaded."))
    for item in (source, path):
        result = msm.interactions.halogen_bonds.get_halogen_bonds(item, pbc=False, heavy_mode="force")
        assert result.n_interactions == 100 and result.parameters["execution_chunks"] == 15
    selected = msm.interactions.halogen_bonds.get_halogen_bonds(path, pbc=False, heavy_mode="force", structure_indices=[98, 1, 50, 1])
    assert selected.occurrence_structures.tolist() == [1, 50, 98]
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.interactions.halogen_bonds.get_halogen_bonds(source, pbc=False)


def test_runtime_ackredit_distinguishes_adapted_source_and_reference_software():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("halogen-producer"):
        result = msm.interactions.halogen_bonds.get_halogen_bonds(_system(), pbc=False)
        used = ackredit.get_used_items()
        assert "doi:10.1073/pnas.0407607101" in used
        assert "doi:10.1186/s13321-021-00548-6" in used
    original = deepcopy(result.parameters["attribution"])
    with ackredit.session("halogen-reader"):
        typed = msm.convert(result, to_form="molsysmt.InteractionsDict")
        restored = msm.convert(typed, to_form="molsysmt.Interactions")
        assert restored.parameters["attribution"] == original
        assert ackredit.get_used_items() == {}
