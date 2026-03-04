from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:pdb_id')
def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_openmm_Modeller(tmp_item, skip_digestion=True)

    return tmp_item


