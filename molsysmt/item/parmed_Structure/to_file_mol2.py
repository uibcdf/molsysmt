from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:

        digest_item(item, 'parmed.Structure')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False)
    tmp_item.save(output_filename)
    tmp_item = output_filename

    return tmp_item

