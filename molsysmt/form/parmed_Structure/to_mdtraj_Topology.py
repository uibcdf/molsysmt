from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.Structure')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from parmed.Structure to mdtraj.Topology.


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
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.


    .. versionadded:: 1.0.0
    """

    from .to_openmm_Topology import to_openmm_Topology
    from ..openmm_Topology.to_mdtraj_Topology import (
        to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology,
    )

    tmp_item = to_openmm_Topology(
        item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
    tmp_item = openmm_Topology_to_mdtraj_Topology(
        tmp_item,
        skip_digestion=True,
    )

    return tmp_item
