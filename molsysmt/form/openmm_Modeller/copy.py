from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import Modeller

    tmp_item = Modeller(item.topology, item.positions)

    return tmp_item

