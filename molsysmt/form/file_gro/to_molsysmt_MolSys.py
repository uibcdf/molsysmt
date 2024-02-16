from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mdtraj_Trajectory
    from ..mdtraj_Trajectory import to_molsysmt_MolSys as mdtraj_Trajectory_to_molsysmt_MolSys

    tmp_item = to_mdtraj_Trajectory(item, skip_digestion=True)
    tmp_item = mdtraj_Trajectory_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

