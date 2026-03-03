from molsysmt._private.arg_digestion import arg_digest
import numpy as np

@arg_digest(form='mdtraj.Trajectory')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):

    from ..mdtraj_Topology.to_mdtraj_Topology import to_mdtraj_Topology
    from ..mdtraj_Topology.to_string_amino_acids_3 import to_string_amino_acids_3 as mdtraj_Topology_to_string_amino_acids_3

    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_string_amino_acids_3(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

