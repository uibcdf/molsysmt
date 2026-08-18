from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Simulation')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Simulation to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Context.to_openmm_Context import to_openmm_Context as openmm_Simulation_to_openmm_Context
    from molsysmt.form.openmm_Context.to_molsysmt_Structures import to_molsysmt_Structures as openmm_Context_to_molsysmt_Structures

    tmp_item = openmm_Simulation_to_openmm_Context(item)
    tmp_item = openmm_Context_to_molsysmt_Structures(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item

