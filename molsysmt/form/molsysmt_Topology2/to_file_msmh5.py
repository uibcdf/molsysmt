from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology2')
def to_file_msmh5(item, atom_indices='all', coordinates=None, output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single'):

    from molsysmt.native import MSMH5FileHandler

    handler = MSMH5FileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False)

    _add_topology_to_msmh5(item, handler, atom_indices=atom_indices)

    handler.close()

    return output_filename

def _add_topology_to_msmh5(item, file, atom_indices='all'):

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

    atoms_df = item.atoms

    n_atoms = atoms_df.shape[0]

    atoms = file['topology']['atoms']

    atoms.attrs['n_atoms'] = n_atoms

    atoms['id'].resize((n_atoms,))
    atoms['name'].resize((n_atoms,))
    atoms['type'].resize((n_atoms,))
    atoms['group_index'].resize((n_atoms,))
    atoms['chain_index'].resize((n_atoms,))

    atoms['id'][:] = atoms_df['atom_id'].to_numpy(dtype=int)
    atoms['name'][:] = atoms_df['atom_name'].to_numpy(dtype=str)
    atoms['type'][:] = atoms_df['atom_type'].to_numpy(dtype=str)
    atoms['group_index'][:] = atoms_df['group_index'].to_numpy(dtype=int)
    atoms['chain_index'][:] = atoms_df['chain_index'].to_numpy(dtype=int)

    # Groups

    groups_df = item.groups

    n_groups = groups_df.shape[0]

    groups = file['topology']['groups']
    groups.attrs['n_groups'] = n_groups

    if n_groups > 0:

        groups['id'].resize((n_groups,))
        groups['name'].resize((n_groups,))
        groups['type'].resize((n_groups,))
        groups['component_index'].resize((n_groups,))

        groups['id'][:] = groups_df['group_id'].to_numpy(dtype=int)
        groups['name'][:] = groups_df['group_name'].to_numpy(dtype=str)
        groups['type'][:] = groups_df['group_type'].to_numpy(dtype=str)
        groups['component_index'][:] = groups_df['component_index'].to_numpy(dtype=int)

    # Components

    components_df = item.components

    n_components = components_df.shape[0]

    components = file['topology']['components']
    components.attrs['n_components'] = n_components

    if n_components > 0:

        components['id'].resize((n_components,))
        components['name'].resize((n_components,))
        components['type'].resize((n_components,))
        components['molecule_index'].resize((n_components,))

        components['id'][:] = components_df['component_id'].to_numpy(dtype=int)
        components['name'][:] = components_df['component_name'].to_numpy(dtype=str)
        components['type'][:] = components_df['component_type'].to_numpy(dtype=str)
        components['molecule_index'][:] = components_df['molecule_index'].to_numpy(dtype=int)

    # Molecules

    molecules_df = item.molecules

    n_molecules = molecules_df.shape[0]

    molecules = file['topology']['molecules']
    molecules.attrs['n_molecules'] = n_molecules

    if n_molecules > 0:

        molecules['id'].resize((n_molecules,))
        molecules['name'].resize((n_molecules,))
        molecules['type'].resize((n_molecules,))
        molecules['entity_index'].resize((n_molecules,))

        molecules['id'][:] = molecules_df['molecule_id'].to_numpy(dtype=int)
        molecules['name'][:] = molecules_df['molecule_name'].to_numpy(dtype=str)
        molecules['type'][:] = molecules_df['molecule_type'].to_numpy(dtype=str)
        molecules['entity_index'][:] = molecules_df['entity_index'].to_numpy(dtype=int)

    # Entities

    entities_df = item.entities

    n_entities = entities_df.shape[0]

    entities = file['topology']['entities']
    entities.attrs['n_entities'] = n_entities

    if n_entities > 0:

        entities['id'].resize((n_entities,))
        entities['name'].resize((n_entities,))
        entities['type'].resize((n_entities,))

        entities['id'][:] = entities_df['entity_id'].to_numpy(dtype=int)
        entities['name'][:] = entities_df['entity_name'].to_numpy(dtype=str)
        entities['type'][:] = entities_df['entity_type'].to_numpy(dtype=str)


    # Chains

    chains_df = item.chains

    n_chains = chains_df.shape[0]

    chains = file['topology']['chains']
    chains.attrs['n_chains'] = n_chains

    if n_chains > 0:

        chains['id'].resize((n_chains,))
        chains['name'].resize((n_chains,))
        chains['type'].resize((n_chains,))

        chains['id'][:] = chains_df['chain_id'].to_numpy(dtype=int)
        chains['name'][:] = chains_df['chain_name'].to_numpy(dtype=str)
        chains['type'][:] = chains_df['chain_type'].to_numpy(dtype=str)

    del(atoms_df, groups_df, components_df, molecules_df, entities_df, chains_df)

    # Bonds

    bonds_df = item.bonds

    n_bonds = bonds_df.shape[0]

    bonds = file['topology']['bonds']
    bonds.attrs['n_bonds'] = n_bonds

    if n_bonds>0:

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

