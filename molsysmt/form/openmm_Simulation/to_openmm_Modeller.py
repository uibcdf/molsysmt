from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to openmm.Modeller.

    Parameters
    ----------
    item : openmm.Simulation
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Modeller
        Converted molecular system representation.
    """

    from openmm.app import Modeller
    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from . import get_coordiantes_from_atom

    topology = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    tmp_item = Modeller(topology, positions)

    return tmp_item

