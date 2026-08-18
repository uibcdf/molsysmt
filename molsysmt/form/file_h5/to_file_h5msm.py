from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5')
def to_file_h5msm(item, atom_indices='all', structure_indices='all', output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single',
                  skip_digestion=False):
    """
    Converting from file:h5 to file:h5msm.


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
    compression : object, default='gzip'
        Argument compression.
    compression_opts : object, default=4
        Argument compression_opts.
    int_precision : object, default='single'
        Argument int_precision.
    float_precision : object, default='single'
        Argument float_precision.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:h5msm
        Resulting object in file:h5msm form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm as molsysmt_MolSys_to_file_h5msm

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                  structure_indices=structure_indices, skip_digestion=True)
    return molsysmt_MolSys_to_file_h5msm(tmp_item, output_filename=output_filename,
            compression=compression, compression_opts=compression_opts,
            int_precision=int_precision, float_precision=float_precision,
            skip_digestion=True)
