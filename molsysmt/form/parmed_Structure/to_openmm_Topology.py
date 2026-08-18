from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.Structure')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to openmm.Topology.

    Parameters
    ----------
    item : parmed.Structure
        Source item in parmed.Structure form.
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

    from ..openmm_Topology.extract import extract as extract_openmm_Topology

    tmp_item = item.topology
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

