from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:top')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from .to_parmed_GromacsTopologyFile import to_parmed_GromacsTopologyFile
    from molsysmt.form.parmed_GromacsTopologyFile.to_molsysmt_MolSys import to_molsysmt_MolSys as parmed_GromacsTopologyFile_to_molsysmt_MolSys

    tmp_item = to_parmed_GromacsTopologyFile(item, skip_digestion=True)
    tmp_item = parmed_GromacsTopologyFile_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                              structure_indices=structure_indices,
                                                              skip_digestion=True)

    return tmp_item
