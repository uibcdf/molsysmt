def to_pdbfixer_PDBFixer(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_pdb import is_file_pdb
    from molsysmt.basic import convert

    if not is_file_pdb(item):
        raise ValueError

    tmp_item = convert(item, 'pdbfixer.PDBFixer', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

