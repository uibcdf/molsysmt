def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from molsysmt._private_tools.exceptions import WrongFormError
    from molsysmt.tools.mdtraj_Trajectory import is_mdtraj_Trajectory
    from molsysmt.native.molsys import MolSys
    from molsysmt.tools.mdtraj_Trajectory import to_molsysmt_Topology as mdtraj_Trajectory_to_molsysmt_Topology
    from molsysmt.tools.mdtraj_Trajectory import to_molsysmt_Structures as mdtraj_Trajectory_to_molsysmt_Structures
    from molsysmt.basic import convert

    if not is_mdtraj_Trajectory(item):
        raise WrongFormError('mdtraj.Trajectory')

    tmp_item = MolSys()
    tmp_item.topology = mdtraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.trajectory = mdtraj_Trajectory_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

