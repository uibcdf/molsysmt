from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSysOld')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from copy import deepcopy

    tmp_item = MolSys()

    tmp_item.topology.atoms.atom_name = item.topology.atoms_dataframe.atom_name.copy()
    tmp_item.topology.atoms.atom_id = item.topology.atoms_dataframe.atom_id.copy()
    tmp_item.topology.atoms.atom_type = item.topology.atoms_dataframe.atom_type.copy()
    tmp_item.topology.atoms.group_index = item.topology.atoms_dataframe.group_index.copy()
    tmp_item.topology.atoms.chain_index = item.topology.atoms_dataframe.chain_index.copy()

    aux_df = item.topology.atoms_dataframe.groupby('group_index').agg({'group_id': 'first',
                                                                       'group_name': 'first',
                                                                       'group_type': 'first',
                                                                       'component_index': 'first'}).reset_index()

    tmp_item.topology.groups.group_id = aux_df.group_id.copy()
    tmp_item.topology.groups.group_name = aux_df.group_name.copy()
    tmp_item.topology.groups.group_type = aux_df.group_type.copy()
    tmp_item.topology.groups.component_index = aux_df.component_index.copy()

    del aux_df

    aux_df = item.topology.atoms_dataframe.groupby('component_index').agg({'component_id': 'first',
                                                                       'component_name': 'first',
                                                                       'component_type': 'first',
                                                                       'molecule_index': 'first'}).reset_index()

    tmp_item.topology.components.component_id = aux_df.component_id.copy()
    tmp_item.topology.components.component_name = aux_df.component_name.copy()
    tmp_item.topology.components.component_type = aux_df.component_type.copy()
    tmp_item.topology.components.molecule_index = aux_df.molecule_index.copy()

    del aux_df

    aux_df = item.topology.atoms_dataframe.groupby('molecule_index').agg({'molecule_id': 'first',
                                                                       'molecule_name': 'first',
                                                                       'molecule_type': 'first',
                                                                       'entity_index': 'first'}).reset_index()

    tmp_item.topology.molecules.molecule_id = aux_df.molecule_id.copy()
    tmp_item.topology.molecules.molecule_name = aux_df.molecule_name.copy()
    tmp_item.topology.molecules.molecule_type = aux_df.molecule_type.copy()
    tmp_item.topology.molecules.entity_index = aux_df.entity_index.copy()

    del aux_df

    aux_df = item.topology.atoms_dataframe.groupby('chain_index').agg({'chain_id': 'first',
                                                                       'chain_name': 'first',
                                                                       'chain_type': 'first'}).reset_index()

    tmp_item.topology.chains.chain_id = aux_df.chain_id.copy()
    tmp_item.topology.chains.chain_name = aux_df.chain_name.copy()
    tmp_item.topology.chains.chain_type = aux_df.chain_type.copy()

    del aux_df

    aux_df = item.topology.atoms_dataframe.groupby('entity_index').agg({'entity_id': 'first',
                                                                       'entity_name': 'first',
                                                                       'entity_type': 'first'}).reset_index()

    tmp_item.topology.entities.entity_id = aux_df.entity_id.copy()
    tmp_item.topology.entities.entity_name = aux_df.entity_name.copy()
    tmp_item.topology.entities.entity_type = aux_df.entity_type.copy()

    del aux_df

    tmp_item.topology.bonds.atom1_index = item.topology.bonds_dataframe.atom1_index.copy()
    tmp_item.topology.bonds.atom2_index = item.topology.bonds_dataframe.atom2_index.copy()

    tmp_item.structures.n_atoms = item.structures.n_atoms
    tmp_item.structures.n_structures = item.structures.n_structures

    tmp_item.structures.coordinates = deepcopy(item.structures.coordinates)
    tmp_item.structures.velocities = deepcopy(item.structures.velocities)
    tmp_item.structures.box = deepcopy(item.structures.box)
    tmp_item.structures.time = deepcopy(item.structures.time)

    return tmp_item
