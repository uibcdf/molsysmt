def to_mdtraj_Topology(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.mdtraj_HDF5TrajectoryFile import is_mdtraj_HDF5TrajectoryFile
    from molsysmt.basic import convert

    if not is_mdtraj_HDF5TrajectoryFile(item):
        raise ValueError

    tmp_item = convert(item, to_form='mdtraj.Topology', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

