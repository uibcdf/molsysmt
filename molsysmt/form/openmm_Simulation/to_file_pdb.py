from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from openmm.Simulation to file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:pdb
        Resulting object in file:pdb form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology as openmm_Simulation_to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_file_pdb import to_file_pdb as openmm_Topology_to_file_pdb
    from . import get_coordinates_from_atom
    from . import get_box_from_system

    topology = openmm_Simulation_to_openmm_Topology(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    box = get_box_from_system(item, structure_indices=structure_indices, skip_digestion=True)
    topology.setPeriodicBoxVectors(box)

    tmp_item = openmm_Topology_to_file_pdb(topology, coordinates=coordinates, output_filename=output_filename,
                                           skip_digestion=True)

    return tmp_item

