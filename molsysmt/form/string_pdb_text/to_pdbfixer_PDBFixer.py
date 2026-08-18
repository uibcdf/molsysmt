from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to pdbfixer.PDBFixer.

    Parameters
    ----------
    item : string:pdb_text
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pdbfixer.PDBFixer
        Converted molecular system representation.
    """

    from io import StringIO
    from pdbfixer.pdbfixer import PDBFixer
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, skip_digestion=True)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.seek(0)
    #tmp_io.close()

    tmp_item = PDBFixer(pdbfile=tmp_io)

    return tmp_item

