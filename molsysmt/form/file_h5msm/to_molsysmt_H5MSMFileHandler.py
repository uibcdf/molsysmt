from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_H5MSMFileHandler(item, skip_digestion=False):
    """
    Converting from file:h5msm to molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : file:h5msm
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Converted molecular system representation.
    """

    from molsysmt.native import H5MSMFileHandler

    return H5MSMFileHandler(item, io_mode='r')
