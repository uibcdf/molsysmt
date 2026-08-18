from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def get_non_bonded_potential_energy(molecular_system, selection='all', selection_2=None, structure_indices='all',
                                    engine='OpenMM', syntax='MolSysMT', skip_digestion=False):
    """
    Calculating non-bonded interaction potential energy between selections or pairwise across structures.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Primary selection of atoms.
    selection_2 : str, list, tuple, or numpy.ndarray, optional
        Secondary selection of atoms for interaction energy calculations.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure frames to evaluate.
    engine : str, default='OpenMM'
        Simulation engine backend.
    syntax : str, default='MolSysMT'
        Selection syntax used.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    quantity or dict
        Non-bonded potential energy interaction values in canonical units (`kJ/mol`).

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import select, convert, get, get_form, has_attribute
    from molsysmt.configure import default_attribute
    import openmm as mm
    import numpy as np

    if engine == 'OpenMM':

        form_in = get_form(molecular_system)

        if form_in in ['openmm.Simulation', 'openmm.Context']:
            openmm_system = molecular_system.system
            topology = convert(molecular_system, to_form='molsysmt.Topology')
            coordinates = get(molecular_system, element='atom', selection='all', structure_indices=structure_indices, coordinates=True)
        else:
            extra_conversion_arguments = {}
            possible_missing_attributes = ['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                                          'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                                          'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att] = default_attribute[att]

            openmm_system = convert(molecular_system, to_form='openmm.System', **extra_conversion_arguments)
            topology = convert(molecular_system, to_form='molsysmt.Topology')
            coordinates = get(molecular_system, element='atom', selection='all', structure_indices=structure_indices, coordinates=True)

        # Evaluate interactions
        integrator = mm.VerletIntegrator(1.0 * mm.unit.femtoseconds)
        context = mm.Context(openmm_system, integrator, mm.Platform.getPlatformByName('CPU'))

        n_structures = coordinates.shape[0]
        output = []

        for i in range(n_structures):
            pos = puw.get_value(coordinates[i], to_unit='nanometer')
            context.setPositions(pos)
            state = context.getState(getEnergy=True)
            output.append(puw.get_value(state.getPotentialEnergy(), to_unit='kJ/mol'))

        return puw.quantity(np.array(output), 'kJ/mol')

    else:
        raise NotImplementedError
