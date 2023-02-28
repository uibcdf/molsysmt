def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all',
                           id=None, name=None, description=None):

    from molsysmt.form.biopython_Seq import to_biopython_SeqRecord as biopython_Seq_to_biopython_SeqRecord

    return biopython_Seq_to_biopython_SeqRecord(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.biopython_Seq import to_file_fasta as biopython_Seq_to_file_fasta

    return biopython_Seq_to_file_fasta(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices,
                                           output_filename=output_filename)
