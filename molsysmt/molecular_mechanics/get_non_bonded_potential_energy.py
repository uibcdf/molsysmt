# =======================
# Potential Energy
# =======================

"""
Potential Energy
================

Methods related with the potential energy of the system.
From energy minimization to potential energy contribution of specific set of atoms or interactions.
"""

from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import openmm as mm
from openmm import unit

@digest()
def get_non_bonded_potential_energy(molecular_system, selection='all', selection_2=None,
        platform='CUDA', engine='OpenMM', syntax='MolSysMT'):

    from molsysmt import convert, get_form, has_attribute, select
    from molsysmt.config import default_attribute

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    if selection_2 is not None:
        atom_indices_2 = select(molecular_system, selection=selection_2, syntax=syntax)
    else:
        atom_indices_2 = None

    if engine=='OpenMM':

        form_in = get_form(molecular_system)

        if form_in == 'openmm.Context':

            context=molecular_system

        elif form_in == 'openmm.Simulation':

            context = item.context

        else:

            extra_conversion_arguments={}

            possible_missing_attributes=['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                    'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                    'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att]=default_attribute[att]

            context = convert(molecular_system, to_form='openmm.Context',
                    **extra_conversion_arguments, platform=platform)

        tmp_system = context.getSystem()

        non_bonded_force = None
        non_bonded_forcegroup = None
        for ii in range(tmp_system.getNumForces()):
            force = tmp_system.getForce(ii)
            if force.getName() == 'NonbondedForce':
                non_bonded_force = force
                non_bonded_forcegroup = ii
                non_bonded_force.setForceGroup(ii)

        tmp_context = mm.Context(tmp_system, mm.VerletIntegrator(0.001), context.getPlatform())
        tmp_context.setPositions(context.getState(getPositions=True).getPositions())

        original_particle_parameters = {}
        for ii in range(non_bonded_force.getNumParticles()):
            charge, sigma, epsilon = non_bonded_force.getParticleParameters(ii)
            original_particle_parameters[ii] = {'charge': charge, 'sigma': sigma, 'epsilon':epsilon}

        original_exception_parameters = {}
        for ii in range(non_bonded_force.getNumExceptions()):
            particle1, particle2, chargeProd, sigma, epsilon = non_bonded_force.getExceptionParameters(ii)
            original_exception_parameters[ii] = {'particle1': particle1, 'particle2': particle2, 'chargeProd': chargeProd,
                                             'sigma': sigma, 'epsilon': epsilon}

        if atom_indices_2 is None:

            output = _aux_openmm(atom_indices, non_bonded_force, non_bonded_forcegroup,
                    tmp_context, original_particle_parameters, original_exception_parameters)

            output = puw.standardize(output)

        else:

            raise NotImplementedError


        return output

    else:

        raise NotImplementedError


def _aux_openmm(atoms_in, non_bonded_force, non_bonded_forcegroup, context, original_particle_parameters,
                original_exception_parameters):

    for ii, parameters in original_particle_parameters.items():

        charge = parameters['charge']
        sigma = parameters['sigma']
        epsilon = parameters['epsilon']

        if ii not in atoms_in:
            charge = 0.0 * unit.elementary_charge
            epsilon = 0.0 * unit.kilojoule_per_mole

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, parameters in original_exception_parameters.items():

        particle1 = parameters['particle1']
        particle2 = parameters['particle2']
        chargeProd = parameters['chargeProd']
        sigma = parameters['sigma']
        epsilon = parameters['epsilon']

        if (particle1 not in atoms_in) and (particle2 not in atoms_in):
            epsilon = 0.0 * unit.kilojoule_per_mole
            if chargeProd != 0.0 * unit.elementary_charge**2:
                chargeProd = 0.0000000000001 * unit.elementary_charge **2

        non_bonded_force.setExceptionParameters(ii, particle1, particle2, chargeProd,
                                                sigma, epsilon)

    non_bonded_force.updateParametersInContext(context)

    energy = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

    return energy

