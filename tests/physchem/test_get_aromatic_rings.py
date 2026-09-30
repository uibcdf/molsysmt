"""Checking explicit aromatic participants independently of geometric detection."""

from importlib.util import find_spec

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures, Topology


def _ring(aromatic=True):
    molsys = Topology(n_atoms=6)
    molsys.bonds = pd.DataFrame({
        "atom1_index": np.arange(6), "atom2_index": np.roll(np.arange(6), -1),
        "bond_type": ["covalent"] * 6, "is_aromatic": [aromatic] * 6,
    })
    molsys._set_chemical_state_atom_attribute("is_aromatic", [aromatic] * 6)
    molsys._reference_chemical_state.connectivity_completeness = "complete"
    return molsys


def _memberships(result):
    return {tuple(result["atom_indices"][a:b]) for a, b in zip(
        result["atom_offsets"][:-1], result["atom_offsets"][1:],
    )}


@pytest.mark.parametrize("aromatic", [True, False])
def test_declared_aromaticity_is_distinct_from_connectivity(aromatic):
    molsys = _ring(aromatic)
    before = molsys.bonds.copy(deep=True)
    result = msm.physchem.get_aromatic_rings(molsys)
    assert len(_memberships(result)) == int(aromatic)
    assert len(msm.topology.get_rings(molsys)["atom_offsets"]) == 2
    assert result["definition"] == "stored_aromatic_bonds"
    assert result["rule_version"] == "stored_aromatic_bond_cycles@1"
    assert result["evidence"]["kind"] == "chemical_states.is_aromatic"
    assert result["software"]["molsysmt"] == msm.__version__
    pd.testing.assert_frame_equal(molsys.bonds, before)


@pytest.mark.parametrize("defect", ["atom_unknown", "bond_unknown", "atom_false", "bond_false", "aromatic_dative", "acyclic_atom"])
def test_missing_or_contradictory_aromatic_metadata_fails_before_selection(defect):
    molsys = _ring()
    if defect.startswith("atom"):
        molsys._reference_chemical_state.atom_attributes.loc[0, "is_aromatic"] = pd.NA if defect.endswith("unknown") else False
    elif defect.startswith("bond"):
        molsys.bonds.loc[0, "is_aromatic"] = pd.NA if defect.endswith("unknown") else False
    elif defect == "aromatic_dative":
        molsys.bonds.loc[0, "bond_type"] = "dative"
    else:
        molsys = Topology(n_atoms=1)
        molsys._set_chemical_state_atom_attribute("is_aromatic", [True])
        molsys._reference_chemical_state.connectivity_completeness = "complete"
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_aromatic_rings(molsys, selection=[])


def test_whole_ring_selections_and_empty_scope():
    molsys = _ring()
    with pytest.raises(ArgumentError, match="cuts a perceived ring"):
        msm.physchem.get_aromatic_rings(molsys, selection=[0])
    selected = msm.physchem.get_aromatic_rings(molsys, selection=[5, 4, 3, 2, 1, 0, 0])
    assert selected["atom_indices"].tolist() == list(range(6))
    empty = msm.physchem.get_aromatic_rings(molsys, selection=[])
    assert empty["atom_indices"].dtype == np.int64
    assert empty["atom_offsets"].tolist() == [0]
    assert empty["examined_atom_indices"].tolist() == list(range(6))


def test_aromatic_bond_subgraph_keeps_a_fused_perimeter_with_nonaromatic_fusion_bond():
    molsys = _ring()
    molsys.bonds = pd.concat([molsys.bonds, pd.DataFrame({
        "atom1_index": [0], "atom2_index": [3], "bond_type": ["covalent"],
        "is_aromatic": [False],
    })], ignore_index=True)
    assert _memberships(msm.topology.get_rings(molsys)) == {(0, 1, 2, 3), (0, 3, 4, 5)}
    assert _memberships(msm.physchem.get_aromatic_rings(molsys)) == {tuple(range(6))}


def test_nonreference_aromatic_state_and_reference_are_independent():
    molsys = _ring()
    second = molsys._append_chemical_state(state_id="nonaromatic")
    molsys._chemical_states[second].bonds = molsys.bonds.copy(deep=True)
    molsys._chemical_states[second].bonds["is_aromatic"] = False
    molsys._set_chemical_state_atom_attribute("is_aromatic", [False] * 6, state_index=second)
    molsys._chemical_states[second].connectivity_completeness = "complete"
    assert not _memberships(msm.physchem.get_aromatic_rings(molsys, chemical_state=second))
    assert len(_memberships(msm.physchem.get_aromatic_rings(molsys))) == 1
    assert molsys._reference_chemical_state_index == 0


def test_h5msm05_reads_chemistry_without_coordinates_or_interactions(tmp_path, monkeypatch):
    import molsysmt.form._h5msm05_modular as modular

    molsys = MolSys()
    molsys.topology = _ring()
    molsys.structures.append(coordinates=puw.quantity(np.zeros((3, 6, 3)), "nm"))
    molsys.interactions = {"saved": msm.Interactions.from_records(
        [], n_atoms=6, n_structures=3, evaluated_structure_indices=[0, 1, 2], method="fixture",
    )}
    filename = str(tmp_path / "aromatic.h5msm")
    msm.convert(molsys, to_form=filename)

    def unexpected_full_load(*args, **kwargs):
        pytest.fail("Ring recognition must not materialize structures or saved analyses.")

    monkeypatch.setattr(modular, "read_molsys_file", unexpected_full_load)
    monkeypatch.setattr(modular, "read_independent_structures", unexpected_full_load)
    monkeypatch.setattr(modular, "read_named_analyses", unexpected_full_load)
    assert _memberships(msm.physchem.get_aromatic_rings(filename)) == {tuple(range(6))}
    assert _memberships(msm.topology.get_rings(filename)) == {tuple(range(6))}


@pytest.mark.parametrize("form", ["molsysmt.Topology", "molsysmt.MolSys", "molsysmt.ChemicalStates", "molsysmt.ChemicalStatesDict"])
def test_public_ring_tools_accept_native_and_dictionary_forms(form):
    source = msm.convert(_ring(), to_form=form)
    for tool in (msm.topology.get_rings, msm.physchem.get_aromatic_rings):
        result = tool(source, selection=[5, 4, 3, 2, 1, 0, 0])
        assert _memberships(result) == {tuple(range(6))}
        assert result["source_atom_indices"].tolist() == list(range(6))


@pytest.mark.parametrize("form", ["molsysmt.TopologyDict", "molsysmt.MolSysDict"])
def test_legacy_dictionary_forms_allow_declared_connectivity_but_do_not_supply_aromatic_flags(form):
    source = msm.convert(_ring(), to_form=form)
    assert _memberships(msm.topology.get_rings(source, assume_complete_connectivity=True)) == {tuple(range(6))}
    with pytest.raises(StructuralInconsistencyError, match="explicit is_aromatic flag"):
        msm.physchem.get_aromatic_rings(source, assume_complete_connectivity=True)


@pytest.mark.parametrize("file_source", [False, True])
@pytest.mark.parametrize("with_structures", [False, True])
def test_topology_free_chemistry_contains_the_information_needed_for_ring_memberships(file_source, with_structures, tmp_path):
    states = msm.convert(_ring(), to_form="molsysmt.ChemicalStates")
    molsys = MolSys._from_partial_domains(chemical_states=states)
    if with_structures:
        molsys.structures = Structures()
        molsys.structures.append(coordinates=puw.quantity(np.zeros((3, 6, 3)), "nm"))
    source = molsys
    if file_source:
        source = str(tmp_path / "chemistry_only.h5msm")
        msm.convert(molsys, to_form=source)
    for tool in (msm.topology.get_rings, msm.physchem.get_aromatic_rings):
        assert _memberships(tool(source)) == {tuple(range(6))}


@pytest.mark.parametrize("file_source", [False, True])
def test_structure_assigned_chemistry_uses_nonconsecutive_indices_not_structure_ids(file_source, tmp_path):
    molsys = MolSys()
    molsys.topology = _ring()
    molsys.structures.append(
        coordinates=puw.quantity(np.zeros((4, 6, 3)), "nm"), structure_id=[11, 70, 200, 201],
    )
    second = molsys.chemical_states.append_state()
    molsys.topology._chemical_states[second].bonds = molsys.topology.bonds.copy(deep=True)
    molsys.topology._chemical_states[second].bonds["is_aromatic"] = False
    molsys.topology._chemical_states[second].connectivity_completeness = "complete"
    msm.set(molsys, element="atom", atom_is_aromatic=[False] * 6, chemical_state=second)
    molsys._set_structure_chemical_state_indices([0, second, second, 0])
    source = molsys
    if file_source:
        source = str(tmp_path / "states.h5msm")
        msm.convert(molsys, to_form=source)
    result = msm.physchem.get_aromatic_rings(source, chemical_state="structure", structure_indices=[2, 1, 2])
    assert not _memberships(result)
    assert result["chemical_state_index"] == second
    assert len(_memberships(msm.topology.get_rings(source, chemical_state="structure", structure_indices=[2, 1]))) == 1
    assert len(_memberships(msm.physchem.get_aromatic_rings(source, chemical_state="structure", structure_indices=[3, 0]))) == 1
    with pytest.raises(StructuralInconsistencyError):
        msm.physchem.get_aromatic_rings(source, chemical_state="structure")


@pytest.mark.skipif(find_spec("mdtraj") is None, reason="MDTraj is an optional form provider.")
def test_connectivity_only_external_form_supports_rings_without_inventing_aromaticity():
    import mdtraj as md

    molsys = md.Topology()
    chain = molsys.add_chain()
    group = molsys.add_residue("LIG", chain)
    atoms = [molsys.add_atom(f"C{i}", md.element.carbon, group) for i in range(6)]
    for a, b in zip(atoms, atoms[1:] + atoms[:1]):
        molsys.add_bond(a, b)
    assert _memberships(msm.topology.get_rings(molsys)) == {tuple(range(6))}
    with pytest.raises(StructuralInconsistencyError, match="explicit is_aromatic flag"):
        msm.physchem.get_aromatic_rings(molsys)


@pytest.mark.parametrize("argument", [{"definition": "planarity"}, {"method": "sssr"}])
def test_unsupported_chemical_or_topological_method_raises(argument):
    with pytest.raises(ArgumentError):
        msm.physchem.get_aromatic_rings(_ring(), **argument)


@pytest.mark.skipif(find_spec("rdkit") is None, reason="RDKit provides optional independent ring fixtures.")
@pytest.mark.parametrize("smiles", ["c1ccccc1", "c1ccncc1", "c1ccc2ccccc2c1", "c1ccc2[nH]ccc2c1", "c1ccccc1-c2ccccc2", "C1CCCCC1", "C1=CC=CCC1"])
def test_declared_aromatic_memberships_match_independent_rdkit_simple_and_fused_fixtures(smiles):
    from rdkit import Chem

    original = Chem.MolFromSmiles(smiles)
    expected = set()
    for cycle in Chem.GetSymmSSSR(original):
        atoms = list(cycle)
        if all(original.GetBondBetweenAtoms(a, b).GetIsAromatic() for a, b in zip(atoms, atoms[1:] + atoms[:1])):
            expected.add(tuple(sorted(atoms)))
    result = msm.physchem.get_aromatic_rings(original)
    assert _memberships(result) == expected
    assert result["n_atoms"] == original.GetNumAtoms()
