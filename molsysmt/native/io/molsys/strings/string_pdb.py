def to_string_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_openmm_Topology import to_string_pdb as openmm_Topology_to_string_pdb

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system)
    tmp_item, tmp_molecular_system = openmm_Topology_to_string_pdb(tmp_item, molecular_system=tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def from_string_pdb(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native import MolSys
    from molsysmt.native.io.topology.strings import from_string_pdb as string_pdb_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.strings import from_string_pdb as string_pdb_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology, _ = string_pdb_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = string_pdb_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

