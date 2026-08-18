from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='mdtraj.Trajectory')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to string.amino.acids.3.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.3
        Converted molecular system representation.
    """

    from molsysmt.form.mdtraj_Topology.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_string_amino_acids_3 import to_string_amino_acids_3 as mdtraj_Topology_to_string_amino_acids_3

    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_string_amino_acids_3(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

