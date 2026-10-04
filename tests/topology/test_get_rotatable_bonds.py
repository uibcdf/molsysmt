"""Checking named torsion criteria, source axes and original-graph context."""

import copy
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import Structures, Topology

Chem = pytest.importorskip("rdkit.Chem")


@pytest.mark.parametrize(
    "smiles,base,restricted",
    [
        ("CCCC", [[1, 2]], [[1, 2]]),
        ("CCC", [], []),
        ("C1CCCCC1", [], []),
        ("CC=CC", [], []),
        ("CC#CC", [], []),
        ("CC(=O)NCC", [[1, 3], [3, 4]], [[3, 4]]),
        ("CC(=S)NCC", [[1, 3], [3, 4]], [[3, 4]]),
        ("CC(=N)NCC", [[1, 3], [3, 4]], [[3, 4]]),
        ("CC(=O)OCC", [[1, 3], [3, 4]], [[3, 4]]),
        ("CC(=O)SCC", [[1, 3], [3, 4]], [[3, 4]]),
        ("O=CNCC", [[1, 2], [2, 3]], [[2, 3]]),
        ("CC(=O)N(C)CC", [[1, 3], [3, 5]], [[3, 5]]),
        ("CCSCC", [[1, 2], [2, 3]], [[1, 2], [2, 3]]),
        ("CC.CCCC", [[3, 4]], [[3, 4]]),
    ],
)
def test_independently_specified_chemical_pairs_and_exclusions(
    smiles, base, restricted
):
    source = Chem.MolFromSmiles(smiles)
    before = Chem.MolToMolBlock(source)
    for method, expected in [
        ("acyclic_single", base),
        ("conjugation_restricted", restricted),
    ]:
        result = msm.topology.get_rotatable_bonds(source, method=method)
        assert result["rotatable_bonded_atom_pairs"].tolist() == expected
        assert result["is_rotatable"].dtype == np.bool_
        assert result["exclusion_mask"].dtype == np.uint8
        np.testing.assert_array_equal(
            result["is_rotatable"], result["exclusion_mask"] == 0
        )
        assert result["rule_version"] == method + "@1"
        assert result["software"]["networkx"]
        fragments = msm.topology.get_rigid_fragments(
            source, bond_indices=result["rotatable_bond_indices"]
        )
        np.testing.assert_array_equal(
            fragments["bonded_atom_pairs"],
            expected if expected else np.empty((0, 2), dtype=int),
        )
    assert Chem.MolToMolBlock(source) == before


def test_aromatic_links_nitrile_and_all_overlapping_exclusions():
    biphenyl = Chem.MolFromSmiles("c1ccccc1-c1ccccc1")
    result = msm.topology.get_rotatable_bonds(biphenyl)
    assert result["rotatable_bonded_atom_pairs"].tolist() == [[5, 6]]
    nitrile = msm.topology.get_rotatable_bonds(Chem.MolFromSmiles("c1ccccc1C#N"))
    bits = nitrile["exclusion_bits"]
    assert not nitrile["is_rotatable"].any()
    assert nitrile["exclusion_mask"][6] & bits["adjacent_triple_bond"]
    assert nitrile["exclusion_mask"][7] & bits["not_single"]
    assert nitrile["exclusion_mask"][7] & bits["terminal_heavy_atom"]
    ester = msm.topology.get_rotatable_bonds(Chem.MolFromSmiles("CC(=O)OCC"))
    assert ester["exclusion_mask"][2] == bits["restricted_conjugation"]


def test_native_graph_does_not_require_aromaticity_charge_or_a_provider(
    tmp_path, monkeypatch
):
    source = msm.convert(Chem.MolFromSmiles("CCCC"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    state.bonds["is_aromatic"] = pd.NA
    state.atom_attributes["is_aromatic"] = pd.NA
    state.atom_attributes["formal_charge"] = pd.NA
    source.topology.atoms["atom_id"] = pd.array(
        ["70", "20", "10", "40"], dtype="string"
    )
    state.bonds["bond_id"] = pd.array(["9", "2", "6"], dtype="string")
    before = source.copy()
    path = tmp_path / "native.h5msm"
    msm.convert(source, to_form=path)

    def forbidden(*args, **kwargs):
        raise AssertionError(
            "The native torsion classifier must not call RDKit or aromaticity perception."
        )

    monkeypatch.setattr(msm.physchem, "get_aromaticity", forbidden)
    monkeypatch.setattr(Chem, "SetAromaticity", forbidden)
    for item in [source, source.topology, str(path)]:
        result = msm.topology.get_rotatable_bonds(item)
        assert result["rotatable_bond_indices"].tolist() == [1]
        assert result["rotatable_bonded_atom_pairs"].tolist() == [[1, 2]]
        assert result["evaluated_atom_indices"].tolist() == [0, 1, 2, 3]
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(state.bonds, before.chemical_states._states[0].bonds)


def test_full_graph_classification_precedes_selection_and_h_materialization():
    source = Chem.MolFromSmiles("CC(=O)OCC")
    full = msm.topology.get_rotatable_bonds(source)
    selected = msm.topology.get_rotatable_bonds(source, selection=[4, 3, 4])
    assert selected["rotatable_bonded_atom_pairs"].tolist() == [[3, 4]]
    assert selected["atom_indices"].tolist() == [3, 4]
    assert len(selected["evaluated_atom_indices"]) == 6
    explicit = msm.topology.get_rotatable_bonds(Chem.AddHs(source))
    np.testing.assert_array_equal(
        explicit["rotatable_bonded_atom_pairs"], full["rotatable_bonded_atom_pairs"]
    )
    assert not msm.topology.get_rotatable_bonds(source, selection=[1, 3])[
        "is_rotatable"
    ].any()
    assert not msm.topology.get_rotatable_bonds(source, selection=[3])[
        "is_rotatable"
    ].any()


def test_reordered_bond_axis_disconnected_inventory_and_isolates():
    source = msm.convert(Chem.MolFromSmiles("CCCC.[Cl-]"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    state.bonds = state.bonds.iloc[[1, 2, 0]].reset_index(drop=True)
    result = msm.topology.get_rotatable_bonds(source)
    assert result["rotatable_bond_indices"].tolist() == [0]
    assert result["rotatable_bonded_atom_pairs"].tolist() == [[1, 2]]
    fragments = msm.topology.get_rigid_fragments(source, bond_indices=[0])
    assert fragments["fragment_offsets"].tolist() == [0, 2, 4, 5]


@pytest.mark.parametrize(
    "defect", ["partial", "order", "dative", "element", "aromatic_bridge"]
)
def test_missing_or_unsupported_evidence_fails_before_selection(defect):
    source = msm.convert(Chem.MolFromSmiles("CCCC"), to_form="molsysmt.MolSys")
    state = source.chemical_states._states[0]
    if defect == "partial":
        state.connectivity_completeness = "partial"
    elif defect == "order":
        state.bonds.loc[0, "bond_order"] = pd.NA
        state.bonds.loc[0, "is_aromatic"] = pd.NA
    elif defect == "dative":
        state.bonds.loc[0, "bond_type"] = "dative"
    elif defect == "element":
        source.topology.atoms.loc[0, "atom_type"] = "Zn"
    else:
        state.bonds.loc[1, "is_aromatic"] = True
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_rotatable_bonds(source, selection=[])


def test_typed_empty_results_invalid_inputs_and_query_rejection():
    result = msm.topology.get_rotatable_bonds(Topology(n_atoms=0))
    for key in ["bond_indices", "rotatable_bond_indices", "evaluated_atom_indices"]:
        assert result[key].shape == (0,) and result[key].dtype == np.int64
    assert (
        result["bonded_atom_pairs"].shape
        == result["rotatable_bonded_atom_pairs"].shape
        == (0, 2)
    )
    empty = msm.topology.get_rotatable_bonds(Chem.MolFromSmiles("CCCC"), selection=[])
    assert empty["is_rotatable"].shape == (0,)
    assert len(empty["evaluated_atom_indices"]) == 4
    for kwargs in [
        dict(method="guess"),
        dict(selection=[-1]),
        dict(selection=[4]),
        dict(structure_indices=[0]),
        dict(chemical_state=1),
    ]:
        with pytest.raises((ArgumentError, StructuralInconsistencyError)):
            msm.topology.get_rotatable_bonds(Chem.MolFromSmiles("CCCC"), **kwargs)
    with pytest.raises(StructuralInconsistencyError, match="quer"):
        msm.topology.get_rotatable_bonds(Chem.MolFromSmarts("C-C"))


def test_assigned_state_and_spatial_selection_resolve_before_detaching():
    source = msm.convert(Chem.MolFromSmiles("CCCC"), to_form="molsysmt.MolSys")
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 4, 3)), "nm")
    )
    second = source.chemical_states._states[0].copy()
    second.state_id = "restricted"
    second.bonds.loc[1, "bond_order"] = 2
    source.chemical_states._states.append(second)
    source._set_structure_chemical_state_indices([0, 1])
    first = msm.topology.get_rotatable_bonds(
        source, chemical_state="structure", structure_indices=[0]
    )
    assert first["rotatable_bond_indices"].tolist() == [1]
    second_result = msm.topology.get_rotatable_bonds(
        source,
        chemical_state="structure",
        structure_indices=[1],
        selection="atom_type == 'C'",
    )
    assert second_result["chemical_state_index"] == 1
    assert not second_result["is_rotatable"].any()
    assert source.chemical_states._reference_index == 0
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_rotatable_bonds(
            source, chemical_state="structure", structure_indices=[0, 1]
        )


def test_optional_attribution_failure_preserves_classification(monkeypatch):
    source = Chem.MolFromSmiles("CCCC")
    from molsysmt import _ackredit

    baseline = msm.topology.get_rotatable_bonds(source)
    monkeypatch.setattr(_ackredit, "backend", lambda: None)
    disabled = msm.topology.get_rotatable_bonds(source)
    np.testing.assert_array_equal(disabled["is_rotatable"], baseline["is_rotatable"])
    assert copy.deepcopy(disabled["attribution"]) == baseline["attribution"]

    def unavailable():
        raise RuntimeError("attribution provider failed")

    monkeypatch.setattr(_ackredit, "backend", unavailable)
    with pytest.warns(Warning, match="attribution"):
        failed_tracking = msm.topology.get_rotatable_bonds(source)
    np.testing.assert_array_equal(
        failed_tracking["is_rotatable"], baseline["is_rotatable"]
    )


def test_known_strict_descriptor_differences_are_not_hidden():
    descriptors = pytest.importorskip("rdkit.Chem.rdMolDescriptors")
    source = Chem.MolFromSmiles("CC(C)(C)CC")
    result = msm.topology.get_rotatable_bonds(source)
    assert result["rotatable_bonded_atom_pairs"].tolist() == [[1, 4]]
    assert (
        descriptors.CalcNumRotatableBonds(
            source, descriptors.NumRotatableBondsOptions.Strict
        )
        == 0
    )


def test_native_classification_in_a_process_without_rdkit_or_meeko():
    script = """
import builtins
import sys
original_import = builtins.__import__
def guarded_import(name, *args, **kwargs):
    if name.split('.')[0] in {'rdkit', 'meeko'}:
        raise AssertionError('unexpected optional torsion provider import: ' + name)
    return original_import(name, *args, **kwargs)
builtins.__import__ = guarded_import
import pandas as pd
import molsysmt as msm
from molsysmt.native import Topology
source = Topology(n_atoms=4)
source.atoms['atom_type'] = pd.array(['C'] * 4, dtype='string')
source.bonds = pd.DataFrame({'atom1_index': [0, 1, 2], 'atom2_index': [1, 2, 3],
    'bond_type': ['covalent'] * 3, 'bond_order': [1, 1, 1]})
source._chemical_states[0].connectivity_completeness = 'complete'
result = msm.topology.get_rotatable_bonds(source)
assert result['rotatable_bonded_atom_pairs'].tolist() == [[1, 2]]
assert 'rdkit' not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", script], capture_output=True, text=True, timeout=60
    )
    assert result.returncode == 0, result.stdout + result.stderr
