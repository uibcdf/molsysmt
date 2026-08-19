from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_pdbfixer_PDBFixer(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from openmm.Topology to pdbfixer.PDBFixer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pdbfixer.PDBFixer
        Resulting object in pdbfixer.PDBFixer form.


    .. versionadded:: 1.0.0
    """

    from .to_string_pdb_text import to_string_pdb_text
    from molsysmt.form.string_pdb_text.to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as string_pdb_text_to_pdbfixer_PDBFixer

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, coordinates=coordinates, skip_digestion=True)
    tmp_item = string_pdb_text_to_pdbfixer_PDBFixer(tmp_item, skip_digestion=True)

    return tmp_item

