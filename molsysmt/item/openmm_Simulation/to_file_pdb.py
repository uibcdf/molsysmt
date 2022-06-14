from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'openmm.Simulation')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_openmm_Topology as openmm_Simulation_to_openmm_Topology
    from molsysmt.item.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb
    from . import get_coordinates_from_atom
    from . import get_box_from_system

    topology = openmm_Simulation_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    box = get_box_from_system(item, structure_indices=structure_indices)
    topology.setPeriodicBoxVectors(box)

    tmp_item = openmm_Topology_to_file_pdb(topology, coordinates=coordinates, output_filename=output_filename)

    return tmp_item

