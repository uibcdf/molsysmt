def to_pdbfixer_PDBFixer(item, selection='all', model_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.string_pdb_text import is_string_pdb_text
    from molsysmt.basic import convert

    if not is_string_pdb_text(item):
        raise ValueError

    tmp_item = convert(item, to_form='pdbfixer.PDBFixer', selection=selection, frame_indices=model_indices, syntaxis=syntaxis)

    return tmp_item

