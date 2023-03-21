from molsysmt._private.digestion import digest
import numpy as np

@digest(form='molsysmt.MolSys')
def to_string_aminoacids3(item, atom_indices='all'):

    from ..molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = molsysmt_Topology_to_string_aminoacids3(item.topology, atom_indices=atom_indices)

    return tmp_item

