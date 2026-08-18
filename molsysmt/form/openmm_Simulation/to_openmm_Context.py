from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Context(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to openmm.Context.

    Parameters
    ----------
    item : openmm.Simulation
        Source item in openmm.Simulation form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Context
        Resulting object in openmm.Context form.

    .. versionadded:: 1.0.0
    """

    tmp_item = item.context

    return tmp_item

