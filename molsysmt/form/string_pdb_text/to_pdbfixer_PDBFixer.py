from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdb_text")
@dep_digest("pdbfixer")
def to_pdbfixer_PDBFixer(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting PDB text to a PDBFixer object.

    The requested atom and structure subset is extracted from the PDB text
    before constructing the object. PDBFixer is imported only when this
    conversion is requested.

    Parameters
    ----------
    item : str
        PDB-formatted text containing the molecular system to read.
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
    >>> from pathlib import Path
    >>> import molsysmt as msm
    >>> pdb_path = Path(msm.systems['Trp-Cage']['1l2y.pdb'])
    >>> molsys = to_pdbfixer_PDBFixer(pdb_path.read_text())
    >>> molsys.topology.getNumAtoms()
    304

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Form_pdbfixer_PDBFixer` for PDBFixer capabilities and availability.

    .. versionadded:: 1.0.0
    """

    from io import StringIO

    from pdbfixer.pdbfixer import PDBFixer

    from . import extract

    tmp_item = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.seek(0)
    # tmp_io.close()

    tmp_item = PDBFixer(pdbfile=tmp_io)

    return tmp_item
