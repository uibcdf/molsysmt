from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom

@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_order_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_pairs_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_pairs_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_inner_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_inner_bonded_atoms_pairs_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_inner_bonded_atoms_pairs_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_aminoacids_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From group


@digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From component


@digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_inner_bonds_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_aminoacids_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From molecule


@digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_inner_bonds_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_aminoacids_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From entity


@digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_inner_bonds_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_aminoacids_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From chain


@digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_atom_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_group_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_component_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_molecule_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_entity_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_chain_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_inner_bonds_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_aminoacids_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From bond


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_index_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_order_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bond_type_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_pairs_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_pairs_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From system


@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_groups_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_components_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_chains_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_molecules_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_entities_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_bonds_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)

@digest(form=form)
def get_n_aminoacids_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_aminoacids_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_nucleotides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_ions_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_waters_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_small_molecules_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_peptides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_proteins_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_dnas_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_rnas_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)

@digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_lipids_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_oligosaccharides_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_oligosaccharides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_n_saccharides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_index_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_inner_bonded_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_inner_bonded_atoms_pairs_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_inner_bonded_atoms_pairs_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@digest(form=form)
def get_bonded_atoms_pairs_from_system(item, skip_digestion=False):

    from ..molsysmt_Topology import get_bonded_atoms_pairs_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

