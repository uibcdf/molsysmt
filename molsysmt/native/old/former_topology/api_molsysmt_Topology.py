from os.path import basename as _basename
from molsysmt.utils.exceptions import *
from molsysmt.native.topology import Topology as molsysmt_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    molsysmt_Topology : form_name,
    'molsysmt.Topology': form_name
}

info=["",""]
with_topology=True
with_trajectory=False

def to_aminoacids3_seq(item, atom_indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import to_aminoacids3_seq as molsysmt_dataframe_to_aminoacids3_seq
    tmp_item = molsysmt_dataframe_to_aminoacids3_seq(item.dataframe, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)
    return tmp_item

def to_aminoacids1_seq(item, atom_indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import to_aminoacids1_seq as molsysmt_dataframe_to_aminoacids1_seq
    tmp_item = molsysmt_dataframe_to_aminoacids1_seq(item.dataframe, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)
    return tmp_item

def to_networkx_Graph(item, atom_indices='all', structure_indices='all'):

    from .api_networkx_Graph import extract as extract_networkx_Graph
    from networkx import empty_graph

    G = empty_graph(item.n_atoms)

    for bond in item.bond:
        G.add_edge(bond.atom[0].index, bond.atom[1].index)

    tmp_item = extract_networkx_Graph(G, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.io.topology.molsysmt_DataFrame import to_molsysmt_DataFrame as molsysmt_Topology_to_molsysmt_DataFrame
    tmp_item = molsysmt_Topology_to_molsysmt_DataFrame(item, atom_indices=atom_indices, structure_indices=structure_indices)
    return tmp_item

def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all', structure_indices='all'):
    from molsysmt.native.io.topology import to_pdb as molsysmt_Topology_to_pdb
    return molsysmt_Topology_to_pdb(item, output_filepath=output_filepath,
                                    trajectory_item=trajectory_item,  atom_indices=atom_indices,
                                    structure_indices=structure_indices)

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, structure_indices=structure_indices)

def copy(item):

    return item.copy()

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    from molsysmt.native.selector import dataframe_select
    atom_indices = dataframe_select(item.dataframe, selection)
    return atom_indices

###### Get

## atom

def get_index_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_id_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_name_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_type_from_atom (item, indices='all', structure_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_bonded_atoms_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_atom (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_atom(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_atom(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_atom as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_form_from_atom(item, indices='all', structure_indices='all'):

    return form_name

## group

def get_index_from_group (item, indices='all', structure_indices='all'):
    get_group_index_from_group (item, indices=indices, structure_indices=structure_indices)

def get_id_from_group (item, indices='all', structure_indices='all'):

    get_group_id_from_group (item, indices=indices, structure_indices=structure_indices)

def get_name_from_group (item, indices='all', structure_indices='all'):

    get_group_name_from_group (item, indices=indices, structure_indices=structure_indices)

def get_type_from_group (item, indices='all', structure_indices='all'):

    get_group_type_from_group (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_group (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_group(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_group(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_group as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

## component

def get_index_from_component (item, indices='all', structure_indices='all'):

    return get_component_index_from_component (item, indices=indices, structure_indices=structure_indices)

def get_id_from_component (item, indices='all', structure_indices='all'):

    return get_component_id_from_component (item, indices=indices, structure_indices=structure_indices)

def get_name_from_component (item, indices='all', structure_indices='all'):

    return get_component_name_from_component (item, indices=indices, structure_indices=structure_indices)

def get_type_from_component (item, indices='all', structure_indices='all'):

    return get_component_type_from_component (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_component (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_component(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_component as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

## molecule

def get_index_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_id_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_name_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_type_from_molecule (item, indices='all', structure_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_molecule (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_molecule(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_molecule as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

## chain

def get_index_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_id_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_name_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_type_from_chain (item, indices='all', structure_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_chain (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_chain(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_chain as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

## entity

def get_index_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_id_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_name_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_type_from_entity (item, indices='all', structure_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, structure_indices=structure_indices)

def get_atom_index_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_id_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_name_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_atom_type_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_atom_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_index_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_id_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_name_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_group_type_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_group_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_component_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_component_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_chain_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_chain_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_molecule_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_molecule_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_index_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_index_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_id_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_name_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_entity_type_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_entity (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_entity(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_charge_from_entity as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

## system

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_bonded_atoms_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_atoms_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_groups_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_components_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_chains_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_molecules_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_entities_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_bonds_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_aminoacids_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_aminoacids_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_nucleotides_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_nucleotides_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_ions_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_ions_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)
def get_n_waters_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_waters_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_cosolutes_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_cosolutes_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_small_molecules_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_small_molecules_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_peptides_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_peptides_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_proteins_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_proteins_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_dnas_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_dnas_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_rnas_from_system (item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_n_dnas_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_mass_from_system(item, indices='all', structure_indices='all'):

    from .api_molsysmt_DataFrame import get_mass_from_system as _get
    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_charge_from_system(item, indices='all', structure_indices='all'):

    return _get(item.dataframe, indices=indices, structure_indices=structure_indices)

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    return 0

def get_form_from_system(item, indices='all', structure_indices='all'):

    return form_name

