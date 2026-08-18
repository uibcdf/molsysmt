from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_GROFileHandler(item, skip_digestion=False):
    """
    Converting from file:gro to molsysmt.GROFileHandler.

    Parameters
    ----------
    item : file:gro
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.GROFileHandler
        Converted molecular system representation.
    """

    from molsysmt.native import GROFileHandler

    return GROFileHandler(item, io_mode='r')

