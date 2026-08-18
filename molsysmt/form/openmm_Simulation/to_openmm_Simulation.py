from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from openmm.Simulation to openmm.Simulation.

    Parameters
    ----------
    item : openmm.Simulation
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Simulation
        Converted molecular system representation.
    """

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

