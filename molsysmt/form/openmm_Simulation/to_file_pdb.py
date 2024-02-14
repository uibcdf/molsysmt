from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from . import to_openmm_Topology as openmm_Simulation_to_openmm_Topology
    from molsysmt.form.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb
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

