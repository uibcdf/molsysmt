def to_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.api_openmm_Topology import to_openmm_Context as openmm_Topology_to_openmm_Context

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_openmm_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Context(tmp_item, molecular_system=tmp_molecular_system, atom_indices='all', frame_indices=0)

    return tmp_item, tmp_molecular_system

def from_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology import from_openmm_Context as molsysmt_Topology_from_openmm_Context
    from molsysmt.native.io.trajectory import from_openmm_Context as molsysmt_Trajectory_from_openmm_Context

    tmp_item = MolSys()
    tmp_item.topology, _ = molsysmt_Topology_from_openmm_Context(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory, _ = molsysmt_Trajectory_from_openmm_Context(item, atom_indices=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item

