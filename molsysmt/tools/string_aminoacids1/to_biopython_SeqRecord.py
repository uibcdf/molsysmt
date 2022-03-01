def to_biopython_SeqRecord(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.aminoacids1 import is_string_aminoacids1
    from molsysmt.basic import convert

    if not is_string_aminoacids1(item):
        raise ValueError

    tmp_item = convert(item, to_form='biopython.SeqRecord', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

