from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def to_molsysmt_MolecularMechanics(
    item,
    atom_indices="all",
    structure_indices="all",
    discard_torsion_tree=True,
    skip_digestion=False,
):
    """Converting explicit PDBQT data into native MolecularMechanics data.

    Parameters
    ----------
    item : str or pathlib.Path
        PDBQT path containing one supported rigid receptor or ligand.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include; serials remain string IDs.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL IDs; serialized selections must be nonempty and unique.
    discard_torsion_tree : bool, default=True
        Authorize omission of the format-specific torsion tree. A full MolSys
        conversion requires explicit True for a ligand with ROOT. Reduced
        domains project their own attributes and omit the tree by default.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    molsysmt.MolecularMechanics
        Selected native data. Coordinates are converted from angstroms through
        PyUnitWizard; partial charges are native values in elementary charge.

    Notes
    -----
    No charges or atom types are assigned; every present hydrogen is retained.
    BRANCH supplies only some covalent edges with unknown orders. Connectivity
    is partial; aromaticity and formal charges remain unknown. No torsion tree
    or arbitrary REMARK metadata is stored in a native domain. Use
    get_torsion_tree() and keep the source for lossless format metadata.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(item, storage_mode="indexed") as handler:
        return handler._domain(
            "molecular_mechanics", atom_indices, structure_indices, discard_torsion_tree
        )
