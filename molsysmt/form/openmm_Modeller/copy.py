from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def copy(item, skip_digestion=False):
    """
    Creating a copy of an item of form openmm.Modeller.

    Parameters
    ----------
    item : openmm.Modeller
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Modeller
        Copied item.
    """

    from openmm.app import Modeller

    tmp_item = Modeller(item.topology, item.positions)

    return tmp_item

