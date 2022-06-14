from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_nglview_NGLWidget(item, atom_indices='all', structure_indices='all', syntaxis='MolSysMT'):

    if check:

        digest_item(item, 'openmm.PDBFile')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology import to_nglview_NGLWidget as openmm_Topology_to_nglview_NGLWidget

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_nglview_NGLWidget(tmp_item, coordinates=coordinates, check=False)

    return tmp_item

