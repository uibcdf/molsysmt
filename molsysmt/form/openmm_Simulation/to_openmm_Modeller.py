from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from openmm.app import Modeller
    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from .get_structural_attributes import get_coordinates_from_atom

    topology = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                          skip_digestion=True)
    tmp_item = Modeller(topology, positions)

    return tmp_item

