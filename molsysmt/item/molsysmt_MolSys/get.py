from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest

form='molsysmt.MolSys'

## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bonded_atoms_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_inner_bond_index_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_inner_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_inner_bonded_atoms_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_inner_bonds_from_atom (item, indices='all'):

    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    from ..molsysmt_Structures import get_coordinates_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

## group

@digest(form=form)
def get_atom_index_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_group (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_group as aux_get
    return aux_get(item.topology, indices=indices)

## component

@digest(form=form)
def get_atom_index_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_component(item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_component (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_component as aux_get
    return aux_get(item.topology, indices=indices)

## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_molecule(item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_molecule (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)


## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_chain(item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_chain (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

## entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_atom_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_atom_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_atom_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_group_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_group_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_group_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_entity(item, indices='all'):

    from ..molsysmt_Topology import get_group_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_component_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_component_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_component_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_component_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_chain_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_chain_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_chain_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_chain_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_molecule_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_entity_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_atoms_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_groups_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_components_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_chains_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_entity (item, indices='all'):

    from ..molsysmt_Topology import get_n_entities_from_entity as aux_get
    return aux_get(item.topology, indices=indices)


## system

@digest(form=form)
def get_n_atoms_from_system(item):

    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_groups_from_system(item):

    from ..molsysmt_Topology import get_n_groups_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_components_from_system(item):

    from ..molsysmt_Topology import get_n_components_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_chains_from_system(item):

    from ..molsysmt_Topology import get_n_chains_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_molecules_from_system(item):

    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_entities_from_system(item):

    from ..molsysmt_Topology import get_n_entities_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_bonds_from_system(item):

    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_aminoacids_from_system (item):

    from ..molsysmt_Topology import get_n_aminoacids_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_nucleotides_from_system (item):

    from ..molsysmt_Topology import get_n_nucleotides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_ions_from_system (item):

    from ..molsysmt_Topology import get_n_ions_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_waters_from_system (item):

    from ..molsysmt_Topology import get_n_waters_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_cosolutes_from_system (item):

    from ..molsysmt_Topology import get_n_cosolutes_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_small_molecules_from_system (item):

    from ..molsysmt_Topology import get_n_small_molecules_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_peptides_from_system (item):

    from ..molsysmt_Topology import get_n_peptides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_proteins_from_system (item):

    from ..molsysmt_Topology import get_n_proteins_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_dnas_from_system (item):

    from ..molsysmt_Topology import get_n_dnas_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_rnas_from_system (item):

    from ..molsysmt_Topology import get_n_rnas_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_lipids_from_system (item):

    from ..molsysmt_Topology import get_n_lipids_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_coordinates_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_box_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_box_shape_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_box_lengths_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_box_angles_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_box_volume_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_time_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_step_from_system(item, structure_indices='all'):

    from ..molsysmt_Structures import get_step_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_n_structures_from_system(item):

    from ..molsysmt_Structures import get_n_structures_from_system as aux_get
    return aux_get(item.structures)

@digest(form=form)
def get_bonded_atoms_from_system(item):

    from ..molsysmt_Topology import get_bonded_atoms_from_system as aux_get
    return aux_get(item.topology)

## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all'):

    from ..molsysmt_Topology import get_bond_index_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_index_from_bond(item, indices='all'):

    from ..molsysmt_Topology import get_atom_index_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_bond(item, indices='all'):

    from ..molsysmt_Topology import get_n_bonds_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

