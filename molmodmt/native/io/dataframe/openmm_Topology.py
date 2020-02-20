
def from_openmm_Topology(item, atom_indices='all', frame_indices='all'):


    from molmodmt.native import DataFrame

    tmp_item = DataFrame()


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


