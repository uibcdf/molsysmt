from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('rdkit')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from rdkit.Mol to string:smiles.

    Parameters
    ----------
    item : rdkit.Mol
        Source item in rdkit.Mol form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:smiles
        Resulting object in string:smiles form.

    .. versionadded:: 1.0.0
    """

    from rdkit import Chem

    canonical = Chem.MolToSmiles(item)

    return 'smiles:' + canonical
