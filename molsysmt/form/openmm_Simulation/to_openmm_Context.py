from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Context(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to openmm.Context.

    Parameters
    ----------
    item : openmm.Simulation
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Context
        Converted molecular system representation.
    """

    tmp_item = item.context

    return tmp_item

