def to_openmm_Simulation(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_pdb import is_file_pdb
    from molsysmt.basic import convert

    if not is_file_pdb(item):
        raise ValueError

    tmp_item = convert(item, 'openmm.Simulation', selection=selection, frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

