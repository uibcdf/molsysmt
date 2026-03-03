#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.arg_digestion import arg_digest

form='openmm.GromacsTopFile'

## From atom

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_atom_id_from_atom import get_atom_id_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_atom_name_from_atom import get_atom_name_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_atom_type_from_atom import get_atom_type_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_group_index_from_atom import get_group_index_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_component_index_from_atom import get_component_index_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_chain_index_from_atom import get_chain_index_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_molecule_index_from_atom import get_molecule_index_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_entity_index_from_atom import get_entity_index_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_inner_bonded_atoms_from_atom import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_inner_bonds_from_atom import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From group

@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_group_id_from_group import get_group_id_from_group as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_group_name_from_group import get_group_name_from_group as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_group_type_from_group import get_group_type_from_group as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From component

@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_component_id_from_component import get_component_id_from_component as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_component_name_from_component import get_component_name_from_component as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_component_type_from_component import get_component_type_from_component as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From molecule

@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_molecule_id_from_molecule import get_molecule_id_from_molecule as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_molecule_name_from_molecule import get_molecule_name_from_molecule as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_molecule_type_from_molecule import get_molecule_type_from_molecule as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From chain

@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_chain_id_from_chain import get_chain_id_from_chain as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_chain_name_from_chain import get_chain_name_from_chain as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_chain_type_from_chain import get_chain_type_from_chain as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From entity

@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_entity_id_from_entity import get_entity_id_from_entity as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_entity_name_from_entity import get_entity_name_from_entity as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_entity_type_from_entity import get_entity_type_from_entity as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_atoms_from_system import get_n_atoms_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_groups_from_system import get_n_groups_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_components_from_system import get_n_components_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_chains_from_system import get_n_chains_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_molecules_from_system import get_n_molecules_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_entities_from_system import get_n_entities_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_n_bonds_from_system import get_n_bonds_from_system as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From bond

@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_bond_order_from_bond import get_bond_order_from_bond as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_bond_type_from_bond import get_bond_type_from_bond as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.get_bonded_atoms_from_bond import get_bonded_atoms_from_bond as aux_get

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

