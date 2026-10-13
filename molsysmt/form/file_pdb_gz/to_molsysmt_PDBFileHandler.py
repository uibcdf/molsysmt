from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):
    """Reading a compressed PDB into an independently owned native handler.

    Parameters
    ----------
    item : molecular system
        String or path-like gzip-compressed PDB input.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.PDBFileHandler
        Native parser result owning its decoded text buffer. Close it after use.

    Raises
    ------
    FileContentError
        If gzip integrity or UTF-8 decoding fails, with the original cause retained.

    Notes
    -----
    Reads without creating a decompressed file. Native PDB parsing remains eager;
    this is not a streaming trajectory reader. Compressed source bytes are retained.

    .. versionadded:: 1.0.0
    """
    from ._read import read_handler

    return read_handler(item)
