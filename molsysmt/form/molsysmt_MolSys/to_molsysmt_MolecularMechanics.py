from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_molsysmt_MolecularMechanics(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanics
        Converted molecular system representation.
    """

    tmp_item = item.molecular_mechanics.copy()

    return tmp_item


