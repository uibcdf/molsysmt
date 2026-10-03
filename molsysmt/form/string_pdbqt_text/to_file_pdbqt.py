from molsysmt._private.argdigest import arg_digest


@arg_digest(form="string:pdbqt_text")
def to_file_pdbqt(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """Copying validated PDBQT contents into a file.

    Parameters
    ----------
    item : str
        Explicit pdbqt_text: string containing one supported PDBQT system.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom indices (0-based) to include; serials remain string IDs.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Only zero exists in the supported profile.
    output_filename : str or pathlib.Path, default=None
        Destination path; required for file output. Validation precedes writing.
    skip_digestion : bool, default=False
        Whether to skip argument digestion. Default is False.

    Returns
    -------
    str or pathlib.Path
        Destination path.

    Notes
    -----
    Identity conversions preserve the original payload, tree, remarks and atom
    order. Rigid subsets use validated native projection. Tree subsets require
    an explicit remapped tree through the native writer and are rejected here.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.pdbqt_adapter import selected_payload, write_payload

    payload = selected_payload(item, atom_indices, structure_indices, text=True)
    return write_payload(payload, output_filename)
