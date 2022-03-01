from molsysmt._private_tools.exceptions import *

def from_pytraj_Trajectory (item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Topology
    from molsysmt.native.io.trajectory import from_pytraj_Trajectory as pytraj_Trajectory_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = pytraj_Trajectory_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.trajectory, _ = pytraj_Trajectory_to_molsysmt_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

