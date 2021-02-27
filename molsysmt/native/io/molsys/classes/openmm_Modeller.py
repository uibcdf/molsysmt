def from_openmm_Modeller (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.io.topology.classes import from_openmm_Modeller as openmm_Modeller_to_molsysmt_Topology
    from molsysmt.native.io.trajectory.classes import from_openmm_Modeller as openmm_Modeller_to_molsysmt_Trajectory

    tmp_item = MolSys()
    tmp_item.topology = openmm_Modeller_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item.trajectory = openmm_Modeller_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Modeller (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller
    from .openmm_Topology import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.forms.classes.api_molsysmt_MolSys import get_coordinates_from_atom

    tmp_topology = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices,
                                              frame_indices=frame_indices)

    return Modeller(tmp_topology, tmp_positions[0])

