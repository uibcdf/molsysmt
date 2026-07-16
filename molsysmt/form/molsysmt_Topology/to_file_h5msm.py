from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import InternalAlgorithmError
from molsysmt._private.variables import is_all
import numpy as np
import h5py

@arg_digest(form='molsysmt.Topology')
def to_file_h5msm(item, atom_indices='all', coordinates=None, output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):

    from molsysmt.native import H5MSMFileHandler

    handler = H5MSMFileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False)

    dump_topology_to_h5msm(item, handler, atom_indices=atom_indices)

    handler.close()

    return output_filename

def dump_topology_to_h5msm(item, file, atom_indices='all'):

    from molsysmt.native import H5MSMFileHandler
    from datetime import datetime

    file_is_h5msm = False
    needs_to_be_closed = False


    if isinstance(file, h5py._hl.files.File):

        if 'type' in file.attrs:
            file_is_h5msm = (file.attrs['type']=='h5msm')

    elif isinstance(file, H5MSMFileHandler):

            file = file.file
            file_is_h5msm = True

    else:

        from molsysmt.form.file_h5msm.is_form import is_form as is_file_h5msm_form

        file_is_h5msm = is_file_h5msm_form(file)

        if file_is_h5msm:
            file = h5py.File(file, "w")
            needs_to_be_closed = True

    if not file_is_h5msm:
        raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.form.molsysmt_Topology.to_file_h5msm")
    if not is_all(atom_indices):
        item = item.extract(atom_indices=atom_indices, skip_digestion=True)
    int_precision = file.attrs['int_precision']
    float_precision = file.attrs['float_precision']

    if int_precision=='single':
        int_type=np.int32
    elif int_precision=='double':
        int_type=np.int64

    if float_precision=='single':
        float_type=np.float32
    elif float_precision=='double':
        float_type=np.float64


    # Atoms

    atoms_df = item.atoms

    n_atoms = atoms_df.shape[0]

    file['topology'].attrs['n_atoms'] = n_atoms

    atoms = file['topology']['atoms']

    atoms['atom_id'].resize((n_atoms,))
    atoms['atom_name'].resize((n_atoms,))
    atoms['atom_type'].resize((n_atoms,))
    if 'isotope' in atoms:
        atoms['isotope'].resize((n_atoms,))
    atoms['group_index'].resize((n_atoms,))
    atoms['chain_index'].resize((n_atoms,))

    atoms['atom_id'][:] = atoms_df['atom_id'].to_numpy(dtype='S')
    atoms['atom_name'][:] = atoms_df['atom_name'].to_numpy(dtype='S')
    atoms['atom_type'][:] = atoms_df['atom_type'].to_numpy(dtype='S')
    if 'isotope' in atoms:
        atoms['isotope'][:] = atoms_df['isotope'].fillna(0).to_numpy(dtype=np.uint16)
    atoms['group_index'][:] = atoms_df['group_index'].fillna(-1).to_numpy(dtype=int_type)
    atoms['chain_index'][:] = atoms_df['chain_index'].fillna(-1).to_numpy(dtype=int_type)

    # Groups

    groups_df = item.groups

    n_groups = groups_df.shape[0]

    file['topology'].attrs['n_groups'] = n_groups

    groups = file['topology']['groups']

    if n_groups > 0:

        groups['group_id'].resize((n_groups,))
        groups['group_name'].resize((n_groups,))
        groups['group_type'].resize((n_groups,))
        groups['molecule_index'].resize((n_groups,))

        groups['group_id'][:] = groups_df['group_id'].to_numpy(dtype='S')
        groups['group_name'][:] = groups_df['group_name'].to_numpy(dtype='S')
        groups['group_type'][:] = groups_df['group_type'].to_numpy(dtype='S')
        groups['molecule_index'][:] = groups_df['molecule_index'].fillna(-1).to_numpy(dtype=int_type)

    # Molecules

    molecules_df = item.molecules

    n_molecules = molecules_df.shape[0]

    file['topology'].attrs['n_molecules'] = n_molecules

    molecules = file['topology']['molecules']

    if n_molecules > 0:

        molecules['molecule_id'].resize((n_molecules,))
        molecules['molecule_name'].resize((n_molecules,))
        molecules['molecule_type'].resize((n_molecules,))
        molecules['entity_index'].resize((n_molecules,))

        molecules['molecule_id'][:] = molecules_df['molecule_id'].to_numpy(dtype='S')
        molecules['molecule_name'][:] = molecules_df['molecule_name'].to_numpy(dtype='S')
        molecules['molecule_type'][:] = molecules_df['molecule_type'].to_numpy(dtype='S')
        molecules['entity_index'][:] = molecules_df['entity_index'].fillna(-1).to_numpy(dtype=int_type)

    # Entities

    entities_df = item.entities

    n_entities = entities_df.shape[0]

    file['topology'].attrs['n_entities'] = n_entities

    entities = file['topology']['entities']

    if n_entities > 0:

        entities['entity_id'].resize((n_entities,))
        entities['entity_name'].resize((n_entities,))
        entities['entity_type'].resize((n_entities,))

        entities['entity_id'][:] = entities_df['entity_id'].to_numpy(dtype='S')
        entities['entity_name'][:] = entities_df['entity_name'].to_numpy(dtype='S')
        entities['entity_type'][:] = entities_df['entity_type'].to_numpy(dtype='S')

    # Chains

    chains_df = item.chains

    n_chains = chains_df.shape[0]

    file['topology'].attrs['n_chains'] = n_chains

    chains = file['topology']['chains']

    if n_chains > 0:

        chains['chain_id'].resize((n_chains,))
        chains['chain_name'].resize((n_chains,))
        chains['chain_type'].resize((n_chains,))

        chains['chain_id'][:] = chains_df['chain_id'].to_numpy(dtype='S')
        chains['chain_name'][:] = chains_df['chain_name'].to_numpy(dtype='S')
        chains['chain_type'][:] = chains_df['chain_type'].to_numpy(dtype='S')

    del atoms_df, groups_df, molecules_df, entities_df, chains_df

    dataset_options = {
        'compression': file['topology']['atoms']['atom_id'].compression,
    }
    if dataset_options['compression'] == 'gzip':
        dataset_options['compression_opts'] = file['topology']['atoms']['atom_id'].compression_opts
    from ._h5msm_chemical_states import write_chemical_states

    write_chemical_states(item, file['topology'], dataset_options)

    # Modification time

    file.attrs['modification_time'] = datetime.now().isoformat()

    if needs_to_be_closed:
        file.close()

    pass
