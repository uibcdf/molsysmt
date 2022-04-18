from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_xtc(item, atom_indices='all', structure_indices=structure_indices, check=True):

    if check:

        digest_item(item, 'mdtraj.Trajectory')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, check=False)

    tmp_item.save_xtc(output_filename)
    tmp_item = output_filename

    return tmp_item

