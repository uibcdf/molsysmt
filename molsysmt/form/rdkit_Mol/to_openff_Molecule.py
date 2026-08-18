from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('openff.toolkit')
def to_openff_Molecule(item, skip_digestion=False):
    """
    Converting from rdkit.Mol to openff.Molecule.

    Parameters
    ----------
    item : rdkit.Mol
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openff.Molecule
        Converted molecular system representation.
    """

    from openff.toolkit.topology import Molecule

    return Molecule.from_rdkit(item)
