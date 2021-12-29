def to_file_mol2(item, selection='all', frame_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.file_pdb import is_file_pdb
    from molsysmt.tools.file_mol2 import is_file_mol2
    from molsysmt.basic import convert

    if not is_file_pdb(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    if not is_file_mol2(output_filename):
        raise ValueError

    tmp_item = convert(item, output_filename, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

