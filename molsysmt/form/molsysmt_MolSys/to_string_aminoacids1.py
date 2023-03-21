from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_string_aminoacids1(item, atom_indices='all'):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    tmp_item = to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_string_aminoacids1(tmp_item, atom_indices=atom_indices)

    return tmp_item

