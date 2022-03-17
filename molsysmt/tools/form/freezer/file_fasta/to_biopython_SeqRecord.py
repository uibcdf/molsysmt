def to_biopython_SeqRecord(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_fasta import is_file_fasta
    from molsysmt.basic import convert

    if not is_file_fasta(item):
        raise ValueError

    tmp_item = convert(item, 'biopython.SeqRecord', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

