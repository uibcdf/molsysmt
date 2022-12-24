from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', digest=True):

    from openmm.app import Modeller
    from . import to_openmm_Topology
    from . import get_coordiantes_from_atom

    topology = to_openmm_Topology(item, atom_indices=atom_indices, digest=False)
    positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, digest=False)
    tmp_item = Modeller(topology, positions)

    return tmp_item

