from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:gro')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all',
                       skip_digestion=False):
    """
    Converting from file:gro to molsysmt.Structures.

    Parameters
    ----------
    item : file:gro
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler
    from molsysmt.form.molsysmt_GROFileHandler.to_molsysmt_Structures import to_molsysmt_Structures as molsysmt_GROFileHandler_to_molsysmt_Structures

    tmp_item = to_molsysmt_GROFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_GROFileHandler_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices,
                                                          structure_indices=structure_indices,
                                                          skip_digestion=True)

    return tmp_item

