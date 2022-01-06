def to_openmm_Modeller(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.openmm_Topology import is_openmm_Topology
    from molsysmt.basic import convert

    if not is_openmm_Topology(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm.Modeller', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

