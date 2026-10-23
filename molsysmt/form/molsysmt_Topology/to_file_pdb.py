from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
def to_file_pdb(
    item,
    coordinates,
    box=None,
    atom_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from molsysmt.Topology to file:pdb.


    Parameters
    ----------
    item : molecular system
        Native topology to serialize together with explicit coordinates.
    coordinates : object
        Length quantity with shape (n_structures, n_atoms, 3) on the full source
        atom axis. Values are converted to PDB angstroms by the native writer.
    box : object, default=None
        Optional length quantity containing row-vector periodic cells.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from tempfile import TemporaryDirectory
    >>> source = msm.systems["T4 lysozyme L99A"]["181l.pdb"]
    >>> molsys = msm.convert(source, get_missing_bonds=False)
    >>> with TemporaryDirectory() as directory:
    ...     output = to_file_pdb(molsys.topology,
    ...                          coordinates=molsys.structures.coordinates,
    ...                          output_filename=f"{directory}/export.pdb")
    ...     assert msm.get_form(output) == 'file:pdb'

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.string_pdb_text.to_file_pdb import to_file_pdb as write_text

    from .to_string_pdb_text import to_string_pdb_text

    text = to_string_pdb_text(
        item,
        atom_indices=atom_indices,
        coordinates=coordinates,
        box=box,
        skip_digestion=True,
    )
    return write_text(text, output_filename=output_filename, skip_digestion=True)
