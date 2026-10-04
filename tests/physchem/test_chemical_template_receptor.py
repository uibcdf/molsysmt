"""Protecting explicit preparation of a bounded observed 1QKU peptide fragment."""

import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralAttributeDropWarning

DATA = Path(__file__).parent / "data" / "chemical_templates"


@pytest.fixture(scope="module")
def receptor_case():
    manifest = json.loads((DATA / "manifest.json").read_text())
    assert (
        hashlib.sha256(gzip.decompress((DATA / "1qku.cif.gz").read_bytes())).hexdigest()
        == manifest["source_sha256"]
    )
    full = msm.convert(DATA / "1qku.cif.gz", to_form="molsysmt.MolSys")
    selection = msm.select(
        full,
        selection='molecule_type == "protein" and chain_id == "A" '
        'and group_id not in ["301", "302", "303"]',
    )
    source = msm.extract(full, selection=selection)
    names = source.topology.groups.group_name.tolist()
    # Operator choices for this scenario, not an environmental protonation model.
    definition = msm.physchem.get_peptide_chemical_template(
        ["HIE" if name == "HIS" else name for name in names],
        "ammonium",
        "carboxylate",
    )
    template = definition["template"]
    lookup = {
        (int(row.group_index), row.atom_name): int(index)
        for index, row in source.topology.atoms.iterrows()
    }
    mapping = []
    for index, row in template.topology.atoms.iterrows():
        name = row.atom_name
        # Explicit equivalent-N correspondence matches the observed ARG drawing.
        if names[int(row.group_index)] == "ARG" and name in {"NH1", "NH2"}:
            name = "NH2" if name == "NH1" else "NH1"
        mapping.append([int(index), lookup[(int(row.group_index), name)]])
    mapping = np.asarray(mapping, dtype=np.int64)
    normalization = msm.physchem.normalize_aromatic_bond_orders(source)
    applied = msm.physchem.apply_chemical_template(
        normalization["molecular_system"],
        template,
        mapping,
        definition["template_provenance"],
    )
    return full, selection, source, definition, mapping, normalization, applied


def test_observed_fragment_requires_explicit_normalization_and_preserves_source(
    receptor_case,
    tmp_path,
):
    full, selection, source, definition, mapping, normalized, applied = receptor_case
    receptor = msm.extract(
        full, selection='molecule_type == "protein" and chain_id == "A"'
    )
    coverage = msm.build.get_residue_chemical_coverage(receptor)
    incomplete = [g for g in coverage["groups"] if g["status"] == "incomplete"]
    assert len(coverage["groups"]) == 250
    assert len(incomplete) == 3
    assert receptor.topology.groups.loc[
        [g["group_index"] for g in incomplete], "group_id"
    ].tolist() == ["301", "302", "303"]
    report = msm.physchem.assess_chemical_template(
        source, definition["template"], mapping, definition["template_provenance"]
    )
    assert report["status"] != "compatible"
    assert any(
        i["reason_code"] == "aromatic_representation_requires_normalization"
        for i in report["issues"]
    )
    assert normalized["report"]["changed_bond_indices"].size == 167
    assert source.get_n_atoms() == 1975
    assert source.topology.groups.group_id.tolist() == [str(i) for i in range(304, 551)]
    assert sorted(mapping[:, 1].tolist()) == list(range(1975))
    prepared = applied["molecular_system"]
    assert applied["report"]["status"] == "applied"
    assert len(applied["report"]["added_bonds"]) == 0
    assert len(prepared.chemical_states.get_bonds()) == 2013
    assert prepared.chemical_states._states[0].connectivity_completeness == "complete"
    assert source.chemical_states._states[0].connectivity_completeness == "partial"
    assert source.chemical_states._states[0].atom_attributes.empty
    pd.testing.assert_frame_equal(prepared.topology.atoms, source.topology.atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(prepared.structures.coordinates),
        msm.pyunitwizard.get_value(full.structures.coordinates)[:, selection],
    )
    assert msm.pyunitwizard.get_unit(prepared.structures.coordinates) == (
        msm.pyunitwizard.get_unit(source.structures.coordinates)
    )
    assert msm.physchem.get_aromatic_rings(prepared)["atom_offsets"].size == 32
    path = tmp_path / "prepared_fragment.h5msm"
    msm.convert(prepared, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        prepared.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates),
        msm.pyunitwizard.get_value(prepared.structures.coordinates),
    )


def test_prepared_fragment_smarts_excludes_amide_and_guanidinium_acceptors(
    receptor_case,
):
    pytest.importorskip("rdkit")
    prepared = receptor_case[-1]["molecular_system"]
    sites = msm.physchem.get_hbond_sites(prepared, method="smarts_donor_acceptor")
    acceptors = set(sites["acceptor_atom_indices"].tolist())
    atoms = prepared.topology.atoms
    assert acceptors
    assert not acceptors.intersection(atoms.index[atoms.atom_name.eq("N")])
    arg_groups = prepared.topology.groups.index[
        prepared.topology.groups.group_name.eq("ARG")
    ]
    arg_nitrogens = atoms.index[
        atoms.group_index.isin(arg_groups) & atoms.atom_name.isin(["NE", "NH1", "NH2"])
    ]
    assert len(arg_groups) == 11
    assert not acceptors.intersection(arg_nitrogens)
    assert set(atoms.index[atoms.atom_name.eq("O")]).issubset(acceptors)
    assert sites["donor_hydrogen_pairs"].shape == (0, 2)


def test_fixed_state_fragment_hydrogens_keep_heavy_pose_and_h5msm(
    receptor_case, tmp_path
):
    pytest.importorskip("rdkit")
    prepared = receptor_case[-1]["molecular_system"]
    original = prepared.copy()
    with pytest.warns(StructuralAttributeDropWarning, match="b_factor"):
        result = msm.build.add_missing_hydrogens(
            prepared,
            pH=None,
            engine="RDKit",
            mode="fixed_chemical_state",
            return_report=True,
        )
    hydrogenated = result["molecular_system"]
    assert result["report"]["n_added_hydrogens"] == 2028
    assert hydrogenated.get_n_atoms() == 4003
    assert hydrogenated.topology.atoms.atom_type.iloc[1975:].eq("H").all()
    assert hydrogenated.topology.atoms.atom_id.iloc[:1975].tolist() == (
        original.topology.atoms.atom_id.tolist()
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(hydrogenated.structures.coordinates)[:, :1975],
        msm.pyunitwizard.get_value(original.structures.coordinates),
    )
    pd.testing.assert_frame_equal(prepared.topology.atoms, original.topology.atoms)
    pd.testing.assert_frame_equal(
        prepared.chemical_states._states[0].atom_attributes,
        original.chemical_states._states[0].atom_attributes,
    )
    sites = msm.physchem.get_hbond_sites(hydrogenated, method="smarts_donor_acceptor")
    pairs = sites["donor_hydrogen_pairs"]
    assert pairs.size
    assert (pairs[:, 0] < 1975).all() and (pairs[:, 1] >= 1975).all()
    path = tmp_path / "hydrogenated_fragment.h5msm"
    msm.convert(hydrogenated, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates),
        msm.pyunitwizard.get_value(hydrogenated.structures.coordinates),
    )
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        hydrogenated.chemical_states._states[0].atom_attributes,
    )
