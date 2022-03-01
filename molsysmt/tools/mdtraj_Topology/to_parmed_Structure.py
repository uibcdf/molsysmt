def to_parmed_Structure(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.mdtraj_Topology import is_mdtraj_Topology
    from molsysmt.basic import convert

    if not is_mdtraj_Topology(item):
        raise ValueError

    tmp_item = convert(item, to_form='parmed.Structure', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

