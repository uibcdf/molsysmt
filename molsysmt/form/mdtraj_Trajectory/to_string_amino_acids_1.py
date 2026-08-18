from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_string_amino_acids_1(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to string.amino.acids.1.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    string.amino.acids.1
        Converted molecular system representation.
    """

    from molsysmt.form.mdtraj_Topology.to_string_amino_acids_1 import to_string_amino_acids_1 as mdtraj_Topology_to_string_amino_acids_1

    output = mdtraj_Topology_to_string_amino_acids_1(item.topology, atom_indices=atom_indices, skip_digestion=True)

    return output
