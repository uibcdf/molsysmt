from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from .get import get_coordinates_from_atom
    from molsysmt import pyunitwizard as puw
    from openmm.app import Modeller

    topology = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)

    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                            skip_digestion=True)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(topology, positions)

    return tmp_item

