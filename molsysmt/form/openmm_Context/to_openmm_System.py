from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Context')
def to_openmm_System(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Context to openmm.System.

    Parameters
    ----------
    item : openmm.Context
        Source item in openmm.Context form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.System
        Resulting object in openmm.System form.

    .. versionadded:: 1.0.0
    """

    tmp_item = item.getSystem()

    return tmp_item

