from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def to_string_pdb_text(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Reading compressed PDB text with the shared plain-text selection tool.

    Parameters
    ----------
    item : molecular system
        String or path-like gzip-compressed PDB input.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str
        Decoded PDB text, retaining exact original text when both selections are all.

    Raises
    ------
    FileContentError
        If gzip integrity or UTF-8 decoding fails.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.variables import is_all
    from molsysmt.form.string_pdb_text.extract import extract

    from ._read import read_text

    text = read_text(item)
    if is_all(atom_indices) and is_all(structure_indices):
        return text
    return extract(
        text,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )
