from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pdb')
def to_molsysmt_PDBFileHandler(item, skip_digestion=False):
    """
    Converting from file:pdb to molsysmt.PDBFileHandler.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.PDBFileHandler
        Resulting object in molsysmt.PDBFileHandler form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native import PDBFileHandler

    return PDBFileHandler(str(item), io_mode='r')

