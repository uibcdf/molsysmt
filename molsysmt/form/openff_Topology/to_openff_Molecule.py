from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError

@arg_digest(form='openff.Topology')
def to_openff_Molecule(item, skip_digestion=False):
    """
    Converting from openff.Topology to openff.Molecule.


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

    molecules = list(item.molecules)
    if len(molecules) == 1:
        return molecules[0]
    raise NotImplementedMethodError(
        "Cannot convert an openff.Topology with multiple molecules to a single openff.Molecule."
    )
