from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Context')
def to_openmm_System(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Context to openmm.System.

    Parameters
    ----------
    item : openmm.Context
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.System
        Converted molecular system representation.
    """

    tmp_item = item.getSystem()

    return tmp_item

