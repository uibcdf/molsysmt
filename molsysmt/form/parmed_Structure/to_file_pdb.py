from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)
    tmp_item.save(output_filename)
    tmp_item = output_filename

    return tmp_item

