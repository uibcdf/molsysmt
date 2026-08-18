from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MoleculeMechanicsDict')
def to_molsysmt_MolecularMechanicsDict(item, copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.MolecularMechanicsDict to molsysmt.MolecularMechanicsDict.

    Parameters
    ----------
    item : molsysmt.MolecularMechanicsDict
        Source item in molsysmt.MolecularMechanicsDict form.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanicsDict
        Resulting object in molsysmt.MolecularMechanicsDict form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, copy_if_all=copy_if_all, skip_digestion=True)

