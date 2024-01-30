from molsysmt._private.digestion import digest

@digest(form='MDAnalysis.Universe')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None,
        multiframe=True, skip_digestion=False):

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item.atoms.write(output_filename, multiframe=multiframe)
    tmp_item = output_filename

    return tmp_item

