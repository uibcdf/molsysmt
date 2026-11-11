from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:h5msm")
def to_file_h5msm(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
    *,
    format_version=None,
):
    """
    Converting from file:h5msm to file:h5msm.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Destination for the converted file.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    format_version : str or none, default=None
        None retains this adapter's legacy copy/extraction route. An explicit
        '0.5', experimental '0.6', or '1.0' writes the selected schema.

    Returns
    -------
    file:h5msm
        Resulting object in file:h5msm form.


    .. versionadded:: 1.0.0
    """

    if format_version is not None:
        from molsysmt.basic import convert

        return convert(
            item,
            to_form="file:h5msm",
            selection=atom_indices,
            structure_indices=structure_indices,
            output_filename=output_filename,
            format_version=format_version,
        )

    from .extract import extract

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )
