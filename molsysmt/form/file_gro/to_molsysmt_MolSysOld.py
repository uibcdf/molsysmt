from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_MolSysOld(item, atom_indices='all', structure_indices='all'):

    from . import to_mdtraj_Trajectory
    from ..mdtraj_Trajectory import to_molsysmt_MolSysOld as mdtraj_Trajectory_to_molsysmt_MolSysOld

    tmp_item = to_mdtraj_Trajectory(item)
    tmp_item = mdtraj_Trajectory_to_molsysmt_MolSysOld(tmp_item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)

    return tmp_item

