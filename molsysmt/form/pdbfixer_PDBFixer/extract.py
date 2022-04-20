from molsysmt._private.digestion import digest_item, atom_indices, structure_indices

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        digest_item(item, 'pdbfixer.PDBFixer')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from . import to_openmm_Topology
        from . import get_coordinates_from_atom, get_box_from_atom
        from ..openmm_Topology import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, check=False)
        coordinates = get_coordinates_from_atom(tmp_item, atom_indices=atom_indices, check=False)
        box = get_box_from_atom(tmp_item, check=False)
        tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates, box=box, check=False)

    return tmp_item

