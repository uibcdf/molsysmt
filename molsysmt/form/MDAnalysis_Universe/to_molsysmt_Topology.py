from molsysmt._private.arg_digestion import arg_digest
@arg_digest(form='MDAnalysis.Universe')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.MDAnalysis_Topology.to_molsysmt_Topology import (
        to_molsysmt_Topology as topology_to_molsysmt_Topology,
    )

    return topology_to_molsysmt_Topology(
        item._topology,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
