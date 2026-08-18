from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('openff.toolkit')
def to_openff_Molecule(item, skip_digestion=False):
    """
    Converting from rdkit.Mol to openff.Molecule.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Molecule
        Resulting object in openff.Molecule form.


    .. versionadded:: 1.0.0
    """

    from openff.toolkit.topology import Molecule

    return Molecule.from_rdkit(item)
