from molsysmt._private.digestion import digest
import numpy as np

@digest(form='mdtraj.Trajectory')
def to_string_aminoacids3(item, atom_indices='all', skip_digestion=False):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3

    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_string_aminoacids3(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

