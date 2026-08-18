from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.PDBTrajectoryFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.PDBTrajectoryFile to molsysmt.MolSys.

    Parameters
    ----------
    item : mdtraj.PDBTrajectoryFile
        Source item in mdtraj.PDBTrajectoryFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys
    from .to_molsysmt_Structures import to_molsysmt_Structures
    from .to_mdtraj_Topology import to_mdtraj_Topology
    from molsysmt.form.mdtraj_Topology.to_molsysmt_Topology import to_molsysmt_Topology

    tmp_item = MolSys()
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)
    mdtraj_topology = to_mdtraj_Topology(item, skip_digestion=True)
    tmp_item.topology = to_molsysmt_Topology(mdtraj_topology, skip_digestion=True)

    return tmp_item
