def to_openmm_Topology(item, selection='all', frame_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.parmed_GromacsTopologyFile import is_parmed_GromacsTopologyFile
    from molsysmt.basic import convert

    if not is_parmed_GromacsTopologyFile(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm_Topology', selection=selection,
            frame_indices=frame_indices, syntaxis=syntaxis)

    return tmp_item

