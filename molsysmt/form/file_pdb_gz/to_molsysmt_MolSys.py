from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb.gz")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
    *,
    get_missing_bonds=True,
    bond_inference_engine=None,
):
    """Reading compressed PDB data into native MolSys through the existing parser.

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
    get_missing_bonds : bool, default=True
        Whether to request the plain PDB connectivity policy. False preserves
        only declared edges and never invokes an inference engine.
    bond_inference_engine : str or None, default=None
        Explicit MolSysMT or OpenMM engine, requiring get_missing_bonds=True.
        None retains the plain PDB default and its diagnosed optional fallback.

    Returns
    -------
    molsysmt.MolSys
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

    Examples
    --------
    >>> import gzip
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> import molsysmt as msm
    >>> with TemporaryDirectory() as directory:
    ...     path = Path(directory) / 'observed.pdb.gz'
    ...     source = Path(msm.systems['T4 lysozyme L99A']['181l.pdb'])
    ...     _ = path.write_bytes(gzip.compress(source.read_bytes()))
    ...     molsys = msm.convert(path, to_form='molsysmt.MolSys',
    ...                          get_missing_bonds=False)
    ...     print(molsys.topology.n_atoms)
    1441

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys import (
        to_molsysmt_MolSys as convert_handler,
    )

    from ._read import read_handler

    handler = read_handler(item)
    try:
        return convert_handler(
            handler,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            get_missing_bonds=get_missing_bonds,
            bond_inference_engine=bond_inference_engine,
            skip_digestion=True,
        )
    finally:
        handler.close()
