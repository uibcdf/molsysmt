from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.Modeller')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, digest=True):

    from openmm.app import Modeller

    if is_all(atom_indices) and is_all(structure_indices):

        tmp_item = Modeller(item.topology, item.positions)

    else:

        from . import get_coordinates_from_atom
        from ..openmm_Topology import extract as extract_openmm_Topology

        tmp_topology = extract_openmm_Topology(item.topology, atom_indices=atom_indices, digest=False)
        tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, digest=False)
        tmp_item = Modeller(tmp_topology, tmp_positions)

    return tmp_item

