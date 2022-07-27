from molsysmt._private.digestion import digest_item, digest_group_indices

def to_string_aminoacids3(item, group_indices='all'):

    if check:

        digest_item(item, 'file:mmtf.MMTFDecoder')
        group_indices = digest_group_indices(atom_indices)

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_string_aminoacids3(tmp_item, group_indices=group_indices)

    return tmp_item

