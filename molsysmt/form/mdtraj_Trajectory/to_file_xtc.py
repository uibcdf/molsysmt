from molsysmt._private.digestion import digest

@digest(form='mdtraj.Trajectory')
def to_file_xtc(item, atom_indices='all', structure_indices='all'):

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False)

    tmp_item.save_xtc(output_filename)
    tmp_item = output_filename

    return tmp_item

def _to_file_xtc(item, atom_indices='all', structure_indices='all', output_filename=None):

    return to_file_xtc(item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=output_filename)

