from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdb_id")
def to_file_cif(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from string:pdb_id to file:cif.


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
    file:cif
        Resulting object in file:cif form.


    Notes
    -----
    Download and extraction use owned staging beside the destination. Failure
    before publication preserves an existing destination and retires staging.
    The parent directory must be writable. Successful output belongs to the
    caller. Cleanup errors propagate, including after publication; publication
    is not rolled back if retiring the empty staging directory fails.

    .. versionadded:: 1.0.0
    """

    import os
    from tempfile import TemporaryDirectory

    from molsysmt.form.string_pdb_id import _extract_pdb_id

    from ..file_cif import download
    from ..file_cif.extract import extract

    pdb_id = _extract_pdb_id(item)
    if output_filename is None:
        output_filename = f"{pdb_id}.cif"

    destination_directory = os.path.dirname(os.path.abspath(output_filename))
    with TemporaryDirectory(
        prefix=".molsysmt-convert-", dir=destination_directory
    ) as scratch:
        staged_filename = os.path.join(scratch, "download.cif")
        tmp_item = download(pdb_id, output_filename=staged_filename)
        tmp_item = extract(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            output_filename=tmp_item,
            copy_if_all=False,
            skip_digestion=True,
        )
        os.replace(tmp_item, output_filename)

    return output_filename
