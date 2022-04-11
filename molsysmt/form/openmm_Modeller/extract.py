from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'openmm.Modeller')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from openmm.app import Modeller

    if (atom_indices is 'all') and (structure_indices is 'all'):

        tmp_item = Modeller(item.topology, item.positions)

    else:

        from . import get_coordinates_from_atom
        from ..openmm_Topology import extract as extract_openmm_Topology

        tmp_topology = extract_openmm_Topology(item.topology, atom_indices=atom_indices)
        tmp_positions = get_coordinates_from_atom(item, indices=atom_indices)
        tmp_item = Modeller(tmp_topology, tmp_positions)

    return tmp_item

