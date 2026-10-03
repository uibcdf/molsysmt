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
    sites = msm.physchem.get_hbond_sites(prepared)
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
