from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Topology to parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Resulting object in parmed.Structure form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_parmed_Structure import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item, skip_digestion=True)

    return tmp_item

