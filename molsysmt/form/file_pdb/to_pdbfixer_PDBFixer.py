from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdb")
@dep_digest("pdbfixer")
def to_pdbfixer_PDBFixer(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting a PDB file to a PDBFixer object.

    PDBFixer is imported only when this conversion is requested. Its constructor
    reads the PDB file before the requested atom and structure subset is extracted.

    Parameters
    ----------
    item : str
        Path to the PDB file to read.
    atom_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include. Use 'all' to retain every atom.
    structure_indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion and validation mechanism.

    Returns
    -------
    pdbfixer.PDBFixer
        PDBFixer object containing the requested subset.

    Raises
    ------
    LibraryNotFoundError
        If the optional PDBFixer package is unavailable.
    ImportError
        If PDBFixer or one of its dependencies fails to import. The original
        exception is preserved.

    Notes
    -----
    Dependency availability is checked even when ``skip_digestion=True``.

    Examples
    --------
    >>> import molsysmt as msm
    >>> pdb_path = str(msm.systems['Trp-Cage']['1l2y.pdb'])
    >>> molsys = to_pdbfixer_PDBFixer(pdb_path)
    >>> molsys.topology.getNumAtoms()
    304

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Form_pdbfixer_PDBFixer` for PDBFixer capabilities and availability.

    .. versionadded:: 1.0.0
    """

    from pdbfixer.pdbfixer import PDBFixer

    from ..pdbfixer_PDBFixer.extract import extract as extract_pdbfixer_PDBFixer

    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer_PDBFixer(
        tmp_item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    return tmp_item
