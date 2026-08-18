from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest(form='mdtraj.Trajectory')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to string:amino_acids_3.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item in mdtraj.Trajectory form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.mdtraj_Topology.to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_string_amino_acids_3 import to_string_amino_acids_3 as mdtraj_Topology_to_string_amino_acids_3

    tmp_item = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_string_amino_acids_3(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

