from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all',
                       skip_digestion=False):
    """
    Converting from file:gro to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler
    from molsysmt.form.molsysmt_GROFileHandler.to_molsysmt_Structures import to_molsysmt_Structures as molsysmt_GROFileHandler_to_molsysmt_Structures

    tmp_item = to_molsysmt_GROFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_GROFileHandler_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          skip_digestion=True)

    return tmp_item

