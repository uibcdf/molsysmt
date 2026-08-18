from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.PDBFile')
def to_mdtraj_Topology(item, atom_indices='all', syntax='MolSysMT', skip_digestion=False):
    """
    Converting from openmm.PDBFile to mdtraj.Topology.

    Parameters
    ----------
    item : openmm.PDBFile
        Source item in openmm.PDBFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection`.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_mdtraj_Topology import to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item

