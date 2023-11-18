from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.MolSysOld')
def to_string_aminoacids3(item, group_indices='all'):

    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = molsysmt_Topology_to_string_aminoacids3(item.topology, group_indices=group_indices)

    return tmp_item

