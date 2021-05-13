def to_file_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.native.io.molsys.classes import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_file_pdb(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)

    return tmp_item, tmp_molecular_system

def from_file_pdb(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_file_pdb as file_pdb_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.files import from_file_pdb as file_pdb_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = file_pdb_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = file_pdb_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

