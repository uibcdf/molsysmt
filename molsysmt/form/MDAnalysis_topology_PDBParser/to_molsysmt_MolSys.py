from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='MDAnalysis.topology.PDBParser')
@dep_digest('MDAnalysis')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from MDAnalysis import Universe
    from molsysmt.form.MDAnalysis_Universe.to_molsysmt_MolSys import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_MolSys

    tmp_item = Universe(item.filename)

    return MDAnalysis_Universe_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                   structure_indices=structure_indices, skip_digestion=True)
