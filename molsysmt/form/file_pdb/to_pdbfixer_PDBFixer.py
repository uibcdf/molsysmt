from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:pdb to pdbfixer.PDBFixer.


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
    pdbfixer.PDBFixer
        Resulting object in pdbfixer.PDBFixer form.


    .. versionadded:: 1.0.0
    """

    from pdbfixer.pdbfixer import PDBFixer
    from ..pdbfixer_PDBFixer.extract import extract as extract_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    return tmp_item

