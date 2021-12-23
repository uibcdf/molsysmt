def to_file_mmtf(item, selection='all', model_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.string_pdb_id import is_string_pdb_id
    from molsysmt.tools.file_mmtf import is_file_mmtf
    from molsysmt.basic import convert

    if not is_string_pdb_id(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    if not is_file_mmtf(output_filename):
        raise ValueError

    tmp_item = convert(item, output_filename, selection=selection, frame_indices=model_indices, syntaxis=syntaxis)

    return tmp_item

