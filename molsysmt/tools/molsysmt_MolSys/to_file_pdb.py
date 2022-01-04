
def to_file_pdb(item, selection='all', frame_indices='all', output_filename=None, syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_MolSys import is_molsymst_MolSys
    from molsysmt.basic import convert

    if not is_molsysmt_MolSys(item):
        raise ValueError

    if output_filename is None:
        raise ValueError

    tmp_item = convert(item, to_form=output_filename, selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

