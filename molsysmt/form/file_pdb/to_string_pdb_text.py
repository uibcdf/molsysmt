from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to string:pdb_text.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:pdb_text
        Resulting object in string:pdb_text form.


    .. versionadded:: 1.0.0
    """

    from ..string_pdb_text.extract import extract as extract_string_pdb_text

    with open(item, 'r') as fff:
        tmp_item = fff.read()

    tmp_item = extract_string_pdb_text(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item
