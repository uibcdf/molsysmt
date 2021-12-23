def to_file_msmpk(item, selection='all', model_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.string_pdb_id import is_string_pdb_id
    from molsysmt.tools.file_msmpk import is_file_msmpk
    from molsysmt.basic import convert

    if not is_string_pdb_id(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    if not is_file_msmpk(output_filename):
        raise ValueError

    tmp_item = convert(item, output_filename, selection=selection, frame_indices=model_indices, syntaxis=syntaxis)

    return tmp_item

