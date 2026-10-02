"""Contract tests for the native chemical-state authority."""

import pickle

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import ChemicalStates, MolSys, Topology


def test_standalone_collection_has_explicit_empty_state():
    states = ChemicalStates(n_atoms=3)

    assert states.n_atoms == 3
    assert states.n_chemical_states == 0
    assert states.reference_chemical_state_index is None
    with pytest.raises(msm.StructuralInconsistencyError):
        states.get_bonds()

    assert states.append_state() == 0
    assert states.n_chemical_states == 1
    assert states.reference_chemical_state_index == 0
    assert states.get_bonds().empty
    assert states.append_state() == 1
    assert states.reference_chemical_state_index == 0


def test_molsys_and_topology_share_one_bond_authority():
    system = MolSys(n_atoms=3)
    system.topology.add_bonds([[0, 1]])

    assert system.chemical_states is system.topology._chemical_states_domain
    assert not hasattr(system.topology, "chemical_states")
    assert system.chemical_states.get_bonds() is system.topology.bonds
    system.topology.add_bonds([[1, 2]])
    assert len(system.chemical_states.get_bonds()) == 2
    assert msm.ChemicalStates is ChemicalStates


def test_topology_rejects_a_shadow_chemical_states_attribute():
    topology = Topology(n_atoms=2)
    bonds = topology.bonds

    assert not hasattr(topology, "chemical_states")
    with pytest.raises(AttributeError, match="MolSys.chemical_states"):
        topology.chemical_states = ChemicalStates(n_atoms=2)
    assert topology.bonds is bonds
    assert "chemical_states" not in vars(topology)


def test_copy_and_atom_extraction_do_not_share_state_storage():
    system = MolSys(n_atoms=3)
    system.topology.add_bonds([[0, 1], [1, 2]])

    copied = system.copy()
    assert copied.chemical_states is copied.topology._chemical_states_domain
    assert copied.chemical_states is not system.chemical_states
    copied.topology.add_bonds([[0, 2]])
    assert len(system.topology.bonds) == 2

    subset = system.extract(atom_indices=[1, 2], skip_digestion=True)
    assert subset.chemical_states is subset.topology._chemical_states_domain
    assert subset.chemical_states.n_atoms == 2
    assert subset.topology.bonds[["atom1_index", "atom2_index"]].iloc[0].tolist() == [
        0,
        1,
    ]


def test_replacement_rejects_a_different_atom_domain_without_mutation():
    system = MolSys(n_atoms=2)
    original = system.chemical_states

    with pytest.raises(msm.StructuralInconsistencyError, match="atom-index domain"):
        system.chemical_states = ChemicalStates(n_atoms=3)

    assert system.chemical_states is original
    assert system.topology._chemical_states_domain is original


def test_partial_replacement_rejects_an_attached_interaction_axis():
    states = ChemicalStates(n_atoms=3)
    analysis = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=0,
        evaluated_structure_indices=[],
        method="candidate",
    )
    system = MolSys._from_partial_domains(
        chemical_states=states, interactions={"candidate": analysis}
    )

    with pytest.raises(msm.StructuralInconsistencyError, match="interactions"):
        system.chemical_states = ChemicalStates(n_atoms=2)

    assert system.chemical_states is states
    assert system.interactions["candidate"] is analysis


def test_chemical_state_replacement_keeps_topology_bond_facade_current():
    system = MolSys(n_atoms=2)
    replacement = ChemicalStates(n_atoms=2)
    replacement.append_state()

    system.chemical_states = replacement

    assert system.chemical_states is replacement
    assert system._chemical_states_domain is replacement
    assert system.topology.bonds is replacement.get_bonds()


def test_molsys_replacement_detaches_old_topology_and_owns_new_states():
    system = MolSys(n_atoms=2)
    previous_topology = system.topology
    replacement_topology = Topology(n_atoms=2)
    replacement_topology.add_bonds([[0, 1]])

    system.topology = replacement_topology

    assert system.chemical_states is replacement_topology._chemical_states_domain
    assert (
        system._chemical_states_domain is replacement_topology._chemical_states_domain
    )
    previous_topology.add_bonds([[0, 1]])
    assert len(system.chemical_states.get_bonds()) == 1


def test_one_topology_cannot_own_two_molsys_state_domains():
    first = MolSys(n_atoms=2)
    second = MolSys(n_atoms=2)

    with pytest.raises(msm.StructuralInconsistencyError, match="already attached"):
        second.topology = first.topology

    assert second.chemical_states is second.topology._chemical_states_domain
    second.topology = first.topology.copy()
    assert second.chemical_states is not first.chemical_states


def test_reset_atoms_keeps_domain_aligned_and_rejects_data_loss():
    topology = Topology()
    states = topology._chemical_states_domain

    topology.reset_atoms(2)
    assert topology._chemical_states_domain is states
    assert states.n_atoms == 2
    assert len(states._states[0].atom_attributes) == 2

    topology.add_bonds([[0, 1]])
    with pytest.raises(msm.StructuralInconsistencyError, match="invalidate"):
        topology.reset_atoms(3)
    assert topology.n_atoms == states.n_atoms == 2
    assert len(topology.bonds) == 1


def test_topology_replacement_rejects_dangling_structure_state_indices():
    system = MolSys(n_atoms=2)
    system.chemical_states.append_state()
    system._structure_chemical_state_indices = pd.array([1], dtype="Int64")
    previous = system.topology

    with pytest.raises(msm.StructuralInconsistencyError, match="outside"):
        system.topology = Topology(n_atoms=2)

    assert system.topology is previous
    assert system.chemical_states.n_chemical_states == 2


def test_pickle_and_legacy_state_restore_one_collection():
    system = MolSys(n_atoms=2)
    system.topology.add_bonds([[0, 1]])
    loaded = pickle.loads(pickle.dumps(system))
    assert loaded.chemical_states is loaded.topology._chemical_states_domain
    assert len(loaded.topology.bonds) == 1
    replacement = ChemicalStates(n_atoms=2)
    replacement.append_state()
    loaded.chemical_states = replacement
    assert loaded.chemical_states is replacement

    topology = Topology(n_atoms=2)
    topology.add_bonds([[0, 1]])
    legacy_state = topology.__dict__.copy()
    domain = legacy_state.pop("_chemical_states_domain")
    legacy_state["_chemical_states"] = domain._states
    legacy_state["_reference_chemical_state_index"] = domain._reference_index
    restored = object.__new__(Topology)
    restored.__setstate__(legacy_state)
    assert restored._chemical_states_domain.n_atoms == 2
    assert restored._chemical_states_domain.get_bonds() is restored.bonds
