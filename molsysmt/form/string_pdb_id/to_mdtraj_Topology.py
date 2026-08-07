from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.form.string_pdb_id.to_string_pdb_text import to_string_pdb_text
    from molsysmt.form.string_pdb_text.to_mdtraj_Topology import to_mdtraj_Topology as string_pdb_text_to_mdtraj_Topology

    tmp_item = to_string_pdb_text(item, skip_digestion=True)
    tmp_item = string_pdb_text_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item


