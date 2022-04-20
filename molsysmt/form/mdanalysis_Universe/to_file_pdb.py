from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        multiframe=True, check=True):

    if check:

        digest_item(item, 'mdanalysis.Universe')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)


    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.atoms.write(output_filename, multiframe=multiframe)
    tmp_item = output_filename

    return tmp_item

