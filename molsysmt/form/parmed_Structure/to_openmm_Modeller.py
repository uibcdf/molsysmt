from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to openmm.Modeller.

    Parameters
    ----------
    item : parmed.Structure
        Source item in parmed.Structure form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom, get_box_from_system
    from molsysmt.form.openmm_Topology.to_openmm_Modeller import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

