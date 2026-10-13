from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def to_molsysmt_Structures(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
):
    """Reading compressed PDB data into native Structures through the existing parser.

    Parameters
    ----------
    item : molecular system
        String or path-like gzip-compressed PDB input.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices (0-based), preserving existing PDB selection semantics.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Detached native data with the same PDB metadata, connectivity policy and
        configured physical units as uncompressed input.

    Raises
    ------
    FileContentError
        If gzip integrity or UTF-8 decoding fails, with the cause retained.

    Notes
    -----
    The temporary text handler closes on success and conversion failure.
    No decompressed neighbor or scratch file is created. Native parsing is eager.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Structures import (
        to_molsysmt_Structures as convert_handler,
    )

    from ._read import read_handler

    handler = read_handler(item)
    try:
        return convert_handler(
            handler,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            skip_digestion=True,
        )
    finally:
        handler.close()
