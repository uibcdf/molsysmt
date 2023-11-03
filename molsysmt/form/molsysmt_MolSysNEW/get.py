from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest

form='molsysmt.MolSysNEW'

## From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_entity_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_entity_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_entity_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_entity_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_groups_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_components_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_chains_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_entities_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bonded_atoms_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_inner_bond_index_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_inner_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_inner_bonded_atoms_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_inner_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_inner_bonds_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_inner_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_coordinates_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

@digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_velocities_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

@digest(form=form)
def get_occupancy_from_atom (item, indices='all', structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_occupancy_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

@digest(form=form)
def get_alternate_location_from_atom (item, indices='all', structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_alternate_location_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

@digest(form=form)
def get_b_factor_from_atom (item, indices='all', structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_b_factor_from_atom as aux_get
    return aux_get(item.structures, indices=indices, structure_indices=structure_indices)

@digest(form=form)
def get_formal_charge_from_atom (item, indices='all'):

    from ..molsysmt_MolecularMechanics import get_formal_charge_from_atom as aux_get
    return aux_get(item.molecular_mechanics, indices=indices)

@digest(form=form)
def get_partial_charge_from_atom (item, indices='all'):

    from ..molsysmt_MolecularMechanics import get_partial_charge_from_atom as aux_get
    return aux_get(item.molecular_mechanics, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_aminoacids_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_nucleotides_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_ions_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_waters_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_small_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_atomNEW (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_atomNEW (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_dnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_rnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_lipids_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_oligosaccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_atom (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_n_saccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices)


## group

@digest(form=form)
def get_atom_index_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_atom_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from ..molsysmt_TopologyNEW import get_group_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_component_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_chain_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_group (item, indices='all'):

    from ..molsysmt_TopologyNEW import get_molecule_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_index_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_id_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_name_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_type_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_atoms_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_groups_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_components_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_molecules_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_chains_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_entities_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_ions_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_waters_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_dnas_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_rnas_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_lipids_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_group as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_group (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_group as aux_get
    return aux_get(item.topology, indices=indices)


## component

@digest(form=form)
def get_atom_index_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_component(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_index_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_id_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_name_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_type_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_atoms_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_groups_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_components_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_chains_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_entities_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_ions_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_waters_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_dnas_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_rnas_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_lipids_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_component (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices)


## molecule

@digest(form=form)
def get_atom_index_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_molecule(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_atoms_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_groups_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_components_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_chains_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_entities_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_ions_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_waters_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_dnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_rnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_lipids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_molecule (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices)


## chain

@digest(form=form)
def get_atom_index_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_chain(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_atoms_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_groups_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_components_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_chains_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_entities_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_ions_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_waters_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_dnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_rnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_lipids_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_chain (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices)


## entity

@digest(form=form)
def get_atom_index_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_id_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_name_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_atom_type_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_atom_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_index_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_id_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_name_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_group_type_from_entity(item, indices='all'):

    from ..molsysmt_TopologyNew import get_group_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_name_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_index_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_id_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_component_type_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_component_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_name_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_index_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_id_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_chain_type_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_chain_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_index_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_id_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_name_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_molecule_type_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_molecule_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_index_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_id_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_name_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_entity_type_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_entity_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_atoms_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_atoms_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_groups_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_groups_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_components_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_components_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_molecules_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_chains_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_chains_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_entities_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_entities_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_aminoacids_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_nucleotides_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_ions_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_ions_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_waters_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_waters_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_small_molecules_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_peptides_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_peptides_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_proteins_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_proteins_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_dnas_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_dnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_rnas_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_rnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_lipids_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_lipids_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_oligosaccharides_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_saccharides_from_entity (item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices)


## system

@digest(form=form)
def get_n_atoms_from_system(item):

    from ..molsysmt_TopologyNew import get_n_atoms_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_groups_from_system(item):

    from ..molsysmt_TopologyNew import get_n_groups_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_components_from_system(item):

    from ..molsysmt_TopologyNew import get_n_components_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_chains_from_system(item):

    from ..molsysmt_TopologyNew import get_n_chains_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_molecules_from_system(item):

    from ..molsysmt_TopologyNew import get_n_molecules_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_entities_from_system(item):

    from ..molsysmt_TopologyNew import get_n_entities_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_bonds_from_system(item):

    from ..molsysmt_TopologyNew import get_n_bonds_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_aminoacids_from_system (item):

    from ..molsysmt_TopologyNew import get_n_aminoacids_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_nucleotides_from_system (item):

    from ..molsysmt_TopologyNew import get_n_nucleotides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_ions_from_system (item):

    from ..molsysmt_TopologyNew import get_n_ions_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_waters_from_system (item):

    from ..molsysmt_TopologyNew import get_n_waters_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_small_molecules_from_system (item):

    from ..molsysmt_TopologyNew import get_n_small_molecules_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_peptides_from_system (item):

    from ..molsysmt_TopologyNew import get_n_peptides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_proteins_from_system (item):

    from ..molsysmt_TopologyNew import get_n_proteins_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_dnas_from_system (item):

    from ..molsysmt_TopologyNew import get_n_dnas_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_rnas_from_system (item):

    from ..molsysmt_TopologyNew import get_n_rnas_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_lipids_from_system (item):

    from ..molsysmt_TopologyNew import get_n_lipids_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_oligosaccharides_from_system (item):

    from ..molsysmt_TopologyNew import get_n_oligosaccharides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_n_saccharides_from_system (item):

    from ..molsysmt_TopologyNew import get_n_saccharides_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_coordinates_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_velocities_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_velocities_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_box_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_shape_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_box_shape_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_lengths_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_box_lengths_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_angles_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_box_angles_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_box_volume_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_box_volume_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_time_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_structure_id_from_system as aux_get
    return aux_get(item.structures, structure_indices=structure_indices)

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_n_structures_from_system as aux_get
    return aux_get(item.structures, structure_indices='all')

@digest(form=form)
def get_bonded_atoms_from_system(item):

    from ..molsysmt_TopologyNew import get_bonded_atoms_from_system as aux_get
    return aux_get(item.topology)

@digest(form=form)
def get_occupancy_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_occupancy_from_system as aux_get
    return aux_get(item.structures, structure_indices='all')

@digest(form=form)
def get_b_factor_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_b_factor_from_system as aux_get
    return aux_get(item.structures, structure_indices='all')

@digest(form=form)
def get_alternate_location_from_system(item, structure_indices='all'):

    from ..molsysmt_StructuresNEW import get_alternate_location_from_system as aux_get
    return aux_get(item.structures, structure_indices='all')

@digest(form=form)
def get_bioassembly_from_system(item):

    from ..molsysmt_StructuresNEW import get_bioassembly_from_system as aux_get
    return aux_get(item.structures)

@digest(form=form)
def get_n_bioassemblies_from_system(item):

    from ..molsysmt_StructuresNEW import get_n_bioassemblies_from_system as aux_get
    return aux_get(item.structures)


## bond

@digest(form=form)
def get_bond_index_from_bond(item, indices='all'):

    from ..molsysmt_TopologyNew import get_bond_index_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    from ..molsysmt_TopologyNew import get_bond_order_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    from ..molsysmt_TopologyNew import get_bond_type_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    from ..molsysmt_TopologyNew import get_bonded_atoms_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

@digest(form=form)
def get_n_bonds_from_bond(item, indices='all'):

    from ..molsysmt_TopologyNew import get_n_bonds_from_bond as aux_get
    return aux_get(item.topology, indices=indices)

## molecular mechanics

@digest(form=form)
def get_forcefield_from_system(item):

    from ..molsysmt_MolecularMechanics import get_forcefield_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_non_bonded_method_from_system(item):

    from ..molsysmt_MolecularMechanics import get_non_bonded_method_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_cutoff_distance_from_system(item):

    from ..molsysmt_MolecularMechanics import get_cutoff_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_switch_distance_from_system(item):

    from ..molsysmt_MolecularMechanics import get_switch_distance_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_dispersion_correction_from_system(item):

    from ..molsysmt_MolecularMechanics import get_dispersion_correction_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_ewald_error_tolerance_from_system(item):

    from ..molsysmt_MolecularMechanics import get_ewald_error_tolerance_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_hydrogen_mass_from_system(item):

    from ..molsysmt_MolecularMechanics import get_hydrogen_mass_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_constraints_from_system(item):

    from ..molsysmt_MolecularMechanics import get_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_flexible_constraints_from_system(item):

    from ..molsysmt_MolecularMechanics import get_flexible_constraints_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_water_model_from_system(item):

    from ..molsysmt_MolecularMechanics import get_water_model_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_rigid_water_from_system(item):

    from ..molsysmt_MolecularMechanics import get_rigid_water_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_implicit_solvent_from_system(item):

    from ..molsysmt_MolecularMechanics import get_implicit_solvent_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_solute_dielectric_from_system(item):

    from ..molsysmt_MolecularMechanics import get_solute_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_solvent_dielectric_from_system(item):

    from ..molsysmt_MolecularMechanics import get_solvent_dielectric_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_salt_concentration_from_system(item):

    from ..molsysmt_MolecularMechanics import get_salt_concentration_from_system as aux_get
    return aux_get(item.molecular_mechanics)

@digest(form=form)
def get_kappa_from_system(item):

    from ..molsysmt_MolecularMechanics import get_kappa_from_system as aux_get
    return aux_get(item.molecular_mechanics)

