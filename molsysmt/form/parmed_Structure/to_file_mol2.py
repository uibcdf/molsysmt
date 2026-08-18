from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_file_mol2(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from parmed.Structure to file.mol2.

    Parameters
    ----------
    item : parmed.Structure
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.mol2
        Converted molecular system representation.
    """

    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)
    tmp_item.save(output_filename)
    tmp_item = output_filename

    return tmp_item

