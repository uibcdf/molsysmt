"""Protect canonical hydrophobic pair identity, images, sparse scopes and storage."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import MemoryBudgetExceededError


def _system(n_frames=3, smiles="CCC.CCC"):
    molsys = msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")
    xyz = np.array(
        [
            [0, 0, 0],
            [0.15, 0, 0],
            [0.30, 0, 0],
            [0, 0.30, 0],
            [0.15, 0.30, 0],
            [0.30, 0.30, 0],
        ]
    )
    coordinates = np.repeat(xyz[None], n_frames, axis=0)
    if n_frames == 3:
        coordinates[1, 3:] += [0, 1.0, 0]
    molsys.structures.append(coordinates=puw.quantity(coordinates, "nm"))
    molsys.structures.structure_id = np.array(
        [f"frame-label-{100 - i}" for i in range(n_frames)]
    )
    return molsys


@pytest.mark.parametrize(
    ("mode", "first", "second", "count"),
    [
        ("internal", [1, 4], None, 2),
        ("internal", [4], None, 0),
        ("incident", [1], None, 2),
        ("incident", [4], None, 2),
        ("incident", [0], None, 0),
        ("between", [4], [1], 2),
        ("between", [0, 1, 2], [3, 4, 5], 2),
    ],
)
def test_canonical_pair_queries_and_nonconsecutive_structure_indices(
    mode, first, second, count
):
    source = _system()
    result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source,
        selection=first,
        selection_2=second,
        selection_mode=mode,
        structure_indices=[2, 0, 2],
        pbc=False,
    )
    assert result.n_interactions == count
    assert result.evaluated_structure_indices.tolist() == [0, 2]
    assert not source.interactions
    if count:
        assert result.participant_atoms.tolist() == [1, 4]
        assert result.participant_roles == ("hydrophobic_1", "hydrophobic_2")
        assert result.occurrence_structures.tolist() == [0, 2]
        np.testing.assert_allclose(result.measurements["distance"], 0.30)
        assert (
            result.query(atom_indices=[1], mode="involving_selection").n_interactions
            == 2
        )
        assert (
            result.query(atom_indices=[1], mode="within_selection").n_interactions == 0
        )
        assert (
            result.query(
                atom_indices=[1], mode="across_selection_boundary"
            ).n_interactions
            == 2
        )
        assert result.between_selections([4], [1], exclusive=True).n_interactions == 2


def test_pair_identity_deduplicates_internal_and_cross_scopes_without_covalent_filter():
    source = _system(n_frames=1, smiles="c1ccccc1")
    result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, pbc=False
    )
    pairs = [
        tuple(result.relation(i)["participants"][j]["atom_indices"][0] for j in (0, 1))
        for i in range(len(result.relation_types))
    ]
    assert len(pairs) == 15 and all(a < b for a, b in pairs) and len(set(pairs)) == 15
    assert (0, 1) in pairs  # A direct covalent neighbor is not silently filtered.
    incident = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, selection=[0, 1], selection_mode="incident", pbc=False
    )
    assert incident.n_interactions == 9
    query = result.query(atom_indices=[0, 1], mode="involving_selection").to_dict()
    np.testing.assert_allclose(
        query["measurements"]["distance"], incident.measurements["distance"]
    )
    source.structures.coordinates = puw.quantity(np.zeros((1, 6, 3)), "nm")
    coincident = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, pbc=False
    )
    assert coincident.n_interactions == 15 and np.all(
        coincident.measurements["distance"] == 0
    )


@pytest.mark.parametrize(
    "box",
    [
        np.eye(3),
        np.array([[1.0, 0.1, 0], [0, 1.0, 0.1], [0, 0, 1.0]]),
        np.array([[0, 1.0, 0], [-1.0, 0, 0], [0, 0, 1.0]]),
    ],
)
def test_periodic_images_reconstruct_geometry_and_survive_scope_reversal(box):
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    lattice = np.zeros((6, 3), dtype=int)
    lattice[4] = [1, -1, 0]
    xyz[0] += lattice @ box
    source.structures.coordinates = puw.quantity(xyz, "nm")
    source.structures.box = puw.quantity(box[None], "nm")
    original = msm.interactions.hydrophobic.get_hydrophobic_interactions(source)
    for mode, first, second in [("incident", [4], None), ("between", [4], [1])]:
        result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
            source, selection=first, selection_2=second, selection_mode=mode
        )
        np.testing.assert_array_equal(result.image_vectors, original.image_vectors)
        observed = xyz[0, result.participant_atoms] + result.image_vectors @ box
        np.testing.assert_allclose(
            np.linalg.norm(observed[1] - observed[0]),
            result.measurements["distance"][0],
        )
    np.testing.assert_array_equal(original.image_vectors, [[0, 0, 0], [-1, 1, 0]])


def test_mic_tie_image_is_independent_of_selection_orientation():
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, 4] = xyz[0, 1] + [0.5, 0, 0]
    source.structures.coordinates = puw.quantity(xyz, "nm")
    source.structures.box = puw.quantity(np.eye(3)[None], "nm")
    results = [
        msm.interactions.hydrophobic.get_hydrophobic_interactions(
            source,
            selection=[a],
            selection_2=[b],
            selection_mode="between",
            distance_threshold="0.51 nm",
        )
        for a, b in [(1, 4), (4, 1)]
    ]
    assert results[0].n_interactions == 1
    np.testing.assert_array_equal(results[0].image_vectors, results[1].image_vectors)


@pytest.mark.parametrize("form", ["native", "rdkit", "composite", "h5msm"])
def test_scientific_geometry_is_form_agnostic(form, tmp_path):
    source = _system()
    if form == "rdkit":
        source = msm.convert(source, to_form="rdkit.Mol")
    elif form == "composite":
        source = [source.topology, source.structures]
    elif form == "h5msm":
        path = str(tmp_path / "source.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, pbc=False
    )
    assert result.n_interactions == 2 and result.n_structures == 3
    assert result.evaluated_structure_indices.tolist() == [0, 1, 2]


def test_units_empty_shapes_named_and_typed_h5msm_preserve_original_provenance(
    tmp_path,
):
    source = _system()
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
            source, pbc=False, distance_threshold="4.5 angstroms"
        )
    assert result.measure_units == {"distance": "nm"}
    empty = result.query(structure_indices=[1]).to_dict()
    assert (
        empty["occurrence_indices"].shape == (0,)
        and empty["occurrence_indices"].dtype == np.int64
    )
    items = result.parameters["attribution"]["items"]
    assert any(item.get("doi") == "10.1186/s13321-021-00548-6" for item in items)
    assert not any(item["id"].startswith("software:prolif:") for item in items)
    source.interactions = {"hydrophobic": result}
    path = str(tmp_path / "named.h5msm")
    msm.convert(source, to_form=path)
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    restored = loaded.interactions["hydrophobic"]
    assert (
        restored.parameters == result.parameters
        and restored.software == result.software
    )
    np.testing.assert_array_equal(
        restored.to_dict()["occurrence_indices"], result.to_dict()["occurrence_indices"]
    )
    typed = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        source, pbc=False, output_type="molsysmt.InteractionsDict"
    )
    assert msm.convert(typed, to_form="molsysmt.Interactions").n_interactions == 2
    subset = msm.extract(loaded, selection=[4, 1], structure_indices=[2, 0, 1])
    assert subset.interactions["hydrophobic"].n_interactions == 2
    assert (
        msm.extract(loaded, selection=[0, 1, 2])
        .interactions["hydrophobic"]
        .n_interactions
        == 0
    )


@pytest.mark.parametrize(
    "options",
    [
        {"distance_threshold": 0.45},
        {"distance_threshold": "-1 nm"},
        {"distance_threshold": "1 ps"},
        {"distance_threshold": puw.quantity([0.4, 0.5], "nm")},
        {"distance_threshold": "nan nm"},
        {"method": "prolif"},
        {"profile": "carbon_fluorine"},
        {"output_type": "numpy.ndarray"},
        {"selection_mode": "between"},
        {"selection_2": [4]},
        {"structure_indices": [3]},
        {"selection_mode": "between", "selection": [1, 4], "selection_2": [4]},
    ],
)
def test_invalid_parameters_fail(options):
    with pytest.raises(msm.ArgumentError):
        msm.interactions.hydrophobic.get_hydrophobic_interactions(
            _system(), pbc=False, **options
        )


def test_invalid_coordinates_and_box_fail():
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, 1, 0] = np.nan
    source.structures.coordinates = puw.quantity(xyz, "nm")
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.interactions.hydrophobic.get_hydrophobic_interactions(source, pbc=False)
    source = _system(n_frames=1)
    source.structures.box = puw.quantity(np.zeros((1, 3, 3)), "nm")
    with pytest.raises(msm.StructuralInconsistencyError):
        msm.interactions.hydrophobic.get_hydrophobic_interactions(source)


def test_chunked_file_projection_does_not_load_analyses_or_full_coordinates(
    monkeypatch, tmp_path
):
    source = _system(n_frames=100)
    path = str(tmp_path / "ensemble.h5msm")
    msm.convert(source, to_form=path)
    monkeypatch.setattr(msm.configure, "chunk_size", 7)
    monkeypatch.setattr(msm.configure, "max_ram_usage", 2_000_000)
    from molsysmt.form import _h5msm05_modular

    monkeypatch.setattr(
        _h5msm05_modular,
        "read_molsys_file",
        lambda *a, **k: pytest.fail("Full file loaded."),
    )
    for item in (source, path):
        result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
            item, pbc=False, heavy_mode="force"
        )
        assert (
            result.n_interactions == 100
            and result.execution_records[0]["details"]["execution_chunks"] == 15
        )
    selected = msm.interactions.hydrophobic.get_hydrophobic_interactions(
        path, pbc=False, heavy_mode="force", structure_indices=[98, 1, 50, 1]
    )
    assert selected.occurrence_structures.tolist() == [1, 50, 98]
    monkeypatch.setattr(msm.configure, "max_ram_usage", 100)
    with pytest.raises(MemoryBudgetExceededError):
        msm.interactions.hydrophobic.get_hydrophobic_interactions(source, pbc=False)


def test_runtime_ackredit_credits_reference_and_not_reloading():
    ackredit = pytest.importorskip("ackredit")
    with ackredit.session("hydrophobic-producer"):
        result = msm.interactions.hydrophobic.get_hydrophobic_interactions(
            _system(), pbc=False
        )
        assert "doi:10.1186/s13321-021-00548-6" in ackredit.get_used_items()
    with ackredit.session("hydrophobic-reader"):
        typed = msm.convert(result, to_form="molsysmt.InteractionsDict")
        assert (
            msm.convert(typed, to_form="molsysmt.Interactions").parameters
            == result.parameters
        )
        assert ackredit.get_used_items() == {}


def test_exact_cutoff_and_empty_evaluation_have_explicit_scope():
    source = _system(n_frames=1)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, 4] = xyz[0, 1] + [0, 0.45, 0]
    source.structures.coordinates = puw.quantity(xyz, "nm")
    detector = msm.interactions.hydrophobic.get_hydrophobic_interactions
    assert detector(source, pbc=False).n_interactions == 1
    assert (
        detector(source, pbc=False, distance_threshold="0.449 nm").n_interactions == 0
    )
    empty = detector(source, pbc=False, selection=[])
    assert empty.evaluated_structure_indices.tolist() == [0]
    assert empty.evaluation_atom_indices.size == 0
    assert empty.query(structure_indices=[0]).to_dict()["occurrence_indices"].shape == (
        0,
    )
    absent = detector(source, pbc=False, structure_indices=[])
    assert absent.evaluated_structure_indices.shape == (0,)


def test_dense_candidates_fail_before_materializing_unbounded_sparse_output(
    monkeypatch,
):
    molecule = Chem.MolFromSmiles(".".join(["c1ccccc1"] * 18))
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    source.structures.append(
        coordinates=puw.quantity(np.zeros((1, molecule.GetNumAtoms(), 3)), "nm")
    )
    monkeypatch.setattr(msm.configure, "max_ram_usage", 500000)
    with pytest.raises(MemoryBudgetExceededError, match="candidate"):
        msm.interactions.hydrophobic.get_hydrophobic_interactions(source, pbc=False)
