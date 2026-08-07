from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.openmm_PDBFile import to_openmm_PDBFile
    from molsysmt.form.openmm_PDBFile import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item = to_openmm_PDBFile(item, skip_digestion=True)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

