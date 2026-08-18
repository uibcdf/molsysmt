from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_openmm_System(item, atom_indices='all', structure_indices='all',
        forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005, skip_digestion=False):
    """
    Converting from molsysmt.MolSys to openmm.System.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    forcefield : str, default='AMBER14'
        Force field parameter identifier or name.
    water_model : str, default=None
        Water model parameter identifier (e.g., 'TIP3P').
    implicit_solvent : str, default=None
        Implicit solvent model name if applicable.
    non_bonded_method : object, default='no cutoff'
        Argument non_bonded_method.
    constraints : object, default='hbonds'
        Argument constraints.
    switch_distance : object, default=None
        Argument switch_distance.
    dispersion_correction : object, default=False
        Argument dispersion_correction.
    ewald_error_tolerance : object, default=0.0005
        Argument ewald_error_tolerance.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.System
        Resulting object in openmm.System form.


    .. versionadded:: 1.0.0
    """

    # The sibling converter, which turns *this* form into an openmm.Topology. Reaching
    # for openmm_Topology's own to_openmm_Topology handed a molsysmt.MolSys to a
    # function that subsets an openmm.Topology, and it failed on the first attribute
    # that did not match.
    from .to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_openmm_System import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = openmm_Topology_to_openmm_System(tmp_item, forcefield=forcefield,
            water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints,
            switch_distance=switch_distance, dispersion_correction=dispersion_correction,
            ewald_error_tolerance=ewald_error_tolerance, skip_digestion=True)

    return tmp_item

