from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def to_biopython_SeqRecord(item, atom_indices='all', skip_digestion=False):

    from molsysmt.form.string_aminoacids1.to_string_aminoacids1 import to_string_aminoacids1
    from molsysmt.form.string_aminoacids1.to_biopython_SeqRecord import to_biopython_SeqRecord as string_aminoacids1_to_biopython_SeqRecord

    tmp_item = pdbfixer_PDBFixer_to_string_aminoacids1(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = string_aminoacids1_to_biopython_SeqRecord(tmp_item, skip_digestion=True)

    return tmp_item

