def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.native.io.topology.classes import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_pdb as openmm_Topology_to_pdb

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item)
    tmp_item = molsysmt_Topology_to_openmm_Topology(tmp_item)

    return openmm_Topology_to_pdb(tmp_item, output_filepath=output_filepath, trajectory_item=item,
                                 atom_indices=atom_indices, frame_indices=frame_indices)

def from_pdb(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt import convert

    tmp_item = MolSys()
    tmp_item.topology = convert(item, to_form='molsysmt.Topology', selection=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = convert(item, to_form='molsysmt.Trajectory', selection=atom_indices, frame_indices=frame_indices)

    return tmp_item

