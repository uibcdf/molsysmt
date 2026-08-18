from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('openff.toolkit')
def to_openff_Molecule(item, skip_digestion=False):
    """
    Converting from string:smiles to openff.Molecule.

    Parameters
    ----------
    item : string:smiles
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Molecule
        Converted molecular system representation.
    """

    from openff.toolkit.topology import Molecule

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item
    return Molecule.from_smiles(smiles)
