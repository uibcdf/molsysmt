from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb")
def to_molsysmt_MolSys(
    item,
    atom_indices="all",
    structure_indices="all",
    skip_digestion=False,
    *,
    get_missing_bonds=True,
):
    """
    Converting from file:pdb to molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        PDB file to read.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    get_missing_bonds : bool, default=True
        Whether to request the existing optional OpenMM connectivity inference.
        If False, retain only bonds declared by PDB records, without invoking
        the inference engine.

    Returns
    -------
    molsysmt.MolSys
        Native molecular system with preserved atom identity and coordinates.
        PDB coordinates and box lengths are expressed in the configured length
        units; inference does not establish complete chemical assignments.

    Notes
    -----
    The existing True default remains dependent on optional OpenMM availability.
    Use False for an explicit-only graph independent of that engine.

    Examples
    --------
    >>> import molsysmt as msm
    >>> path = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> molsys = msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    >>> msm.get(molsys, n_bonds=True)
    13


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_MolSys import (
        to_molsysmt_MolSys as molsysmt_PDBFileHandler_to_molsysmt_MolSys,
    )
    from molsysmt.form.molsysmt_PDBFileHandler.to_molsysmt_PDBFileHandler import (
        to_molsysmt_PDBFileHandler,
    )

    handler = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    try:
        tmp_item = molsysmt_PDBFileHandler_to_molsysmt_MolSys(
            handler,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            get_missing_bonds=get_missing_bonds,
            skip_digestion=True,
        )
    finally:
        handler.close()

    return tmp_item
