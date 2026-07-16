from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError, InternalAlgorithmError, FormatError
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@arg_digest(form='molsysmt.Topology')
def merge(items, atom_indices='all', keep_ids=True, skip_digestion=False):

    from molsysmt.native import Topology
    from . import extract

    n_items = len(items)

    output = Topology()


    if is_all(atom_indices):
        atom_indices = ['all' for ii in range(n_items)]

    if len(atom_indices)!=n_items:
        raise ArgumentError("atom_indices", value=atom_indices, caller="molsysmt.form.molsysmt_Topology.merge")

    n_atoms = []
    n_groups = []
    n_components = []
    n_chains = []
    n_molecules = []
    n_entities = []
    atoms_dataframes = []
    groups_dataframes = []
    molecules_dataframes = []
    components_dataframes = []
    chains_dataframes = []
    entities_dataframes = []
    component_indices = []
    atom_state_dataframes = []
    bonds_dataframes = []
    source_states = []

    for aux_item, aux_atom_indices in zip(items, atom_indices):

        if is_all(aux_atom_indices):
            tmp_item = aux_item
        else:
            tmp_item = extract(aux_item, atom_indices=aux_atom_indices)

        if len(tmp_item._chemical_states) != 1:
            raise StructuralInconsistencyError(
                reason=(
                    'Topology merge currently requires exactly one chemical state '
                    'per input; explicit multi-state alignment is not yet defined.'
                ),
                caller='molsysmt.form.molsysmt_Topology.merge',
            )

        bond_atom_offset = sum(n_atoms)
        group_offset = sum(n_groups)
        component_offset = sum(n_components)
        chain_offset = sum(n_chains)
        molecule_offset = sum(n_molecules)
        entity_offset = sum(n_entities)
        n_atoms.append(tmp_item.atoms.shape[0])
        n_groups.append(tmp_item.groups.shape[0])
        n_components.append(tmp_item.components.shape[0])
        n_chains.append(tmp_item.chains.shape[0])
        n_molecules.append(tmp_item.molecules.shape[0])
        n_entities.append(tmp_item.entities.shape[0])

        tmp_atoms = tmp_item.atoms.copy()
        tmp_groups = tmp_item.groups.copy()
        tmp_molecules = tmp_item.molecules.copy()
        if group_offset:
            tmp_atoms['group_index'] += group_offset
        if chain_offset:
            tmp_atoms['chain_index'] += chain_offset
        if molecule_offset:
            tmp_groups['molecule_index'] += molecule_offset
        if entity_offset:
            tmp_molecules['entity_index'] += entity_offset

        tmp_component_indices = tmp_item._get_component_indices().copy()
        known_components = tmp_component_indices.notna()
        if component_offset:
            tmp_component_indices.loc[known_components] += component_offset

        source_state = tmp_item._chemical_states[0]
        tmp_bonds = tmp_item._get_chemical_state_bonds()
        if tmp_bonds.shape[0] and bond_atom_offset:
            tmp_bonds = Topology._remap_bond_atom_indices(
                tmp_bonds,
                {
                    index: index + bond_atom_offset
                    for index in range(tmp_item.n_atoms)
                },
            )
        atoms_dataframes.append(tmp_atoms)
        groups_dataframes.append(tmp_groups)
        components_dataframes.append(tmp_item.components)
        molecules_dataframes.append(tmp_molecules)
        chains_dataframes.append(tmp_item.chains)
        entities_dataframes.append(tmp_item.entities)
        component_indices.append(tmp_component_indices)
        atom_state_dataframes.append(source_state.atom_attributes)
        bonds_dataframes.append(tmp_bonds)
        source_states.append(source_state)

    output.atoms = pd.concat(atoms_dataframes, ignore_index=True, copy=False)
    output.groups = pd.concat(groups_dataframes, ignore_index=True, copy=False)
    output.components = pd.concat(components_dataframes, ignore_index=True, copy=False)
    output.molecules = pd.concat(molecules_dataframes, ignore_index=True, copy=False)
    output.chains = pd.concat(chains_dataframes, ignore_index=True, copy=False)
    output.entities = pd.concat(entities_dataframes, ignore_index=True, copy=False)
    output._set_component_indices(
        pd.concat(component_indices, ignore_index=True, copy=False)
    )
    atom_state_attributes = pd.concat(
        atom_state_dataframes, ignore_index=True, copy=False, sort=False
    )
    for attribute in atom_state_attributes.columns:
        output._set_chemical_state_atom_attribute(
            attribute, atom_state_attributes[attribute].tolist()
        )
    output._set_chemical_state_bonds(output._concatenate_bond_tables(*bonds_dataframes))

    def _combine_completeness(values):
        if all(value == 'complete' for value in values):
            return 'complete'
        if all(value == 'unavailable' for value in values):
            return 'unavailable'
        return 'partial'

    output_state = output._chemical_states[0]
    output_state.state_id = (
        source_states[0].state_id
        if all(state.state_id == source_states[0].state_id for state in source_states)
        else None
    )
    output_state.connectivity_completeness = _combine_completeness(
        [state.connectivity_completeness for state in source_states]
    )
    output_state.component_completeness = _combine_completeness(
        [state.component_completeness for state in source_states]
    )
    output_state.component_evidence = (
        source_states[0].component_evidence
        if all(
            state.component_evidence == source_states[0].component_evidence
            for state in source_states
        )
        else 'unknown'
    )
    output_state.provenance_index = None

    if not keep_ids:
        output.rebuild_atoms(redefine_ids=True, redefine_types=False)
        output.rebuild_groups(redefine_ids=True, redefine_types=False)
        output.rebuild_components(redefine_indices=False, redefine_ids=True, redefine_types=False,
                                  redefine_names=False)
        output.rebuild_molecules(redefine_indices=False, redefine_ids=True, redefine_types=False,
                                  redefine_names=False)
        output.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False)
    else:
        output.rebuild_chains(redefine_indices=False, redefine_ids=False, redefine_types=True, redefine_names=False)
        output.rebuild_entities(redefine_indices=False, redefine_ids=False,
                                redefine_types=True, redefine_names=False)

    return output
