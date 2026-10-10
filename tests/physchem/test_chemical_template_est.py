"""Protecting a pinned real EST template, its source pose and explicit stereo choice."""

import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm

DATA = Path(__file__).parent / "data" / "chemical_templates"


@pytest.fixture(scope="module")
def est_case():
    manifest = json.loads((DATA / "manifest.json").read_text())
    for filename, checksum in manifest["artifact_sha256"].items():
        assert hashlib.sha256((DATA / filename).read_bytes()).hexdigest() == checksum
    assert (
        hashlib.sha256(gzip.decompress((DATA / "1qku.cif.gz").read_bytes())).hexdigest()
        == manifest["source_sha256"]
    )
    source = msm.convert(str(DATA / "1qku.cif.gz"), to_form="molsysmt.MolSys")
    assert source.get_n_atoms() == 6596
    assert msm.get(source, n_structures=True) == 1
    assert (
        list(msm.select(source, selection=manifest["source_selection"]))
        == manifest["source_atom_indices"]
    )
    ligand = msm.extract(source, selection=manifest["source_selection"])
    assert ligand.get_n_atoms() == 20
    assert msm.get(ligand, n_bonds=True) == 23
    assert (
        list(msm.get(ligand, element="atom", atom_name=True))
        == manifest["source_atom_names"]
    )
    return ligand, manifest


def _prepare(ligand, manifest):
    return msm.physchem.apply_chemical_template(
        ligand,
        template=DATA / "est_template.h5msm",
        atom_correspondence=manifest["atom_correspondence"],
        template_provenance=manifest["template_provenance"],
    )


@pytest.mark.parametrize("source_form", ["native", "h5msm"])
def test_real_est_assignment_in_full_complex_preserves_unassessed_receptor(
    est_case,
    tmp_path,
    source_form,
):
    ligand, manifest = est_case
    source = msm.convert(DATA / "1qku.cif.gz", to_form="molsysmt.MolSys")
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.chemical_states.get_bonds().copy(deep=True)
    molecular_system = source
    if source_form == "h5msm":
        molecular_system = tmp_path / "full-source.h5msm"
        msm.convert(source, to_form=molecular_system)
    local_map = np.asarray(manifest["atom_correspondence"], dtype=np.int64)
    indices = np.asarray(manifest["source_atom_indices"], dtype=np.int64)
    full_map = local_map.copy()
    full_map[:, 1] = indices[local_map[:, 1]]
    output = msm.physchem.apply_chemical_template(
        molecular_system,
        template=DATA / "est_template.h5msm",
        atom_correspondence=full_map,
        template_provenance=manifest["template_provenance"],
        selection=manifest["source_selection"],
    )
    prepared = output["molecular_system"]
    assert prepared.get_n_atoms() == 6596
    assert prepared.chemical_states._states[0].connectivity_completeness == "partial"
    assert output["report"]["coverage"]["scope"] == "selected_component"
    np.testing.assert_array_equal(output["report"]["source"]["atom_indices"], indices)
    pd.testing.assert_frame_equal(prepared.topology.atoms, before_atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(prepared.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    attrs = prepared.chemical_states._states[0].atom_attributes
    outside = np.setdiff1d(np.arange(6596), indices)
    assert attrs.iloc[outside].isna().all().all()
    original_pairs = before_bonds[["atom1_index", "atom2_index"]]
    pd.testing.assert_frame_equal(
        prepared.chemical_states.get_bonds()[["atom1_index", "atom2_index"]],
        original_pairs,
    )
    selected_bonds = before_bonds.atom1_index.isin(
        indices
    ) & before_bonds.atom2_index.isin(indices)
    pd.testing.assert_frame_equal(
        prepared.chemical_states.get_bonds().loc[~selected_bonds, before_bonds.columns],
        before_bonds.loc[~selected_bonds],
    )
    assert source.chemical_states._states[0].atom_attributes.empty
    path = tmp_path / "prepared-complex.h5msm"
    msm.convert(prepared, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    assert restored.chemical_states._states[0].connectivity_completeness == "partial"
    pd.testing.assert_frame_equal(
        restored.chemical_states._states[0].atom_attributes, attrs
    )
    extracted = msm.extract(restored, selection=manifest["source_selection"])
    isolated = _prepare(ligand, manifest)["molecular_system"]
    pd.testing.assert_frame_equal(
        extracted.chemical_states._states[0].atom_attributes,
        isolated.chemical_states._states[0].atom_attributes,
    )
    # Extraction preserves the parent's conservative global connectivity status.
    assert extracted.chemical_states._states[0].connectivity_completeness == "partial"
    reassessed = _prepare(extracted, manifest)["molecular_system"]
    assert reassessed.chemical_states._states[0].connectivity_completeness == "complete"
    assert msm.physchem.get_aromatic_rings(reassessed)["atom_offsets"].tolist() == [
        0,
        6,
    ]


def test_real_est_native_template_preserves_pose_and_known_chemical_controls(
    est_case, tmp_path
):
    ligand, manifest = est_case
    before_atoms = ligand.topology.atoms.copy(deep=True)
    before_bonds = ligand.chemical_states.get_bonds().copy(deep=True)
    original = {
        field: np.asarray(
            msm.pyunitwizard.get_value(getattr(ligand.structures, field))
        ).copy()
        for field in ("coordinates", "box")
        if getattr(ligand.structures, field) is not None
    }
    with msm.pyunitwizard.context(standard_units=["pm", "fs"]):
        result = _prepare(ligand, manifest)
    prepared = result["molecular_system"]
    assert result["report"]["status"] == "applied"
    assert prepared.get_n_atoms() == 20
    assert msm.get(prepared, n_bonds=True) == 23
    assert result["report"]["coverage"]["explicit_hydrogen_atom_indices"].size == 0
    pd.testing.assert_frame_equal(prepared.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(ligand.chemical_states.get_bonds(), before_bonds)
    assert ligand.chemical_states._states[0].atom_attributes.empty
    assert ligand.chemical_states._states[0].connectivity_completeness == "partial"
    for field, values in original.items():
        np.testing.assert_array_equal(
            msm.pyunitwizard.get_value(getattr(prepared.structures, field)), values
        )
        assert msm.pyunitwizard.get_unit(
            getattr(prepared.structures, field)
        ) == msm.pyunitwizard.get_unit(getattr(ligand.structures, field))
    state = prepared.chemical_states._states[0]
    assert state.connectivity_completeness == "complete"
    assert state.atom_attributes["formal_charge"].tolist() == [0] * 20
    np.testing.assert_array_equal(
        state.atom_attributes["n_implicit_hydrogens"].to_numpy(dtype=int)
        + state.atom_attributes["n_explicit_hydrogens"].to_numpy(dtype=int),
        manifest["expected_hydrogen_counts"],
    )
    assert sum(manifest["expected_hydrogen_counts"]) == 24
    ring = msm.physchem.get_aromatic_rings(prepared)
    assert ring["atom_offsets"].tolist() == [0, 6]
    assert ring["atom_indices"].tolist() == [0, 1, 2, 4, 5, 10]
    sites = msm.interactions.hbonds.get_hbond_sites(prepared)
    assert sites["acceptor_atom_indices"].tolist() == [3, 18]
    assert sites["donor_hydrogen_pairs"].shape == (0, 2)
    target = tmp_path / "prepared_est.h5msm"
    msm.convert(prepared, to_form="file:h5msm", output_filename=str(target))
    loaded = msm.convert(target, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes, state.atom_attributes
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates),
        original["coordinates"],
    )


def test_real_est_canonical_stereo_matches_pose_and_does_not_copy_conflicting_ccd_flag(
    est_case,
):
    pytest.importorskip("rdkit")
    ligand, manifest = est_case
    prepared = _prepare(ligand, manifest)["molecular_system"]
    declared = msm.physchem.get_cip_stereochemistry(prepared)
    observed = msm.physchem.get_cip_stereochemistry(
        prepared, structure_indices=[0], from_coordinates=True
    )
    expected = [
        manifest["expected_stereo"][name] for name in manifest["source_atom_names"]
    ]
    np.testing.assert_array_equal(declared["atom_stereochemistry"], expected)
    np.testing.assert_array_equal(observed["atom_stereochemistry"], expected)
    assert {
        name: label for name, label in manifest["expected_stereo"].items() if label
    } == {
        "C8": "R",
        "C9": "S",
        "C13": "S",
        "C14": "S",
        "C17": "S",
    }
    assert manifest["ccd_stereo_disagreements"]["C8"] == {
        "ccd_atom_flag": "S",
        "canonical_and_pose_cip": "R",
    }
    assert (
        prepared.chemical_states._states[0].atom_attributes.at[8, "stereochemistry"]
        == "R"
    )
