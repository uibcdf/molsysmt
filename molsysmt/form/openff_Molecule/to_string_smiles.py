from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from openff.Molecule to string:smiles.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:smiles
        Resulting object in string:smiles form.


    .. versionadded:: 1.0.0
    """

    return 'smiles:' + item.to_smiles()
