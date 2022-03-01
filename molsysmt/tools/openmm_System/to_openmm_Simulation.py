def to_openmm_Simulation(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.openmm_System import is_openmm_System
    from molsysmt.basic import convert

    if not is_openmm_System(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm.Simulation', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

