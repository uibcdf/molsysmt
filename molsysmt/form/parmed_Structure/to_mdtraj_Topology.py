from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='parmed.Structure')
@dep_digest('mdtraj')
def to_mdtraj_Topology(item, atom_indices='all', skip_digestion=False):

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
