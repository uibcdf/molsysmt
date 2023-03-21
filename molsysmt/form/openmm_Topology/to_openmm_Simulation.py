from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Simulation(item, atom_indices='all', coordinates=None):

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, coordinates=coordinates)
    tmp_item = openmm_System_to_openmm_Simulation(tmp_item)

    return tmp_item
