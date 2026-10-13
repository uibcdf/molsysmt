from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def to_molsysmt_Topology(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
    *,
    get_missing_bonds=True,
    bond_inference_engine=None,
):
    """Reading compressed PDB data into native Topology through the existing parser.

    Parameters
    ----------
    item : molecular system
        String or path-like gzip-compressed PDB input.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Retained conversion option; PDB topology is independent of coordinate
        structure selection, matching the plain PDB topology route.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    get_missing_bonds : bool, default=True
        Whether to request the plain PDB connectivity policy. False preserves
        only declared edges and never invokes an inference engine.
    bond_inference_engine : str or None, default=None
        Explicit MolSysMT or OpenMM engine, requiring get_missing_bonds=True.
        None retains the plain PDB default and its diagnosed optional fallback.

    Returns
    -------
    molsysmt.Topology
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
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_Topology import (
        to_molsysmt_Topology as convert_handler,
    )

    from ._read import read_handler

    handler = read_handler(item)
    try:
        return convert_handler(
            handler,
            atom_indices=atom_indices,
            get_missing_bonds=get_missing_bonds,
            bond_inference_engine=bond_inference_engine,
            skip_digestion=True,
        )
    finally:
        handler.close()
