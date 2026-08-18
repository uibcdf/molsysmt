from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MoleculeMechanicsDict')
def to_molsysmt_MolecularMechanicsDict(item, copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.MolecularMechanicsDict to molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, copy_if_all=copy_if_all, skip_digestion=True)

