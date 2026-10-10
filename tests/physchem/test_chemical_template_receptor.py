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
    sites = msm.interactions.hbonds.get_hbond_sites(
        prepared, method="smarts_donor_acceptor"
    )
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
    sites = msm.interactions.hbonds.get_hbond_sites(
        hydrogenated, method="smarts_donor_acceptor"
    )
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


@pytest.fixture(scope="module")
def prepared_interface_case(receptor_case):
    """Compose separately declared receptor/EST chemistry through public tools."""
    pytest.importorskip("rdkit")
    full, receptor_indices, _, _, _, _, receptor_result = receptor_case
    manifest = json.loads((DATA / "manifest.json").read_text())
    ligand = msm.extract(full, selection=manifest["source_selection"])
    ligand_result = msm.physchem.apply_chemical_template(
        ligand,
        template=DATA / "est_template.h5msm",
        atom_correspondence=manifest["atom_correspondence"],
        template_provenance=manifest["template_provenance"],
    )
    prepared = [receptor_result["molecular_system"], ligand_result["molecular_system"]]
    hydrogenated = []
    for item in prepared:
        with pytest.warns(StructuralAttributeDropWarning, match="b_factor"):
            result = msm.build.add_missing_hydrogens(
                item,
                pH=None,
                engine="RDKit",
                mode="fixed_chemical_state",
                return_report=True,
            )
        hydrogenated.append(result["molecular_system"])
    interface = msm.merge(hydrogenated, to_form="molsysmt.MolSys")
    atom_sources = np.concatenate(
        [
            receptor_indices,
            np.full(2028, -1, dtype=np.int64),
            np.asarray(manifest["source_atom_indices"], dtype=np.int64),
            np.full(24, -1, dtype=np.int64),
        ]
    )
    receptor_atoms = np.arange(4003, dtype=np.int64)
    ligand_atoms = np.arange(4003, 4047, dtype=np.int64)
    return (
        full,
        prepared,
        hydrogenated,
        interface,
        atom_sources,
        receptor_atoms,
        ligand_atoms,
    )


def test_prepared_interface_preserves_declared_chemistry_pose_and_source_scope(
    prepared_interface_case,
):
    full, prepared, hydrogenated, interface, atom_sources, receptor, ligand = (
        prepared_interface_case
    )
    assert interface.get_n_atoms() == 4047
    assert len(interface.chemical_states.get_bonds()) == 4088
    assert interface.chemical_states._states[0].connectivity_completeness == "complete"
    assert full.get_n_atoms() == 6596
    assert full.chemical_states._states[0].connectivity_completeness == "partial"
    assert full.chemical_states._states[0].atom_attributes.empty
    np.testing.assert_array_equal(
        np.concatenate(
            [item.topology.atoms.atom_id.to_numpy() for item in hydrogenated]
        ),
        interface.topology.atoms.atom_id,
    )
    pd.testing.assert_frame_equal(
        interface.chemical_states._states[0].atom_attributes,
        pd.concat(
            [item.chemical_states._states[0].atom_attributes for item in hydrogenated],
            ignore_index=True,
        ),
    )
    observed = np.flatnonzero(atom_sources >= 0)
    np.testing.assert_array_equal(
        interface.topology.atoms.atom_id.iloc[observed],
        full.topology.atoms.atom_id.iloc[atom_sources[observed]],
    )
    xyz = msm.pyunitwizard.get_value(interface.structures.coordinates, to_unit="nm")
    np.testing.assert_array_equal(
        xyz[:, observed],
        msm.pyunitwizard.get_value(full.structures.coordinates, to_unit="nm")[
            :, atom_sources[observed]
        ],
    )
    assert len(observed) == sum(item.get_n_atoms() for item in prepared) == 1995
    assert np.count_nonzero(atom_sources == -1) == 2052
    assert not set(
        msm.select(
            full, selection='chain_id == "A" and group_id in ["301", "302", "303"]'
        )
    ).intersection(atom_sources[observed])
    assert msm.physchem.get_aromatic_rings(interface)["atom_offsets"].size == 33
    assert receptor.size == 4003 and ligand.size == 44


@pytest.mark.parametrize("input_form", ["native", "h5msm"])
def test_prepared_interface_named_analyses_queries_source_maps_and_persistence(
    prepared_interface_case,
    tmp_path,
    input_form,
):
    full, _, _, interface, atom_sources, receptor, ligand = prepared_interface_case
    if input_form == "native":
        molecular_system = interface
    else:
        molecular_system = tmp_path / "chemical_interface.h5msm"
        msm.convert(
            interface, to_form="file:h5msm", output_filename=str(molecular_system)
        )
    detectors = {
        "hydrophobic": (msm.interactions.hydrophobic.get_hydrophobic_interactions, {}),
        "hbonds": (
            msm.interactions.hbonds.get_hbonds,
            dict(
                method="donor_acceptor_distance_angle", profile="smarts_donor_acceptor"
            ),
        ),
        "pi_pi": (
            msm.interactions.pi_pi.get_pi_pi_interactions,
            dict(method="plane_angle_intersection", profile="smarts_5_6"),
        ),
    }
    analyses = {}
    for name, (detector, options) in detectors.items():
        result = detector(
            molecular_system,
            selection=receptor,
            selection_2=ligand,
            selection_mode="between",
            structure_indices=[0, 0],
            pbc=False,
            **options,
        )
        assert result.evaluated_structure_indices.tolist() == [0]
        assert result.software["molsysmt"]
        assert result.parameters["attribution"]["items"]
        assert result.evaluation_scope["mode"] == "between"
        # Declare the inspected local-to-deposited map through the typed public form.
        # The detector's local indices and producer identity are not changed.
        payload = msm.convert(result, to_form="molsysmt.InteractionsDict")
        payload.data["atom_source_indices"] = atom_sources.copy()
        payload.data["source_n_atoms"] = full.get_n_atoms()
        payload.data["source_id"] = "rcsb:1QKU:deposited-atom-order"
        mapped = msm.convert(payload, to_form="molsysmt.Interactions")
        analyses[name] = mapped
        assert (
            mapped.query(
                structure_indices=[0, 0],
                atom_indices=ligand,
                mode="involving_selection",
            ).n_interactions
            == result.n_interactions
        )
        assert (
            mapped.query(atom_indices=ligand, mode="within_selection").n_interactions
            == 0
        )
        assert (
            mapped.between_selections(
                receptor, ligand, structure_indices=[0, 0], exclusive=True
            ).n_interactions
            == result.n_interactions
        )
    # These are definition/geometry checkpoints, not biological absence claims.
    assert analyses["hydrophobic"].n_interactions == 12
    assert analyses["hbonds"].n_interactions == 0
    assert analyses["pi_pi"].n_interactions == 0
    xyz = msm.pyunitwizard.get_value(interface.structures.coordinates, to_unit="nm")[0]
    # Close oxygen pairs are eligible sites, but local OH geometry fails the angle.
    sites = msm.interactions.hbonds.get_hbond_sites(
        interface, method="smarts_donor_acceptor"
    )
    triples = np.asarray([[4006, 4025, 379], [4021, 4043, 1754]], dtype=np.int64)
    donor_pairs = set(map(tuple, sites["donor_hydrogen_pairs"].tolist()))
    assert all(tuple(row[:2]) in donor_pairs for row in triples)
    assert set(triples[:, 2]).issubset(sites["acceptor_atom_indices"].tolist())
    donors, hydrogens, acceptors = xyz[triples.T]
    assert (np.linalg.norm(donors - acceptors, axis=1) < 0.35).all()
    dh, ah = donors - hydrogens, acceptors - hydrogens
    cosines = np.einsum("ij,ij->i", dh, ah) / (
        np.linalg.norm(dh, axis=1) * np.linalg.norm(ah, axis=1)
    )
    assert (np.degrees(np.arccos(np.clip(cosines, -1.0, 1.0))) < 130.0).all()
    pairs = []
    hydrophobic = analyses["hydrophobic"]
    for relation_index in hydrophobic.occurrence_relations:
        participants = hydrophobic.relation(relation_index)["participants"]
        pairs.append(
            [int(participant["atom_indices"][0]) for participant in participants]
        )
    pairs = np.asarray(pairs, dtype=np.int64)
    distances = np.linalg.norm(xyz[pairs[:, 0]] - xyz[pairs[:, 1]], axis=1)
    assert (pairs[:, 0] < 4003).all() and (pairs[:, 1] >= 4003).all()
    assert (distances <= 0.45).all()
    assert hydrophobic.measure_units["distance"] == "nm"
    np.testing.assert_allclose(hydrophobic.measurements["distance"], distances)
    named = interface.copy()
    named.interactions = analyses
    path = tmp_path / "named_interface.h5msm"
    msm.convert(named, to_form="file:h5msm", output_filename=str(path))
    loaded = msm.convert(path, to_form="molsysmt.MolSys")
    assert set(loaded.interactions) == set(analyses)
    assert loaded.get_n_atoms() == interface.get_n_atoms()
    pd.testing.assert_frame_equal(
        loaded.chemical_states._states[0].atom_attributes,
        interface.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(interface.structures.coordinates, to_unit="nm"),
    )
    assert interface.interactions == {}
    for name, original in analyses.items():
        restored = loaded.interactions[name]
        np.testing.assert_array_equal(restored.atom_source_indices, atom_sources)
        np.testing.assert_array_equal(
            restored.query(structure_indices=[0]).to_dict()["occurrence_indices"],
            original.query(structure_indices=[0]).to_dict()["occurrence_indices"],
        )
        np.testing.assert_array_equal(
            restored.participant_atoms, original.participant_atoms
        )
        assert restored.evaluated_structure_indices.tolist() == [0]
        assert restored.source_id == original.source_id
        assert restored.source_n_atoms == full.get_n_atoms()
        np.testing.assert_array_equal(restored.structure_source_indices, [0])
        assert restored.software == original.software
        assert restored.parameters == original.parameters
        assert restored.measure_units == original.measure_units
        for field in original.measurements:
            np.testing.assert_array_equal(
                restored.measurements[field], original.measurements[field]
            )
