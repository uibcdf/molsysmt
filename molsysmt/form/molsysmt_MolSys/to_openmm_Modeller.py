from molsysmt._private.digestion import *
from molsysmt.dependencies import requires

@digest(form='molsysmt.MolSys')
@requires('openmm')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from openmm.app import Modeller

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt import pyunitwizard as puw

    tmp_topology = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_positions = puw.convert(tmp_positions, to_form='openmm.unit')

    tmp_item = Modeller(tmp_topology, tmp_positions[0])

    return tmp_item

