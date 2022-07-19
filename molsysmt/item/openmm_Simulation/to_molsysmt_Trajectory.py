def to_molsysmt_Structures(item, selection='all', structure_indices='all', syntax='MolSysMT'):

    from molsysmt.tools.openmm_Simulation import is_openmm_Simulation
    from molsysmt.basic import convert

    if not is_openmm_Simulation(item):
        raise ValueError

    tmp_item = convert(item, to_form='molsysmt.Trajectory', selection=selection, structure_indices=structure_indices,
                       syntax=syntax)

    return tmp_item

