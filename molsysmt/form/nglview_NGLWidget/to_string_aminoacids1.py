from molsysmt._private.digestion import digest

@digest(form='nglview.NGLWidget')
def to_string_aminoacids1(item, atom_indices='all'):

    from . import to_molsysmt_Topology
    from ..to_molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topology_to_string_aminoacids1(tmp_item)

    return tmp_item

def _to_string_aminoacids1(item, atom_indices='all', structure_indices='all'):

    return to_string_aminoacids1(item, atom_indices=atom_indices)

