"""Checking named charge models against chemistry and pinned numerical controls."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

Chem = pytest.importorskip("rdkit.Chem")
puw = msm.pyunitwizard


def molecule(smiles):
    return Chem.AddHs(Chem.MolFromSmiles(smiles))


def calculate(source, **kwargs):
    return msm.physchem.get_partial_charges(
        source, method="gasteiger_marsili", return_report=True, **kwargs
    )


@pytest.mark.parametrize(
    "smiles,total",
    [
        ("CO", 0),
        ("[NH4+]", 1),
        ("C(=O)[O-]", -1),
        ("c1ccccc1", 0),
        ("CP(=O)(O)O", 0),
        ("CS", 0),
    ],
)
def test_full_charge_conservation_sign_symmetry_and_provider_independence(
    smiles, total
):
    source = molecule(smiles)
    before = Chem.MolToMolBlock(source)
    result = calculate(source)
    values = puw.get_value(result["partial_charge"], to_unit="elementary_charge")
    assert values.shape == (source.GetNumAtoms(),)
    assert np.isfinite(values).all()
    assert values.sum() == pytest.approx(total, abs=1e-10)
    assert Chem.MolToMolBlock(source) == before
    assert not any(atom.HasProp("_GasteigerCharge") for atom in source.GetAtoms())
    report = result["report"]
    assert report["method"] == "gasteiger_marsili"
    assert report["engine"] == "RDKit"
    assert report["coverage"] == "complete"
    assert report["parameters"]["iterations"] == 12
    assert report["software"]["rdkit"]
    assert report["references"][0]["doi"] == "10.1016/0040-4020(80)80168-2"
    if smiles == "[NH4+]":
        assert values[0] < 0
        assert values[1:].min() > 0
        np.testing.assert_allclose(values[1:], values[1])
    elif smiles == "c1ccccc1":
        assert values[:6].max() < 0
        np.testing.assert_allclose(values[:6], values[0])
        np.testing.assert_allclose(values[6:], -values[0])
    elif smiles == "C(=O)[O-]":
        assert values[0] > 0
        assert values[1] < 0
        assert values[1] == pytest.approx(values[2])


@pytest.mark.parametrize(
    "smiles,expected",
    [
        ("CO", [0.0319, -0.3996]),
        ("CS", [-0.0215, -0.1828]),
        ("CC#N", [0.0236, 0.0587, -0.1987]),
        ("CC(=O)N", [0.0146, 0.2138, -0.2757, -0.3699]),
    ],
)
def test_pinned_rdkit_halgren_regression_controls(smiles, expected):
    # Published RDKit halgren_out.txt controls, inspected at the local source.
    # These test reproduction of the named provider, not electrostatic accuracy.
    result = calculate(molecule(smiles))
    values = puw.get_value(result["partial_charge"], to_unit="elementary_charge")
    np.testing.assert_allclose(values[: len(expected)], expected, atol=5e-5, rtol=0)


def test_selection_is_after_full_graph_and_respects_charge_unit_configuration():
    source = molecule("CO")
    full = calculate(source)
    with puw.context(standard_units=["coulomb", "angstrom", "fs"]):
        subset = calculate(
            source,
            selection=[3, 0, 3],
            expected_total_charge=puw.quantity(0.0, "coulomb"),
        )
        assert puw.get_unit(subset["partial_charge"]) == puw.unit("coulomb")
    np.testing.assert_allclose(
        puw.get_value(subset["partial_charge"], to_unit="elementary_charge"),
        puw.get_value(full["partial_charge"], to_unit="elementary_charge")[[0, 3]],
    )
    assert subset["report"]["atom_indices"].tolist() == [0, 3]
    assert subset["report"]["evaluated_atom_indices"].tolist() == list(
        range(source.GetNumAtoms())
    )
    empty = calculate(source, selection=[])
    assert empty["partial_charge"].shape == (0,)
    assert empty["report"]["coverage"] == "complete"


def test_quantity_getter_requires_a_charge_standard_without_changing_policy():
    source = molecule("CO")
    before = Chem.MolToMolBlock(source)
    with puw.context(standard_units=["pm", "fs"]):
        policy = puw.configure.report()
        with pytest.raises(Exception) as caught:
            calculate(source)
        # PyUnitWizard does not export this exception at its public root.
        assert type(caught.value).__name__ == "NoStandardsError"
        assert puw.configure.report() == policy
    assert Chem.MolToMolBlock(source) == before
    assert not any(atom.HasProp("_GasteigerCharge") for atom in source.GetAtoms())


def test_supported_forms_and_nonreference_state_are_equivalent(tmp_path):
    source = msm.convert(molecule("CO"), to_form="molsysmt.MolSys")
    second = source.chemical_states._states[0].copy()
    second.state_id = "second"
    source.chemical_states._states.append(second)
    report = calculate(source, chemical_state=1)["report"]
    assert report["chemical_state_index"] == 1
    assert report["chemical_state_id"] == "second"
    assert source.chemical_states._reference_index == 0
    path = tmp_path / "chemistry.h5msm"
    msm.convert(source, to_form=path)
    for item in [source, source.topology, str(path)]:
        np.testing.assert_allclose(
            puw.get_value(calculate(item, chemical_state=1)["partial_charge"]),
            puw.get_value(calculate(source)["partial_charge"]),
        )
    caffeine = calculate(msm.systems["caffeine"]["caffeine.sdf"])
    assert caffeine["partial_charge"].shape == (24,)


@pytest.mark.parametrize(
    "smiles,reason",
    [("CO", "hydrogens"), ("[Na+]", "metals"), ("[CH3]", "radical"), ("*", "element")],
)
def test_unsupported_input_fails_without_source_changes(smiles, reason):
    source = Chem.MolFromSmiles(smiles)
    before = Chem.MolToMolBlock(source)
    with pytest.raises(StructuralInconsistencyError, match=reason):
        calculate(source)
    assert Chem.MolToMolBlock(source) == before


@pytest.mark.parametrize("field", ["formal_charge", "n_unpaired_electrons"])
def test_unknown_required_chemistry_is_not_filled(field):
    source = msm.convert(molecule("CO"), to_form="molsysmt.MolSys")
    source.chemical_states._states[0].atom_attributes.loc[0, field] = pd.NA
    with pytest.raises(StructuralInconsistencyError):
        calculate(source)


@pytest.mark.parametrize(
    "failure", ["missing", "nonfinite", "total", "virtual_hydrogen"]
)
def test_model_failures_are_not_masked_or_renormalized(monkeypatch, failure):
    from rdkit.Chem import rdPartialCharges

    def bad_calculation(mol, **kwargs):
        for index, atom in enumerate(mol.GetAtoms()):
            if failure != "missing" or index:
                atom.SetDoubleProp(
                    "_GasteigerCharge", float("nan") if failure == "nonfinite" else 0.5
                )
            atom.SetDoubleProp(
                "_GasteigerHCharge", 0.1 if failure == "virtual_hydrogen" else 0.0
            )

    monkeypatch.setattr(rdPartialCharges, "ComputeGasteigerCharges", bad_calculation)
    with pytest.raises(StructuralInconsistencyError):
        calculate(molecule("CO"))


@pytest.mark.parametrize(
    "kwargs",
    [
        {"method": "rdkit"},
        {"method": "forcefield"},
        {"method": "gasteiger_marsili", "forcefield": "AMBER14"},
        {"method": "gasteiger_marsili", "expected_total_charge": 0.0},
        {"method": "gasteiger_marsili", "expected_total_charge": True},
        {"method": "gasteiger_marsili", "expected_total_charge": puw.quantity(0, "nm")},
    ],
)
def test_invalid_model_and_declaration_arguments(kwargs):
    with pytest.raises(ArgumentError):
        msm.physchem.get_partial_charges(molecule("CO"), **kwargs)


def test_declared_total_conflict_is_explicit():
    with pytest.raises(StructuralInconsistencyError, match="conflicts"):
        calculate(molecule("CO"), expected_total_charge=1)


def test_forcefield_alanine_sequence_has_independent_template_charges():
    pytest.importorskip("openmm")
    source = "molsysmt/data/pdb/ala3.pdb"
    result = msm.physchem.get_partial_charges(
        source,
        method="forcefield",
        forcefield="AMBER14",
        expected_total_charge=0,
        return_report=True,
    )
    values = puw.get_value(result["partial_charge"], to_unit="elementary_charge")
    # ff14SB's internal ALA charges (OpenMM protein.ff14SB.xml), not values
    # obtained by running createSystem again inside this test.
    atom_names = msm.get(source, element="atom", atom_name=True)
    group_indices = msm.get(source, element="atom", group_index=True)
    actual = {
        name: values[i]
        for i, (name, group) in enumerate(zip(atom_names, group_indices))
        if group == 1
    }
    assert actual["N"] == pytest.approx(-0.4157)
    assert actual["H"] == pytest.approx(0.2719)
    assert actual["CA"] == pytest.approx(0.0337)
    assert actual["CB"] == pytest.approx(-0.1825)
    assert actual["C"] == pytest.approx(0.5973)
    assert actual["O"] == pytest.approx(-0.5679)
    assert values.sum() == pytest.approx(0, abs=1e-8)
    assert result["report"]["parameters"]["forcefield_files"] == ["amber14-all.xml"]
    assert result["report"]["software"]["openmm"]


def test_previous_partial_charges_are_not_reused_by_the_named_model():
    source = msm.convert(molecule("CO"), to_form="molsysmt.MolSys")
    expected = calculate(source)["partial_charge"]
    source.molecular_mechanics.partial_charge = np.full(source.get_n_atoms(), 9.0)
    np.testing.assert_allclose(
        puw.get_value(calculate(source)["partial_charge"]), puw.get_value(expected)
    )
    np.testing.assert_array_equal(
        source.molecular_mechanics.partial_charge, [9.0] * source.get_n_atoms()
    )


@pytest.mark.parametrize(
    "function", [msm.physchem.get_partial_charges, msm.build.assign_partial_charges]
)
def test_only_boolean_skip_digestion_is_accepted(function):
    with pytest.raises(ArgumentError, match="skip_digestion"):
        function(molecule("CO"), method="gasteiger_marsili", skip_digestion=1)


def test_invalid_frame_indices_are_not_ignored():
    with pytest.raises(ArgumentError, match="structure_indices"):
        calculate(molecule("CO"), structure_indices=[9])


def test_rdkit_conformer_indices_can_resolve_through_native_conversion():
    source = molecule("CO")
    source.AddConformer(Chem.Conformer(source.GetNumAtoms()))
    result = calculate(source, structure_indices=[0])
    assert result["partial_charge"].shape == (6,)
    with pytest.raises(ArgumentError):
        calculate(source, structure_indices=[1])


def test_incomplete_connectivity_and_missing_orders_are_rejected():
    source = msm.convert(molecule("CO"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    state.connectivity_completeness = "partial"
    with pytest.raises(StructuralInconsistencyError, match="complete"):
        calculate(source)
    state.connectivity_completeness = "complete"
    state.bonds.loc[0, "bond_order"] = pd.NA
    with pytest.raises(StructuralInconsistencyError, match="bond orders"):
        calculate(source)


def test_forcefield_unknown_total_and_unmatched_chemistry_fail():
    pytest.importorskip("openmm")
    with pytest.raises(StructuralInconsistencyError, match="unknown"):
        msm.physchem.get_partial_charges(
            "molsysmt/data/pdb/ala3.pdb", method="forcefield", forcefield="AMBER14"
        )
    with pytest.raises(StructuralInconsistencyError, match="template"):
        msm.physchem.get_partial_charges(
            molecule("CO"), method="forcefield", forcefield="AMBER14"
        )
