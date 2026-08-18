from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Molecule')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from openff.Molecule to string.smiles.

    Parameters
    ----------
    item : openff.Molecule
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.smiles
        Converted molecular system representation.
    """

    return 'smiles:' + item.to_smiles()
