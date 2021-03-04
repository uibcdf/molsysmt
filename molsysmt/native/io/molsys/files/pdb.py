def to_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filepath=None):

    from molsysmt.native.io.molsys.classes import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_pdb as openmm_Topology_to_pdb

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item)

    return openmm_Topology_to_pdb(tmp_item, output_filepath=output_filepath, trajectory_item=item,
                                 atom_indices=atom_indices, frame_indices=frame_indices)

def from_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.files import from_pdb as pdb_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.files import from_pdb as pdb_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = pdb_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = pdb_to_molsysmt_Trajectory(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

