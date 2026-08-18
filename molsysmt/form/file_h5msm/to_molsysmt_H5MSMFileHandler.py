from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_H5MSMFileHandler(item, skip_digestion=False):
    """
    Converting from file:h5msm to molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Resulting object in molsysmt.H5MSMFileHandler form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import H5MSMFileHandler

    return H5MSMFileHandler(item, io_mode='r')
