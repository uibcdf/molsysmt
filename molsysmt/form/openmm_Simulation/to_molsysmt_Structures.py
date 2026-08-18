from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to molsysmt.Structures.

    Parameters
    ----------
    item : openmm.Simulation
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Structures
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Context.to_openmm_Context import to_openmm_Context as openmm_Simulation_to_openmm_Context
    from molsysmt.form.openmm_Context.to_molsysmt_Structures import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    tmp_item = openmm_Simulation_to_openmm_Context(item)
    tmp_item = openmm_Context_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

