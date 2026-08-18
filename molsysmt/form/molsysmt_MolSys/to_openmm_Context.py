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
    integrator : object, default='Langevin'
        Argument integrator.
    temperature : object, default='300.0 kelvin'
        Argument temperature.
    friction : object, default='1.0/picoseconds'
        Argument friction.
    time_step : object, default='2 femtoseconds'
        Argument time_step.
    platform : str, default='CUDA'
        OpenMM platform name ('Reference', 'CPU', 'CUDA', 'OpenCL').
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
