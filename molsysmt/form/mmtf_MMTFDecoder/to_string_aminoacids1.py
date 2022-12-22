from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_string_aminoacids1(item, group_indices='all', digest=True):

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    tmp_item = to_molsysmt_Topology(item, digest=False)
    tmp_item = molsysmt_Topology_to_string_aminoacids1(tmp_item, group_indices=group_indices, digest=False)

    return tmp_item

