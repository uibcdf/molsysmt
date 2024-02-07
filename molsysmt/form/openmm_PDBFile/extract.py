from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='openmm.PDBFile')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from . import to_openmm_Topology
        from . import get_coordinates_from_atom, get_box_from_atom
        from ..openmm_Topology import to_openmm_PDBFile as openmm_Topology_to_openmm_PDBFile

        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
        coordinates = get_coordinates_from_atom(tmp_item, atom_indices=atom_indices, skip_digestion=True)
        box = get_box_from_atom(tmp_item, skip_digestion=True)
        tmp_item = openmm_Topology_to_openmm_PDBFile(tmp_item, coordinates=coordinates, box=box, skip_digestion=True)

    return tmp_item

