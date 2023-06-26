from molsysmt._private.digestion import digest
import numpy as np

@digest(form='nglview.NGLWidget')
def to_string_aminoacids3(item, group_indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3
    from . import get_atom_index_from_group

    atom_indices = get_atom_index_from_group(item, indices=group_indices)
    atom_indices = np.concatenate(atom_indices)
    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topology_to_string_aminoacids3(tmp_item)

    return tmp_item

