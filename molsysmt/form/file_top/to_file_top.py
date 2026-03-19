from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:top')
def to_file_top(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
                   output_filename=output_filename, skip_digestion=True)
