"""Protecting chemical type provenance, projections and explicit PDBQT export."""

import json
import pickle

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import (
    StructuralAttributeDropWarning,
    StructuralInconsistencyError,
)

Chem = pytest.importorskip("rdkit.Chem")


def prepared(smiles="CC(=O)N"):
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    conf = Chem.Conformer(molecule.GetNumAtoms())
    conf.SetPositions(np.arange(molecule.GetNumAtoms() * 3, dtype=float).reshape(-1, 3))
    molecule.AddConformer(conf)
    output = msm.convert(molecule, to_form="molsysmt.MolSys")
    output.topology.atoms["atom_id"] = pd.array(
        [str(i + 1) for i in range(output.get_n_atoms())], dtype="string"
    )
    return output


def assign(source, **kwargs):
    return msm.build.assign_autodock_atom_types(
        source, typing_scheme="autodock4", **kwargs
    )


def write(source, destination):
    msm.convert(source, to_form=destination, typing_scheme="autodock4")
    return destination.read_text()


def test_detached_assignment_preserves_source_domains_and_original_versions():
    source = prepared()
    source.molecular_mechanics.partial_charge = np.arange(source.get_n_atoms()) / 10
    before = source.copy()
    result = assign(source, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert source.molecular_mechanics.atom_ff_type is None
    assert source.molecular_mechanics.atom_type_assignment is None
    pd.testing.assert_frame_equal(
        output.topology.atoms, source.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        output.chemical_states._states[0].atom_attributes,
        source.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        output.molecular_mechanics.partial_charge,
        before.molecular_mechanics.partial_charge,
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    saved = output.molecular_mechanics.atom_type_assignment
    report["software"]["rdkit"] = "modified after return"
    assert saved["software"]["rdkit"] != "modified after return"
    for restored in (output.copy(), pickle.loads(pickle.dumps(output))):
        assert (
            restored.molecular_mechanics.atom_type_assignment["software"]
            == saved["software"]
        )
        np.testing.assert_array_equal(
            restored.molecular_mechanics.atom_ff_type,
            output.molecular_mechanics.atom_ff_type,
        )
    assert output.molecular_mechanics.forcefield is None


def test_projection_retains_parent_types_and_source_indices(tmp_path):
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    output = msm.extract(source, selection=[3, 0])
    report = output.molecular_mechanics.atom_type_assignment
    assert report["status"] == "projected"
    assert report["atom_source_indices"].tolist() == [0, 3]
    assert report["evaluated_atom_indices"].tolist() == list(
        range(source.get_n_atoms())
    )
    assert report["n_atoms"] == source.get_n_atoms()
    assert report["atom_indices"].tolist() == [0, 1]
    assert output.molecular_mechanics.atom_ff_type.tolist() == ["C", "N"]
    # An isolated N with lost neighbors is not reclassified as an acceptor.
    np.testing.assert_array_equal(
        report["rule_indices"],
        source.molecular_mechanics.atom_type_assignment["rule_indices"][[0, 3]],
    )
    text = write(output, tmp_path / "projected.pdbqt")
    info = json.loads(
        next(
            line.removeprefix("REMARK MOLSYSMT_ATOM_TYPES ")
            for line in text.splitlines()
            if line.startswith("REMARK MOLSYSMT_ATOM_TYPES ")
        )
    )
    assert info["typing_scheme"] == "autodock4"
    assert info["rule_version"] == "chemical_environment@1"
    assert info["n_source_atoms"] == source.get_n_atoms()
    assert info["n_written_atoms"] == 2
    assert info["status"] == "projected"
    assert info["software"] == report["software"]
    restored = msm.convert(tmp_path / "projected.pdbqt", to_form="molsysmt.MolSys")
    assert restored.molecular_mechanics.atom_type_assignment is None
    assert restored.molecular_mechanics.atom_ff_type.tolist() == ["C", "N"]


@pytest.mark.parametrize("mutation", ["labels", "chemistry", "element"])
def test_stale_assignment_cannot_be_rebound_by_extraction_or_export(tmp_path, mutation):
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    if mutation == "labels":
        source.molecular_mechanics.atoms_ff.loc[0, "atom_ff_type"] = "A"
    elif mutation == "chemistry":
        source.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 1
    else:
        source.topology.atoms.loc[0, "atom_type"] = "N"
    destination = tmp_path / "invalid.pdbqt"
    for item in (source, msm.extract(source, selection=[0, 3])):
        with pytest.raises(StructuralInconsistencyError, match="bound chemistry"):
            write(item, destination)
    assert not destination.exists()


def test_manual_replacement_clears_named_typing_but_not_charges():
    output = assign(prepared())
    output = msm.build.assign_partial_charges(output, method="gasteiger_marsili")
    saved = output.molecular_mechanics.partial_charge_assignment["chemical_digest"]
    output.molecular_mechanics.atom_ff_type = (
        output.molecular_mechanics.atom_ff_type.copy()
    )
    assert output.molecular_mechanics.atom_type_assignment is None
    assert (
        output.molecular_mechanics.partial_charge_assignment["chemical_digest"] == saved
    )


def test_strict_join_rejects_false_joint_provenance_and_intersection_clears_it():
    source = assign(prepared())
    values = source.molecular_mechanics.atom_ff_type
    with pytest.raises(StructuralInconsistencyError, match="joint calculation"):
        msm.add(source, source.copy(), in_place=False, attribute_policy="strict")
    with pytest.warns(StructuralAttributeDropWarning, match="atom_type_assignment"):
        joined = msm.add(
            source, source.copy(), in_place=False, attribute_policy="intersection"
        )
    assert joined.molecular_mechanics.atom_type_assignment is None
    np.testing.assert_array_equal(
        joined.molecular_mechanics.atom_ff_type, np.concatenate([values, values])
    )
    assert source.molecular_mechanics.atom_type_assignment is not None


@pytest.mark.parametrize("charges_first", [False, True])
def test_charge_and_type_assignments_coexist_export_under_nondefault_units(
    tmp_path, charges_first
):
    source = prepared("CO")
    with msm.pyunitwizard.context(standard_units=["angstrom", "coulomb"]):
        if charges_first:
            source = assign(
                msm.build.assign_partial_charges(source, method="gasteiger_marsili")
            )
        else:
            source = msm.build.assign_partial_charges(
                assign(source), method="gasteiger_marsili"
            )
        text = write(source, tmp_path / "combined.pdbqt")
    for prefix, attr in [
        ("MOLSYSMT_PARTIAL_CHARGES", "partial_charge_assignment"),
        ("MOLSYSMT_ATOM_TYPES", "atom_type_assignment"),
    ]:
        report = json.loads(
            next(
                line.removeprefix("REMARK " + prefix + " ")
                for line in text.splitlines()
                if line.startswith("REMARK " + prefix + " ")
            )
        )
        assert (
            report["software"] == getattr(source.molecular_mechanics, attr)["software"]
        )
    loaded = msm.convert(tmp_path / "combined.pdbqt", to_form="molsysmt.MolSys")
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(loaded.structures.coordinates, to_unit="angstrom"),
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="angstrom"),
        atol=0.0005,
    )
    np.testing.assert_allclose(
        np.asarray(loaded.molecular_mechanics.partial_charge, dtype=float),
        np.asarray(source.molecular_mechanics.partial_charge, dtype=float),
        atol=0.0005 + 1e-12,
    )
    np.testing.assert_array_equal(
        loaded.molecular_mechanics.atom_ff_type, source.molecular_mechanics.atom_ff_type
    )


def test_geometry_does_not_stale_types_and_h5msm05_does_not_persist_mechanics(tmp_path):
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    source.structures.coordinates = source.structures.coordinates * 2
    assert "MOLSYSMT_ATOM_TYPES" in write(source, tmp_path / "moved.pdbqt")
    with pytest.raises(ValueError, match="cannot encode molecular mechanics"):
        msm.convert(source, to_form=tmp_path / "unsupported.h5msm")


def test_attachment_requires_nonempty_single_state_and_source_rdkit_is_unchanged():
    source = prepared()
    source.chemical_states._states.append(source.chemical_states._states[0].copy())
    with pytest.raises(StructuralInconsistencyError, match="one nonempty"):
        assign(source)
    with pytest.raises(StructuralInconsistencyError, match="one nonempty"):
        assign(Chem.Mol())
    rdkit = Chem.AddHs(Chem.MolFromSmiles("CO"))
    properties = [
        list(atom.GetPropNames(includePrivate=True)) for atom in rdkit.GetAtoms()
    ]
    assign(rdkit)
    assert [
        list(atom.GetPropNames(includePrivate=True)) for atom in rdkit.GetAtoms()
    ] == properties


def test_manual_mechanics_subset_setter_clears_typing_provenance():
    source = assign(prepared())
    msm.set(
        source.molecular_mechanics, element="atom", selection=[0], atom_ff_type=["C"]
    )
    assert source.molecular_mechanics.atom_type_assignment is None
    assert source.molecular_mechanics.atom_ff_type[3] == "N"


def test_bound_scheme_and_chemical_state_must_match_output(tmp_path):
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    source.molecular_mechanics.atom_type_assignment["typing_scheme"] = "incompatible"
    with pytest.raises(StructuralInconsistencyError, match="different typing_scheme"):
        write(source, tmp_path / "wrong_scheme.pdbqt")
    assert not (tmp_path / "wrong_scheme.pdbqt").exists()
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    second = source.chemical_states._states[0].copy()
    second.state_id = "other"
    source.chemical_states._states.append(second)
    source._structure_chemical_state_indices = pd.array([1], dtype="Int64")
    with pytest.raises(StructuralInconsistencyError, match="associated"):
        write(source, tmp_path / "wrong_state.pdbqt")
    assert not (tmp_path / "wrong_state.pdbqt").exists()


def test_query_input_is_rejected_before_attachment_conversion():
    with pytest.raises(StructuralInconsistencyError, match="query"):
        assign(Chem.MolFromSmarts("[C]"))
