from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to openmm.Topology.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_openmm_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = mdtraj_Topology_to_openmm_Topology(tmp_item, skip_digestion=True)

    return tmp_item
