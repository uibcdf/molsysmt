from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_pytraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to pytraj.Topology.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    pytraj.Topology
        Resulting object in pytraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_pytraj_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_pytraj_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

