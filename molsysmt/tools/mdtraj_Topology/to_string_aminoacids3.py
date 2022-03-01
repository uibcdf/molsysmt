def to_string_aminoacids3(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.mdtraj_Topology import is_mdtraj_Topology
    from molsysmt.basic import convert

    if not is_mdtraj_Topology(item):
        raise ValueError

    tmp_item = convert(item, to_form='string:aminoacids3', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

