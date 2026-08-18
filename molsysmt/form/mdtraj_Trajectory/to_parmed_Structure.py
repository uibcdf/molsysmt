from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to parmed.Structure.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_parmed_Structures import to_parmed_Structures as openmm_Topology_to_parmed_Structures

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_parmed_Structures(tmp_item, skip_digestion=True)

    return tmp_item

