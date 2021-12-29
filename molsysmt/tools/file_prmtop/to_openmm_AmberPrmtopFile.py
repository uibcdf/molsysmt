def to_openmm_AmberPrmtopFile(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_prmtop import is_file_prmtop
    from molsysmt.basic import convert

    if not is_file_prmtop(item):
        raise ValueError

    tmp_item = convert(item, 'openmm.AmberPrmtopFile', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

