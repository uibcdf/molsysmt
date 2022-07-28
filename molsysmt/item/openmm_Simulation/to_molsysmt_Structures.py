from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Context as openmm_Simulation_to_openmm_Context
    from molsysmt.item.openmm_Context import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    tmp_item = openmm_Simulation_to_openmm_Context(item)
    tmp_item = openmm_Context_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

