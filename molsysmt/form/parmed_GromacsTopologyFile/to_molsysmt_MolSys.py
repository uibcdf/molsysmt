from molsysmt._private.argdigest import arg_digest

@arg_digest(form='parmed.GromacsTopologyFile')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.parmed_Structure.to_molsysmt_MolSys import to_molsysmt_MolSys as parmed_Structure_to_molsysmt_MolSys

    return parmed_Structure_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices, skip_digestion=True)
