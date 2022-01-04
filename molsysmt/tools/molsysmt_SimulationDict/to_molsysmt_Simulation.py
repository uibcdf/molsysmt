def to_molsysmt_Simulation(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_SimulationDict import is_molsysmt_SimulationDict
    from molsysmt.basic import convert

    if not is_molsysmt_SimulationDict(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Simulation', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

