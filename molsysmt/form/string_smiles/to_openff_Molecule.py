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
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Molecule
        Resulting object in openff.Molecule form.

    .. versionadded:: 1.0.0
    """

    from openff.toolkit.topology import Molecule

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item
    return Molecule.from_smiles(smiles)
