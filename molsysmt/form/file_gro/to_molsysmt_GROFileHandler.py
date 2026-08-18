from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_GROFileHandler(item, skip_digestion=False):
    """
    Converting from file:gro to molsysmt.GROFileHandler.

    Parameters
    ----------
    item : file:gro
        Source item in file:gro form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.GROFileHandler
        Resulting object in molsysmt.GROFileHandler form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import GROFileHandler

    return GROFileHandler(item, io_mode='r')

