from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):
    """
    Converting from file:pdb to molsysmt.PDBFileHandler.

    Parameters
    ----------
    item : file:pdb
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.PDBFileHandler
        Converted molecular system representation.
    """

    from molsysmt.native import PDBFileHandler

    return PDBFileHandler(str(item), io_mode='r')

