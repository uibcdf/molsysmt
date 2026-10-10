"""Validating native charge provenance, projections and bounded PDBQT export."""

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
puw = msm.pyunitwizard


def prepared(smiles="CO"):
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    # Charges do not use this synthetic pose. It exercises coordinate retention.
    conf = Chem.Conformer(molecule.GetNumAtoms())
    conf.SetPositions(np.arange(molecule.GetNumAtoms() * 3, dtype=float).reshape(-1, 3))
    molecule.AddConformer(conf)
    source = msm.convert(molecule, to_form="molsysmt.MolSys")
    source.topology.atoms["atom_id"] = pd.array(
        [str(i + 1) for i in range(source.get_n_atoms())], dtype="string"
    )
    source.molecular_mechanics.atom_ff_type = source.topology.atoms[
        "atom_type"
    ].to_numpy()
    return source


def assign(source, **kwargs):
    return msm.build.assign_partial_charges(
        source, method="gasteiger_marsili", **kwargs
    )


def write(source, path):
    msm.convert(source, to_form=path, typing_scheme="autodock4")
    return path.read_text()


@pytest.mark.parametrize("units", [["pm", "fs"], ["pm", "fs", "coulomb"]])
@pytest.mark.parametrize("form", ["molsysmt.MolSys", "rdkit.Mol"])
def test_native_assignment_needs_no_charge_presentation_standard(units, form):
    source = prepared()
    if form == "rdkit.Mol":
        source = msm.convert(source, to_form=form)
        before = Chem.MolToMolBlock(source)
    else:
        before = source.copy()
    with puw.context(standard_units=units):
        policy = puw.configure.report()
        result = assign(source, return_report=True)
        assert puw.configure.report() == policy
    output, report = result["molecular_system"], result["report"]
    values = np.asarray(output.molecular_mechanics.partial_charge, dtype=float)
    np.testing.assert_allclose(
        values,
        [
            0.03194068372,
            -0.39963024356,
            0.05268663182,
            0.05268663182,
            0.05268663182,
            0.20962966439,
        ],
        rtol=0,
        atol=1e-10,
    )
    assert report["charge_unit"] == "elementary_charge"
    assert report["coverage"] == "complete"
    assert report["total_charge"] == pytest.approx(0, abs=1e-10)
    assert report["attribution"]["target"] == "molsysmt.physchem.get_partial_charges"
    saved = output.molecular_mechanics.partial_charge_assignment
    assert saved["software"] == report["software"]
    assert saved["references"] == report["references"]
    if form == "rdkit.Mol":
        assert Chem.MolToMolBlock(source) == before
        assert not any(atom.HasProp("_GasteigerCharge") for atom in source.GetAtoms())
    else:
        assert source.molecular_mechanics.partial_charge is None
        pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
        pd.testing.assert_frame_equal(
            source.chemical_states._states[0].atom_attributes,
            before.chemical_states._states[0].atom_attributes,
        )
        np.testing.assert_array_equal(
            puw.get_value(source.structures.coordinates, to_unit="nm"),
            puw.get_value(before.structures.coordinates, to_unit="nm"),
        )


def test_native_nonzero_total_quantity_needs_no_charge_standard():
    source = prepared("[NH4+]")
    declaration = puw.convert(puw.quantity(1, "elementary_charge"), to_unit="coulomb")
    with puw.context(standard_units=["pm", "fs"]):
        policy = puw.configure.report()
        result = assign(source, expected_total_charge=declaration, return_report=True)
        assert puw.configure.report() == policy
        with pytest.raises(StructuralInconsistencyError, match="conflicts"):
            assign(source, expected_total_charge=0)
        assert puw.configure.report() == policy
    values = np.asarray(
        result["molecular_system"].molecular_mechanics.partial_charge, dtype=float
    )
    assert values.shape == (5,)
    assert np.isfinite(values).all()
    assert values.sum() == pytest.approx(1, abs=1e-10)
    assert result["report"]["expected_total_charge"] == pytest.approx(1)
    assert result["report"]["total_charge_source"] == "caller_declaration"
    assert source.molecular_mechanics.partial_charge is None


def test_native_forcefield_assignment_needs_no_charge_standard():
    pytest.importorskip("openmm")
    source = msm.convert("molsysmt/data/pdb/ala3.pdb", to_form="molsysmt.MolSys")
    with puw.context(standard_units=["pm", "fs"]):
        policy = puw.configure.report()
        output = msm.build.assign_partial_charges(
            source,
            method="forcefield",
            forcefield="AMBER14",
            expected_total_charge=0,
        )
        assert puw.configure.report() == policy
    values = np.asarray(output.molecular_mechanics.partial_charge, dtype=float)
    assert values.shape == (source.get_n_atoms(),)
    names = source.topology.atoms["atom_name"].to_numpy()
    groups = source.topology.atoms["group_index"].to_numpy()
    actual = {
        name: values[i]
        for i, (name, group) in enumerate(zip(names, groups))
        if group == 1
    }
    # Independent ff14SB template controls, as in the public getter guard.
    assert actual["N"] == pytest.approx(-0.4157)
    assert actual["H"] == pytest.approx(0.2719)
    assert actual["O"] == pytest.approx(-0.5679)
    assert values.sum() == pytest.approx(0, abs=1e-8)
    assert output.molecular_mechanics.partial_charge_assignment["software"]["openmm"]
    assert source.molecular_mechanics.partial_charge is None


def test_assignment_is_detached_and_preserves_domains_and_original_software():
    source = prepared()
    before = source.copy()
    with puw.context(standard_units=["coulomb", "angstrom"]):
        result = assign(source, return_report=True)
    output, report = result["molecular_system"], result["report"]
    assert source.molecular_mechanics.partial_charge is None
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    # Native conversion may use a plain DataFrame instead of its construction
    # subclass. The public contract preserves columns, dtypes, indices and values.
    pd.testing.assert_frame_equal(
        output.topology.atoms, source.topology.atoms, check_frame_type=False
    )
    pd.testing.assert_frame_equal(
        output.chemical_states._states[0].atom_attributes,
        source.chemical_states._states[0].atom_attributes,
    )
    np.testing.assert_array_equal(
        puw.get_value(output.structures.coordinates, to_unit="nm"),
        puw.get_value(source.structures.coordinates, to_unit="nm"),
    )
    values = np.asarray(output.molecular_mechanics.partial_charge, dtype=float)
    assert values[1] == pytest.approx(-0.3996, abs=5e-5)
    assert output.molecular_mechanics.forcefield is None
    saved = output.molecular_mechanics.partial_charge_assignment
    assert saved["software"] == report["software"]
    report["software"]["rdkit"] = "changed after return"
    assert saved["software"]["rdkit"] != "changed after return"
    for restored in [output.copy(), pickle.loads(pickle.dumps(output))]:
        assert (
            restored.molecular_mechanics.partial_charge_assignment["software"]
            == saved["software"]
        )
        np.testing.assert_array_equal(
            restored.molecular_mechanics.partial_charge,
            output.molecular_mechanics.partial_charge,
        )


def test_projection_keeps_parent_charges_and_declares_original_scope(tmp_path):
    output = assign(prepared())
    projection = msm.extract(output, selection=[1, 0])
    report = projection.molecular_mechanics.partial_charge_assignment
    assert report["status"] == "projected"
    assert report["atom_source_indices"].tolist() == [0, 1]
    assert report["n_atoms"] == output.get_n_atoms()
    np.testing.assert_array_equal(
        projection.molecular_mechanics.partial_charge,
        output.molecular_mechanics.partial_charge[:2],
    )
    text = write(projection, tmp_path / "projection.pdbqt")
    info = json.loads(
        text.splitlines()[0].removeprefix("REMARK MOLSYSMT_PARTIAL_CHARGES ")
    )
    assert info["n_written_atoms"] == 2
    assert info["n_source_atoms"] == output.get_n_atoms()
    assert info["status"] == "projected"
    assert info["total_charge_before_rounding"] != pytest.approx(0)
    assert info["decimal_places"] == 3


def test_join_does_not_claim_a_joint_charge_calculation():
    source = assign(prepared())
    values = np.asarray(source.molecular_mechanics.partial_charge, dtype=float)
    with pytest.raises(StructuralInconsistencyError, match="joint calculation"):
        msm.add(source, source.copy(), in_place=False, attribute_policy="strict")
    assert source.get_n_atoms() == len(values)
    assert source.molecular_mechanics.partial_charge_assignment is not None
    with pytest.warns(
        StructuralAttributeDropWarning, match="partial_charge_assignment"
    ):
        joined = msm.add(
            source, source.copy(), in_place=False, attribute_policy="intersection"
        )
    np.testing.assert_array_equal(
        joined.molecular_mechanics.partial_charge, np.concatenate([values, values])
    )
    assert joined.molecular_mechanics.partial_charge_assignment is None


@pytest.mark.parametrize("mutation", ["charge", "chemistry", "element"])
def test_changed_bound_assignment_is_rejected_even_after_projection(tmp_path, mutation):
    source = assign(prepared())
    if mutation == "charge":
        source.molecular_mechanics.atoms_ff.loc[0, "partial_charge"] = 0.5
    elif mutation == "chemistry":
        source.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 1
    else:
        source.topology.atoms.loc[0, "atom_type"] = "N"
    destination = tmp_path / "stale.pdbqt"
    for item in [source, msm.extract(source, selection=[0, 1])]:
        with pytest.raises(StructuralInconsistencyError, match="bound chemistry"):
            write(item, destination)
    assert not destination.exists()


def test_coordinate_changes_do_not_stale_graph_based_charges(tmp_path):
    source = assign(prepared())
    source.structures.coordinates = source.structures.coordinates * 2
    assert write(source, tmp_path / "moved.pdbqt").startswith(
        "REMARK MOLSYSMT_PARTIAL_CHARGES "
    )


def test_explicit_charge_replacement_clears_model_attribution():
    source = assign(prepared())
    source.molecular_mechanics.partial_charge = np.zeros(source.get_n_atoms())
    assert source.molecular_mechanics.partial_charge_assignment is None
    source = assign(prepared())
    msm.set(source, element="atom", selection=[0], partial_charge=[0.2])
    assert source.molecular_mechanics.partial_charge_assignment is None


def test_multiple_state_storage_is_rejected_without_touching_source():
    source = prepared()
    source.chemical_states._states.append(source.chemical_states._states[0].copy())
    with pytest.raises(StructuralInconsistencyError, match="exactly one"):
        assign(source)
    assert source.molecular_mechanics.partial_charge is None


def test_h5msm_05_does_not_silently_store_experimental_mechanics(tmp_path):
    source = assign(prepared())
    with pytest.raises(ValueError, match="cannot encode molecular mechanics"):
        msm.convert(source, to_form=tmp_path / "not_supported.h5msm", strict=True)


def test_rich_h5msm_selection_uses_original_coordinates(tmp_path):
    source = prepared()
    source.molecular_mechanics.atom_ff_type = None
    path = tmp_path / "coordinates.h5msm"
    msm.convert(source, to_form=path)
    result = msm.physchem.get_partial_charges(
        path,
        method="gasteiger_marsili",
        selection='atom_type=="O" within 6 angstroms of atom_index==0',
        return_report=True,
    )
    assert result["report"]["atom_indices"].tolist() == [1]


def test_numeric_h5msm_selection_needs_no_coordinate_array(tmp_path, monkeypatch):
    h5py = pytest.importorskip("h5py")
    source = prepared()
    source.molecular_mechanics.atom_ff_type = None
    path = tmp_path / "no_coordinate_load.h5msm"
    msm.convert(source, to_form=path)
    original = h5py.Dataset.__getitem__

    def forbid_coordinates(dataset, key):
        if dataset.name.endswith("/coordinates"):
            raise AssertionError("Graph charges must not load coordinate arrays.")
        return original(dataset, key)

    monkeypatch.setattr(h5py.Dataset, "__getitem__", forbid_coordinates)
    result = msm.physchem.get_partial_charges(
        path, method="gasteiger_marsili", selection=[0]
    )
    assert result.shape == (1,)


def test_real_conventional_protein_charge_assignment_and_pdbqt_rounding(tmp_path):
    pytest.importorskip("openmm")
    source = msm.convert(
        msm.systems["chicken villin HP35"]["1vii.pdb"], to_form="molsysmt.MolSys"
    )
    groups = source.topology.groups["group_name"].tolist()
    # Protonated Lys/Arg and deprotonated Asp/Glu; the two termini cancel.
    declared_total = sum(
        groups.count(name) * charge
        for name, charge in [("LYS", 1), ("ARG", 1), ("ASP", -1), ("GLU", -1)]
    )
    assert declared_total == 2
    output = msm.build.assign_partial_charges(
        source,
        method="forcefield",
        forcefield="AMBER14",
        expected_total_charge=declared_total,
    )
    values = np.asarray(output.molecular_mechanics.partial_charge, dtype=float)
    assert len(values) == 596
    assert np.isfinite(values).all()
    assert values.sum() == pytest.approx(2, abs=1e-8)
    assert source.molecular_mechanics.partial_charge is None
    report = output.molecular_mechanics.partial_charge_assignment
    assert report["coverage"] == "complete"
    assert len(report["parameters"]["matched_residue_templates"]) == len(groups)
    # Element-consistent labels isolate charge serialization here. This test
    # does not validate the chemical AutoDock typing tracked in #222.
    output.molecular_mechanics.atom_ff_type = output.topology.atoms[
        "atom_type"
    ].to_numpy()
    text = write(output, tmp_path / "protein.pdbqt")
    info = json.loads(
        text.splitlines()[0].removeprefix("REMARK MOLSYSMT_PARTIAL_CHARGES ")
    )
    assert info["method"] == "forcefield"
    assert info["source_coverage"] == "complete"
    assert info["software"]["openmm"] == report["software"]["openmm"]
    parsed = msm.get(tmp_path / "protein.pdbqt", element="atom", partial_charge=True)
    # Binary floating point adds a few ulps at decimal half-rounding ties.
    np.testing.assert_allclose(parsed, values, atol=0.0005 + 1e-12, rtol=0)
