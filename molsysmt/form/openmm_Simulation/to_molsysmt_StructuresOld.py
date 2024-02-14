from molsysmt._private.digestion import digest

@digest(form='openmm.Simulation')
def to_molsysmt_StructuresOld(item, atom_indices='all', structure_indices='all'):

    from . import to_openmm_Context as openmm_Simulation_to_openmm_Context
    from molsysmt.form.openmm_Context import to_molsysmt_StructuresOld as openmm_Context_to_molsysmt_StructuresOld

    tmp_item = openmm_Simulation_to_openmm_Context(item)
    tmp_item = openmm_Context_to_molsysmt_StructuresOld(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

