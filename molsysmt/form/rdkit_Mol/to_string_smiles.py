from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('rdkit')
def to_string_smiles(item, skip_digestion=False):
    """
    Converting from rdkit.Mol to string.smiles.

    Parameters
    ----------
    item : rdkit.Mol
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.smiles
        Converted molecular system representation.
    """

    from rdkit import Chem

    canonical = Chem.MolToSmiles(item)

    return 'smiles:' + canonical
