from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='pdbfixer.PDBFixer')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from . import to_openmm_Topology
        from . import get_coordinates_from_atom
        from ..openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

        coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices)
        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates)

    return tmp_item
