from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_string_aminoacids3(item, group_indices='all', digest=True):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = to_molsysmt_Topology(item, digest=False)
    tmp_item = molsysmt_Topology_to_string_aminoacids3(tmp_item, group_indices=group_indices, digest=False)

    return tmp_item

