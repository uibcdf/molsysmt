def to_parmed_GromacsTopologyFile(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.molsysmt_Trajectory import is_molsysmt_Trajectory
    from molsysmt.basic import convert

    if not is_molsysmt_Trajectory(item):
        raise ValueError

    tmp_item = convert(item, to_form='parmed.GromacsTopologyFile', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

