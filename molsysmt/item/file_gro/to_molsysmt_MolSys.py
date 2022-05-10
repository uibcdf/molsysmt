from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        digest_item(item, 'file:gro')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mdtraj_Trajectory
    from ..mdtraj_Trajectory import to_molsysmt_MolSys as mdtraj_Trajectory_to_molsysmt_MolSys

    tmp_item = to_mdtraj_Trajectory(item, check=False)
    tmp_item = mdtraj_Trajectory_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, check=False)

    return tmp_item

