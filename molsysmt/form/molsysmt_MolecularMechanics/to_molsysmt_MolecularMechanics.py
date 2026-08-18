from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MoleculeMechanics')
def to_molsysmt_MolecularMechanics(item, copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.MolecularMechanics to molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item in molsysmt.MolecularMechanics form.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolecularMechanics
        Resulting object in molsysmt.MolecularMechanics form.

    .. versionadded:: 1.0.0
    """

    from .extract import extract

    return extract(item, copy_if_all=copy_if_all, skip_digestion=True)

