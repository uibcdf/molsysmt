
def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):


    from molmodmt.native import DataFrame

    tmp_item = DataFrame()

    n_atoms = item.getNumAtoms()

    atom_index_array = empty(n_atoms, dtype=int)
    atom_name_array = empty(n_atoms, dtype=object)
    atom_id_array = empty(n_atoms, dtype=int)
    atom_type_array = empty(n_atoms, dtype=object)
    atom_bonded_atom_indices_array = empty(n_atoms, dtype=object)

    group_index_array = empty(n_atoms, dtype=int)
    group_name_array = empty(n_atoms, dtype=object)
    group_id_array = empty(n_atoms, dtype=int)
    group_type_array = empty(n_atoms, dtype=object)

    chain_index_array = empty(n_atoms, dtype=int)
    #chain_name_array = empty(n_atoms, dtype=object)
    chain_id_array = empty(n_atoms, dtype=int)
    #chain_type_array = empty(n_atoms, dtype=object)

    atom_index = 0

    for atom in item.atoms():

        atom_index_array[atom_index] = atom.index
        atom_name_array[atom_index] = atom.name
        atom_id_array[atom_index] = atom.id
        atom_type_array[atom_index] = atom.element.symbol

        group_index_array[atom_index] = atom.residue.index
        group_name_array[atom_index] = atom.residue.name
        group_id_array[atom_index] = atom.residue.id
        group_type_array[atom_index] = group_name_to_group_type(atom.residue.name)

        chain_index_array[atom_index] = atom.residue.chain.index
        chain_id_array[atom_index] = atom.residue.chain.id

        atom_index+=1

    tmp_item["atom.index"] = atom_index_array
    tmp_item["atom.name"] = atom_name_array
    tmp_item["atom.id"] = atom_id_array
    tmp_item["atom.type"] = atom_type_array
    del(atom_name_array, atom_id_array, atom_type_array)

    tmp_item["group.index"] = group_index_array
    tmp_item["group.name"] = group_name_array
    tmp_item["group.id"] = group_id_array
    tmp_item["group.type"] = group_type_array
    del(group_name_array, group_id_array, group_type_array)

    tmp_item["chain.index"] = chain_index_array
    tmp_item["chain.id"] = chain_id_array
    del(chain_id_array)




################
    from molmodmt.native import DataFrame
    from pandas import Series
    from molmodmt.forms.classes.api_molmodmt_DataFrame import extract_subsystem

    tmp_item = DataFrame()

    mdtraj_DataFrame, bonds_list = item.to_dataframe()

    tmp_item['atom.index'] = Series(mdtraj_DataFrame.index).values
    tmp_item['atom.name'] = mdtraj_DataFrame['name'].values
    tmp_item['atom.id'] = mdtraj_DataFrame['serial'].values
    tmp_item['atom.type'] = mdtraj_DataFrame['element'].values

    tmp_item['group.index'] = Series(atom.residue.index for atom in item.atoms).values
    tmp_item['group.name'] = mdtraj_DataFrame['resName'].values
    tmp_item['group.id'] = mdtraj_DataFrame['resSeq'].values
    #tmp_item['group.type']

    #tmp_item['component.index']
    #tmp_item['component.name']
    #tmp_item['component.id']
    #tmp_item['component.type']

    tmp_item['chain.index'] = Series(atom.residue.chain.index for atom in item.atoms).values
    #tmp_item['chain.name']
    tmp_item['chain.id'] = mdtraj_DataFrame['chainID'].values
    #tmp_item['chain.type']

    #tmp_item['entity.index']
    #tmp_item['entity.name']
    #tmp_item['entity.id']
    #tmp_item['entity.type']

    #tmp_item['bioassembly.index']
    #tmp_item['bioassembly.name']
    #tmp_item['bioassembly.id']
    #tmp_item['bioassembly.type']

    tmp_item.set_index(tmp_item['atom.index'].values)

    tmp_item = extract_subsystem(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item


