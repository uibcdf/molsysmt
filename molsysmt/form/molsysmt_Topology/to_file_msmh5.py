from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
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

    n_atoms = item.atoms_dataframe.shape[0]

    n_atoms = item.atoms_dataframe.shape[0]

    atom_index_array = item.atoms_dataframe["atom_index"].to_numpy()
    atom_name_array = item.atoms_dataframe["atom_name"].to_numpy()
    atom_id_array = item.atoms_dataframe["atom_id"].to_numpy()
    atom_type_array = item.atoms_dataframe["atom_type"].to_numpy()

    group_index_array = item.atoms_dataframe["group_index"].to_numpy()
    group_name_array = item.atoms_dataframe["group_name"].to_numpy()
    group_id_array = item.atoms_dataframe["group_id"].to_numpy()
    group_type_array = item.atoms_dataframe["group_type"].to_numpy()

    component_index_array = item.atoms_dataframe["component_index"].to_numpy()
    component_name_array = item.atoms_dataframe["component_name"].to_numpy()
    component_id_array = item.atoms_dataframe["component_id"].to_numpy()
    component_type_array = item.atoms_dataframe["component_type"].to_numpy()

    group_index_array = item.atoms_dataframe["group_index"].to_numpy()
    group_name_array = item.atoms_dataframe["group_name"].to_numpy()
    group_id_array = item.atoms_dataframe["group_id"].to_numpy()
    group_type_array = item.atoms_dataframe["group_type"].to_numpy()



    chain_index_array = item.atoms_dataframe["chain_index"].to_numpy()
    chain_name_array = item.atoms_dataframe["chain_name"].to_numpy()
    chain_id_array = item.atoms_dataframe["chain_id"].to_numpy()
    chain_type_array = item.atoms_dataframe["chain_type"].to_numpy()

    bonds_atom1 = item.bonds_dataframe["atom1_index"].to_numpy()
    bonds_atom2 = item.bonds_dataframe["atom2_index"].to_numpy()


    for ii in range(n_atoms):




    aux_indices = item.atoms_dataframe['group_index'].unique()
    where_not_None = np.where(aux_indices!=None)
    aux_indices = aux_indices[where_not_None]
    n_groups = aux_indices.shape[0]

    aux_indices = item.atoms_dataframe['component_index'].unique()
    where_not_None = np.where(aux_indices!=None)
    aux_indices = aux_indices[where_not_None]
    n_components = aux_indices.shape[0]

    aux_indices = item.atoms_dataframe['molecule_index'].unique()
    where_not_None = np.where(aux_indices!=None)
    aux_indices = aux_indices[where_not_None]
    n_molecules = aux_indices.shape[0]

    aux_indices = item.atoms_dataframe['entity_index'].unique()
    where_not_None = np.where(aux_indices!=None)
    aux_indices = aux_indices[where_not_None]
    n_entities = aux_indices.shape[0]

    aux_indices = item.atoms_dataframe['chain_index'].unique()
    where_not_None = np.where(aux_indices!=None)
    aux_indices = aux_indices[where_not_None]
    n_chains = aux_indices.shape[0]

    # Atoms

    atoms = file['topology']['atoms']

    atoms.attrs['n_atoms'] = n_atoms

    atoms['id'].resize((n_atoms,))
    atoms['name'].resize((n_atoms,))
    atoms['type'].resize((n_atoms,))

    atoms['id'][:] = item.atoms_dataframe['atom_id'].to_numpy()
    atoms['name'][:] = item.atoms_dataframe['atom_name'].to_numpy()
    atoms['type'][:] = item.atoms_dataframe['atom_type'].to_numpy()

    # Groups

    if n_groups > 0:

        groups = file['topology']['groups']

        groups.attrs['n_groups'] = n_groups

        atoms['group_index'].resize((n_atoms,))
        groups['id'].resize((n_groups,))
        groups['name'].resize((n_groups,))
        groups['type'].resize((n_groups,))

        atoms['group_index'][:] = item.atoms_dataframe['group_index'].to_numpy()
        groups['id'][:] = item.atoms_dataframe['group_id'].to_numpy()
        groups['name'][:] = item.atoms_dataframe['group_name'].to_numpy()
        groups['type'][:] = item.atoms_dataframe['group_type'].to_numpy()

    # Components

    if n_components > 0:

        groups['component_index'].resize((n_groups,))
        groups['component_index'][:] = item.atoms_dataframe['component_index'].to_numpy()

    # Chains

    if n_chains > 0:

        atoms['chain_index'].resize((n_atoms,))
        atoms['chain_index'][:] = item.atoms_dataframe['chain_index'].to_numpy()


    if needs_to_be_closed:
        file.close()

    pass

