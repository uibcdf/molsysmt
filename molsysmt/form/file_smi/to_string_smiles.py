from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:smi')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from file:smi to string:smiles.


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

    results = []
    with open(item, 'r') as fff:
        for line in fff:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            smiles = line.split()[0]
            results.append('smiles:' + smiles)

    if len(results) == 1:
        return results[0]

    return results
