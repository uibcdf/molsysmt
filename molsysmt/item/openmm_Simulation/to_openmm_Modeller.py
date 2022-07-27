from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Modeller(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'openmm.Simulation')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from openmm.app import Modeller
    from . import to_openmm_Topology
    from . import get_coordiantes_from_atom

    topology = to_openmm_Topology(item, atom_indices=atom_indices)
    positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
    tmp_item = Modeller(topology, positions)

    return tmp_item

