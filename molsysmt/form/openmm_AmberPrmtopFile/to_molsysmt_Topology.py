from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.AmberPrmtopFile')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.AmberPrmtopFile to molsysmt.Topology.

    Parameters
    ----------
    item : openmm.AmberPrmtopFile
        Source item in openmm.AmberPrmtopFile form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.topology
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
