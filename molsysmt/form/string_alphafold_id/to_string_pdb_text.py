from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:alphafold_id')
def to_string_pdb_text(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)

    tmp_item = molsysmt_MolSys_to_string_pdb_text(tmp_item, skip_digestion=True)

    return tmp_item

