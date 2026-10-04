"""Checking chemical AutoDock classes and detached full-graph evaluation."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError

Chem = pytest.importorskip("rdkit.Chem")


def classify(source, **kwargs):
    return msm.physchem.get_autodock_atom_types(
        source, typing_scheme="autodock4", **kwargs
    )


@pytest.mark.parametrize(
    "smiles,heavy_types",
    [
        ("CCO", ["C", "C", "OA"]),
        ("c1ccccc1", ["A"] * 6),
        ("c1ccncc1", ["A", "A", "A", "NA", "A", "A"]),
        ("c1cc[nH]c1", ["A", "A", "A", "N", "A"]),
        ("CN", ["C", "NA"]),
        ("C[NH3+]", ["C", "N"]),
        ("CC(=O)N", ["C", "C", "OA", "N"]),
        ("NC(=S)C", ["N", "C", "S", "C"]),
        ("Nc1ccccc1", ["N"] + ["A"] * 6),
        ("C=C(N)C", ["C", "C", "N", "C"]),
        ("CSC", ["C", "SA", "C"]),
        ("CS", ["C", "SA"]),
        ("CSSC", ["C", "SA", "SA", "C"]),
        ("c1ccsc1", ["A", "A", "A", "S", "A"]),
        ("CS(=O)(=O)C", ["C", "S", "OA", "OA", "C"]),
        ("C[S-]", ["C", "S"]),
        ("CC(=O)[O-]", ["C", "C", "OA", "OA"]),
        ("FC(Cl)(Br)I", ["F", "C", "Cl", "Br", "I"]),
    ],
)
def test_independent_chemical_environment_controls(smiles, heavy_types):
    molecule = Chem.AddHs(Chem.MolFromSmiles(smiles))
    result = classify(molecule, return_report=True)
    labels, report = result["atom_ff_type"], result["report"]
    assert labels.dtype == np.dtype("U2")
    assert labels.shape == (molecule.GetNumAtoms(),)
    assert labels[: len(heavy_types)].tolist() == heavy_types
    for atom in molecule.GetAtoms():
        if atom.GetAtomicNum() == 1:
            parent = atom.GetNeighbors()[0].GetSymbol()
            assert labels[atom.GetIdx()] == ("H" if parent == "C" else "HD")
    assert report["coverage"] == "complete"
    assert report["rule_version"] == "chemical_environment@1"
    assert len(report["rule_indices"]) == len(labels)
    assert report["software"]["rdkit"]
    assert any(x["roles"] == ["reference_implementation"] for x in report["references"])


def test_full_graph_before_selection_and_rule_precedence():
    source = Chem.AddHs(Chem.MolFromSmiles("Nc1ccccc1"))
    result = classify(source, selection=[0, 0], return_report=True)
    assert result["atom_ff_type"].tolist() == ["N"]
    assert result["report"]["atom_indices"].tolist() == [0]
    assert result["report"]["evaluated_atom_indices"].tolist() == list(range(14))
    # The broad default and two specific conjugation rules overlap. The later
    # specific rule wins, instead of silently treating overlap as ambiguity.
    assert result["report"]["rule_indices"].tolist() == [3]
    assert result["report"]["n_matching_rules"].tolist() == [3]


def test_forms_unknown_aromatic_flags_and_atom_names_do_not_change_types(tmp_path):
    path = msm.systems["caffeine"]["caffeine.sdf"]
    source = msm.convert(path, to_form="molsysmt.MolSys")
    before = source.chemical_states._states[0].atom_attributes.copy()
    expected = classify(path)
    source.topology.atoms["atom_name"] = "misleading_nitrogen"
    h5 = tmp_path / "chemistry.h5msm"
    msm.convert(source, to_form=h5)
    for item in (source, source.topology, h5):
        np.testing.assert_array_equal(classify(item), expected)
    pd.testing.assert_frame_equal(
        source.chemical_states._states[0].atom_attributes, before
    )
    result = classify(source, selection=[5, 0, 5], return_report=True)
    np.testing.assert_array_equal(result["atom_ff_type"], expected[[0, 5]])
    assert result["report"]["atom_indices"].tolist() == [0, 5]


def test_empty_selection_and_graph_have_typed_empty_results():
    for item, selection in [
        (Chem.AddHs(Chem.MolFromSmiles("CO")), []),
        (Chem.Mol(), "all"),
    ]:
        result = classify(item, selection=selection, return_report=True)
        assert result["atom_ff_type"].shape == (0,)
        assert result["atom_ff_type"].dtype == np.dtype("U2")
        assert result["report"]["atom_indices"].dtype == np.int64
        assert result["report"]["rule_indices"].shape == (0,)


@pytest.mark.parametrize("smiles", ["[Na+]", "B", "[CH3]", "[C-]#N", "C[O+]C"])
def test_unqualified_chemistry_fails_explicitly(smiles):
    with pytest.raises(StructuralInconsistencyError):
        classify(Chem.AddHs(Chem.MolFromSmiles(smiles)))


def test_query_and_virtual_hydrogens_are_not_silently_prepared():
    with pytest.raises(StructuralInconsistencyError, match="query"):
        classify(Chem.MolFromSmarts("[C]"))
    with pytest.raises(StructuralInconsistencyError, match="hydrogen"):
        classify(Chem.MolFromSmiles("CO"))


@pytest.mark.parametrize(
    "missing", ["formal_charge", "n_unpaired_electrons", "bond_order", "connectivity"]
)
def test_missing_prerequisite_is_not_guessed(missing):
    source = msm.convert(
        Chem.AddHs(Chem.MolFromSmiles("CO")), to_form="molsysmt.MolSys"
    )
    state = source.chemical_states._states[0]
    if missing == "connectivity":
        state.connectivity_completeness = "partial"
    elif missing == "bond_order":
        state.bonds[missing] = pd.NA
    else:
        state.atom_attributes[missing] = pd.NA
    with pytest.raises(StructuralInconsistencyError):
        classify(source)


def test_contradictory_aromaticity_is_not_overwritten():
    source = msm.convert(
        Chem.AddHs(Chem.MolFromSmiles("c1ccccc1")), to_form="molsysmt.MolSys"
    )
    source.chemical_states._states[0].atom_attributes["is_aromatic"] = False
    with pytest.raises(StructuralInconsistencyError, match="conflicts"):
        classify(source)


def test_source_rdkit_and_rich_selection_are_read_only():
    source = Chem.AddHs(Chem.MolFromSmiles("CO"))
    before = Chem.MolToMolBlock(source)
    props = [list(atom.GetPropNames(includePrivate=True)) for atom in source.GetAtoms()]
    result = classify(source, selection="atom_type=='O'", return_report=True)
    assert result["atom_ff_type"].tolist() == ["OA"]
    assert result["report"]["atom_indices"].tolist() == [1]
    assert Chem.MolToMolBlock(source) == before
    assert [
        list(atom.GetPropNames(includePrivate=True)) for atom in source.GetAtoms()
    ] == props


def test_explicit_state_frames_scheme_and_method_validation():
    source = Chem.AddHs(Chem.MolFromSmiles("CO"))
    source.AddConformer(Chem.Conformer(source.GetNumAtoms()))
    assert classify(source, structure_indices=[0]).shape == (6,)
    with pytest.raises(ArgumentError):
        classify(source, structure_indices=[1])
    with pytest.raises(ArgumentError):
        classify(source, method="guess")
    with pytest.raises(ArgumentError):
        msm.physchem.get_autodock_atom_types(source, typing_scheme="guess")
    native = msm.convert(source, to_form="molsysmt.MolSys")
    second = native.chemical_states._states[0].copy()
    second.state_id = "selected"
    native.chemical_states._states.append(second)
    result = classify(native, chemical_state=1, return_report=True)
    assert result["report"]["chemical_state_id"] == "selected"
    assert result["report"]["chemical_state_index"] == 1
    assert native.chemical_states._reference_index == 0


def test_optional_attribution_failure_preserves_completed_typing(monkeypatch):
    import warnings

    from molsysmt import _ackredit

    def broken():
        raise ImportError("test attribution provider failure")

    monkeypatch.setattr(_ackredit, "backend", broken)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        result = classify(Chem.AddHs(Chem.MolFromSmiles("CC(=O)N")), return_report=True)
    assert result["atom_ff_type"][:4].tolist() == ["C", "C", "OA", "N"]
    assert result["report"]["references"]
    assert result["report"]["software"]["rdkit"]
