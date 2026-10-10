from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdb_text")
def to_file_pdb(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from string:pdb_text to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    Notes
    -----
    Without an output filename, the adapter generates a file and owns it until
    writing and closing succeed. Failure or interruption retires that generated
    file; successful output belongs to the caller. Explicit output paths are
    never removed on failure and may contain partial writes. Cleanup errors
    propagate. The high-level conversion dispatcher requires an explicit output
    filename for file targets.

    Examples
    --------
    Creating a file from bundled PDB text and retiring the caller-owned result:

    >>> import molsysmt as msm
    >>> from pathlib import Path
    >>> from molsysmt.form.string_pdb_text.to_file_pdb import to_file_pdb
    >>> pdb_text = Path(msm.systems["T4 lysozyme L99A"]["181l.pdb"]).read_text()
    >>> output = Path(to_file_pdb(pdb_text))
    >>> output.read_text() == pdb_text
    True
    >>> output.unlink()

    .. versionadded:: 1.0.0
    """

    from pathlib import Path

    from molsysmt._private.files_and_directories import temp_filename

    from . import extract

    tmp_item = extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        copy_if_all=False,
        skip_digestion=True,
    )

    generated_output = output_filename is None
    if generated_output:
        output_filename = temp_filename(extension="pdb")

    try:
        with open(output_filename, "w") as fff:
            fff.write(tmp_item)
    except BaseException:
        if generated_output:
            Path(output_filename).unlink(missing_ok=True)
        raise

    return output_filename
