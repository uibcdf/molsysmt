from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_file_pdb(item, atom_indices='all', structure_indices='all', digest=True):

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)

    tmp_item.save_pdb(output_filename)
    tmp_item = output_filename

    return tmp_item

