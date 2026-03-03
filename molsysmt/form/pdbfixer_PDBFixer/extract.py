from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='pdbfixer.PDBFixer')
@dep_digest('pdbfixer')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:
            from copy import deepcopy
            tmp_item = deepcopy(item)
        else:
            tmp_item = item
    else:

        from ..openmm_Topology.to_openmm_Topology import to_openmm_Topology
        from . import get_coordinates_from_atom
        from ..openmm_Topology.to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

        coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices,
                                                skip_digestion=True)
        tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                      skip_digestion=True)
        tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates, skip_digestion=True)

    return tmp_item
