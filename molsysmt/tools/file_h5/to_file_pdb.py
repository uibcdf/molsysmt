def to_file_pdb(item, selection='all', frame_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.file_h5 import is_file_h5
    from molsysmt.tools.file_pdb import is_file_pdb
    from molsysmt.basic import convert

    if not is_file_h5(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    if not is_file_pdb(output_filename):
        raise ValueError

    tmp_item = convert(item, output_filename, selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

