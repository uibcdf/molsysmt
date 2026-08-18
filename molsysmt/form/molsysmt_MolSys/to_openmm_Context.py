from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_openmm_Context(item, atom_indices='all', structure_indices='all',
        forcefield='AMBER14', water_model=None, implicit_solvent=None,
        non_bonded_method='no cutoff', constraints='hbonds', switch_distance=None,
        dispersion_correction=False, ewald_error_tolerance=0.0005,
        integrator='Langevin', temperature='300.0 kelvin', friction='1.0/picoseconds', time_step='2 femtoseconds',
        platform='CUDA', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to openmm.Context.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
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

    from .to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt.form.openmm_Topology.to_openmm_Context import to_openmm_Context as openmm_Topology_to_openmm_Context

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_item = openmm_Topology_to_openmm_Context(tmp_item, coordinates=coordinates,
            forcefield=forcefield, water_model=water_model, implicit_solvent=implicit_solvent,
            non_bonded_method=non_bonded_method, constraints=constraints, switch_distance=switch_distance,
            dispersion_correction=dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
            integrator=integrator, temperature=temperature, friction=friction, time_step=time_step,
            platform=platform, skip_digestion=True)

    return tmp_item
