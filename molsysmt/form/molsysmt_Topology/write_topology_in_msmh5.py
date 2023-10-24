from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def write_topology_to_msmh5(item, file, atom_indices='all'):

    from h5py._hl.files import File as h5py_File
    from molsysmt.native import MSMH5FileHandler

    file_is_msmh5 = False
    needs_to_be_closed = False

    if isinstance(file, h5py_File):

        if 'type' in file.attrs:
            file_is_msmh5 = (file.attrs['type']=='msmh5')

    elif isinstance(file, MSMH5FileHandler):

            file = file.file
            file_is_msmh5 = True

    else:

        from molsysmt.form.file_msmh5.is_form import is_form as is_file_msmh5_form

        file_is_msmh5 = is_file_msmh5_form(file)

        if file_is_msmh5:
            file = h5py.File(file, "w")
            needs_to_be_closed = True

    if not file_is_msmh5:
        raise ValueError

    # Atoms

    atoms_df = item.atoms_dataframe

    n_atoms = atoms_df.shape[0]

    atoms = file['topology']['atoms']

    atoms.attrs['n_atoms'] = n_atoms

    atoms['id'].resize((n_atoms,))
    atoms['name'].resize((n_atoms,))
    atoms['type'].resize((n_atoms,))

    atoms['id'][:] = atoms_df['atom_id'].to_numpy(dtype=int)
    atoms['name'][:] = atoms_df['atom_name'].to_numpy(dtype=str)
    atoms['type'][:] = atoms_df['atom_type'].to_numpy(dtype=str)

    # Groups

    groups_df = atoms_df[['group_index', 'group_id', 'group_name', 'group_type', 'component_index']].drop_duplicates()

    n_groups = groups_df.shape[0]

    if n_groups==1:
        if groups_df['group_index'].iloc[0] == None:
            n_groups = 0

    groups = file['topology']['groups']
    groups.attrs['n_groups'] = n_groups

    if n_groups > 0:

        if all(groups_df['group_id'].unique()==[None]):
            groups_df['group_id']=groups_df['group_index']

        if all(groups_df['group_name'].unique()==[None]):
            groups_df['group_name']='UNK'

        if all(groups_df['group_type'].unique()==[None]):
            groups_df['group_type']='UNK'

        atoms['group_index'].resize((n_atoms,))
        groups['id'].resize((n_groups,))
        groups['name'].resize((n_groups,))
        groups['type'].resize((n_groups,))

        atoms['group_index'][:] = atoms_df['group_index'].to_numpy(dtype=int)
        groups['id'][:] = groups_df['group_id'].to_numpy(dtype=int)
        groups['name'][:] = groups_df['group_name'].to_numpy(dtype=str)
        groups['type'][:] = groups_df['group_type'].to_numpy(dtype=str)

    # Components

    components_df = atoms_df[['component_index', 'component_id', 'component_name', 'component_type', 'molecule_index']].drop_duplicates()

    n_components = components_df.shape[0]

    if n_components==1:
        if components_df['component_index'].iloc[0] == None:
            n_components = 0

    components = file['topology']['components']
    components.attrs['n_components'] = n_components

    if n_components > 0:

        if all(components_df['component_id'].unique()==[None]):
            components_df['component_id']=components_df['component_index']

        if all(components_df['component_name'].unique()==[None]):
            components_df['component_name']='UNK'

        if all(components_df['component_type'].unique()==[None]):
            components_df['component_type']='UNK'

        groups['component_index'].resize((n_groups,))
        components['id'].resize((n_components,))
        components['name'].resize((n_components,))
        components['type'].resize((n_components,))

        groups['component_index'][:] = groups_df['component_index'].to_numpy(dtype=int)
        components['id'][:] = components_df['component_id'].to_numpy(dtype=int)
        components['name'][:] = components_df['component_name'].to_numpy(dtype=str)
        components['type'][:] = components_df['component_type'].to_numpy(dtype=str)

    # Molecules

    molecules_df = atoms_df[['molecule_index', 'molecule_id', 'molecule_name', 'molecule_type', 'entity_index']].drop_duplicates()

    n_molecules = molecules_df.shape[0]

    if n_molecules==1:
        if molecules_df['molecule_index'].iloc[0] == None:
            n_molecules = 0

    molecules = file['topology']['molecules']
    molecules.attrs['n_molecules'] = n_molecules

    if n_molecules > 0:

        if all(molecules_df['molecule_id'].unique()==[None]):
            molecules_df['molecule_id']=molecules_df['molecule_index']

        if all(molecules_df['molecule_name'].unique()==[None]):
            molecules_df['molecule_name']='UNK'

        if all(molecules_df['molecule_type'].unique()==[None]):
            molecules_df['molecule_type']='UNK'

        components['molecule_index'].resize((n_components,))
        molecules['id'].resize((n_molecules,))
        molecules['name'].resize((n_molecules,))
        molecules['type'].resize((n_molecules,))

        components['molecule_index'][:] = components_df['molecule_index'].to_numpy(dtype=int)
        molecules['id'][:] = molecules_df['molecule_id'].to_numpy(dtype=int)
        molecules['name'][:] = molecules_df['molecule_name'].to_numpy(dtype=str)
        molecules['type'][:] = molecules_df['molecule_type'].to_numpy(dtype=str)

    # Entities

    entities_df = atoms_df[['entity_index', 'entity_id', 'entity_name', 'entity_type']].drop_duplicates()

    n_entities = entities_df.shape[0]

    if n_entities==1:
        if entities_df['entity_index'].iloc[0] == None:
            n_entities = 0

    entities = file['topology']['entities']
    entities.attrs['n_entities'] = n_entities

    if n_entities > 0:

        if all(entities_df['entity_id'].unique()==[None]):
            entities_df['entity_id']=entities_df['entity_index']

        if all(entities_df['entity_name'].unique()==[None]):
            entities_df['entity_name']='UNK'

        if all(entities_df['entity_type'].unique()==[None]):
            entities_df['entity_type']='UNK'

        molecules['entity_index'].resize((n_molecules,))
        entities['id'].resize((n_entities,))
        entities['name'].resize((n_entities,))
        entities['type'].resize((n_entities,))

        molecules['entity_index'][:] = molecules_df['entity_index'].to_numpy(dtype=int)
        entities['id'][:] = entities_df['entity_id'].to_numpy(dtype=int)
        entities['name'][:] = entities_df['entity_name'].to_numpy(dtype=str)
        entities['type'][:] = entities_df['entity_type'].to_numpy(dtype=str)


    # Chains

    chains_df = atoms_df[['chain_index', 'chain_id', 'chain_name', 'chain_type']].drop_duplicates()

    n_chains = chains_df.shape[0]

    if n_chains==1:
        if chains_df['chain_index'].iloc[0] == None:
            n_chains = 0

    chains = file['topology']['chains']
    chains.attrs['n_chains'] = n_chains

    if n_chains > 0:

        if all(chains_df['chain_id'].unique()==[None]):
            chains_df['chain_id']=chains_df['chain_index']

        if chains_df['chain_id'].dtype == 'O':
            chains_df['chain_id']=chains_df['chain_index']

        if all(chains_df['chain_name'].unique()==[None]):
            chains_df['chain_name']='UNK'

        if all(chains_df['chain_type'].unique()==[None]):
            chains_df['chain_type']='UNK'

        atoms['chain_index'].resize((n_atoms,))
        chains['id'].resize((n_chains,))
        chains['name'].resize((n_chains,))
        chains['type'].resize((n_chains,))

        atoms['chain_index'][:] = atoms_df['chain_index'].to_numpy(dtype=int)
        chains['id'][:] = chains_df['chain_id'].to_numpy(dtype=int)
        chains['name'][:] = chains_df['chain_name'].to_numpy(dtype=str)
        chains['type'][:] = chains_df['chain_type'].to_numpy(dtype=str)

    del(groups_df, components_df, molecules_df, entities_df, chains_df)

    # Bonds

    bonds_df = item.bonds_dataframe

    n_bonds = bonds_df.shape[0]

    bonds = file['topology']['bonds']
    bonds.attrs['n_bonds'] = n_bonds

    if n_bonds>0:

        if all(bonds_df['order'].unique()==[None]):
            bonds_df['order']='UNK'

        if all(bonds_df['type'].unique()==[None]):
            bonds_df['type']='UNK'

        bonds['atom1_index'].resize((n_bonds,))
        bonds['atom2_index'].resize((n_bonds,))
        bonds['order'].resize((n_bonds,))
        bonds['type'].resize((n_bonds,))

        bonds['atom1_index'][:] = bonds_df['atom1_index'].to_numpy(dtype=int)
        bonds['atom2_index'][:] = bonds_df['atom2_index'].to_numpy(dtype=int)
        bonds['order'][:] = bonds_df['order'].to_numpy(dtype=str)
        bonds['type'][:] = bonds_df['type'].to_numpy(dtype=str)


    if needs_to_be_closed:
        file.close()

    pass

