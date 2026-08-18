from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Topology')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Topology to openmm.Topology.


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
    openmm.Topology
        Resulting object in openmm.Topology form.


    .. versionadded:: 1.0.0
    """

    from ..openmm_Topology.extract import extract as extract_openmm_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    if not isinstance(item, mdtraj_Topology):
        if hasattr(item, 'topology'):
            item = item.topology
        else:
            from .to_mdtraj_Topology import to_mdtraj_Topology
            item = to_mdtraj_Topology(item, skip_digestion=True)

    tmp_item = item.to_openmm()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)

    return tmp_item

