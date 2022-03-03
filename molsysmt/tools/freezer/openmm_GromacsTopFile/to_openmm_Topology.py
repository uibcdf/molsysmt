def to_openmm_Topology(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.openmm_GromacsTopFile import is_openmm_GromacsTopFile
    from molsysmt.basic import convert

    if not is_openmm_GromacsTopFile(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm.Topology', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

