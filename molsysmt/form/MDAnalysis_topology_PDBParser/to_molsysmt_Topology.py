from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from MDAnalysis import Universe
    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_Topology import to_molsysmt_Topology as MDAnalysis_Universe_to_molsysmt_Topology

    tmp_item = Universe(item.filename)

    return MDAnalysis_Universe_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)
