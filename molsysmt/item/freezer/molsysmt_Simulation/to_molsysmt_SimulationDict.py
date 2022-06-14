def to_molsysmt_SimulationDict(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_Simulation import is_molsysmt_Simulation
    from molsysmt.basic import convert

    if not is_molsysmt_Simulation(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.SimulationDict', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

