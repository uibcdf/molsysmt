from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_string_aminoacids1(item, group_indices='all'):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        group_indices = digest_group_indices(group_indices)

    from . import to_molsysmt_Topology
    from ..molsysmt_Topology import to_string_aminoacids1 as molsysmt_Topology_to_string_aminoacids1

    tmp_item = to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_string_aminoacids1(tmp_item, group_indices=group_indices)

    return tmp_item

