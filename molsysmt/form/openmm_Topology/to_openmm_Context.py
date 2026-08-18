from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Topology')
def to_openmm_Context(item, atom_indices='all', coordinates=None, forcefield='AMBER14', water_model=None,
        implicit_solvent=None, non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005, integrator='Langevin', temperature=None,
        friction='1.0/picoseconds', time_step='2 femtoseconds', platform='CUDA', skip_digestion=False):
    """
    Converting from openmm.Topology to openmm.Context.

    Parameters
    ----------
    item : openmm.Topology
        Source item in openmm.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    forcefield : object
        Argument forcefield.
    water_model : object
        Argument water_model.
    implicit_solvent : object
        Argument implicit_solvent.
    non_bonded_method : object
        Argument non_bonded_method.
    constraints : object
        Argument constraints.
    switch_distance : object
        Argument switch_distance.
    dispersion_correction : object
        Argument dispersion_correction.
    ewald_error_tolerance : object
        Argument ewald_error_tolerance.
    integrator : object
        Argument integrator.
    temperature : object
        Argument temperature.
    friction : object
        Argument friction.
    time_step : object
        Argument time_step.
    platform : object
        Argument platform.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Context
        Resulting object in openmm.Context form.

    .. versionadded:: 1.0.0
    """


    from .to_openmm_System import to_openmm_System
    from molsysmt.form.openmm_System.to_openmm_Context import to_openmm_Context as openmm_System_to_openmm_Context

    system = to_openmm_System(item, atom_indices=atom_indices, forcefield=forcefield,
            water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints,
            switch_distance=switch_distance, dispersion_correction=dispersion_correction,
            ewald_error_tolerance=ewald_error_tolerance, skip_digestion=True)
    context = openmm_System_to_openmm_Context(system, coordinates=coordinates,
            integrator=integrator, temperature=temperature, friction=friction,
            time_step=time_step, platform=platform, skip_digestion=True)

    return context
