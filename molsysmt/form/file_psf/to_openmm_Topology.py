from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:psf')
@dep_digest('openmm')
def to_openmm_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:psf to openmm.Topology.

    Parameters
    ----------
    item : file:psf
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_Topology.to_openmm_Topology import (
        to_openmm_Topology as native_to_openmm_Topology,
    )
    from .to_molsysmt_Topology import to_molsysmt_Topology

    topology = to_molsysmt_Topology(
        item, atom_indices=atom_indices, skip_digestion=True
    )
    return native_to_openmm_Topology(topology, skip_digestion=True)
