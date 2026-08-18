from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def write_topology_in_h5msm(item, file, atom_indices='all', skip_digestion=False):
    """
    Performing write topology in h5msm on form openmm.Topology.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    file : object
        Argument file.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    from ..molsysmt_Topology import write_topology_in_h5msm as write_molsysmt_Topology_in_h5msm

    molsysmt_Topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    write_molsysmt_Topology_in_h5msm(molsysmt_Topology, file, skip_digestion=True)

    pass

