def to_openmm_Topology(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.openmm_GromacsTopFile import is_openmm_GromacsTopFile
    from molsysmt.basic import convert

    if not is_openmm_GromacsTopFile(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm.Topology', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

