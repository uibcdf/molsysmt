from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MoleculeMechanics')
def to_molsysmt_MolecularMechanics(item, copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.MolecularMechanics to molsysmt.MolecularMechanics.

    Parameters
    ----------
    item : molsysmt.MolecularMechanics
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.MolecularMechanics
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, copy_if_all=copy_if_all, skip_digestion=True)

