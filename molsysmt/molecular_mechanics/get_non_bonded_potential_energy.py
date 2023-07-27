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
from molsysmt._private.variables import is_iterable_of_iterables, is_iterable_of_iterables
import openmm as mm
from openmm import unit
import numpy as np

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

            if not is_iterable_of_iterables(atom_indices) and not is_iterable_of_iterables(atom_indices_2):

                output = _aux_openmm_crossed(atom_indices, atom_indices_2, non_bonded_force, non_bonded_forcegroup,
                         tmp_context, original_particle_parameters, original_exception_parameters)

                output = puw.standardize(output)

            else:

                output = _aux_openmm_crossed_lists(atom_indices, atom_indices_2, non_bonded_force, non_bonded_forcegroup,
                         tmp_context, original_particle_parameters, original_exception_parameters)

                #output = puw.standardize(output)

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
            sigma = 0.0 * unit.nanometer

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, parameters in original_exception_parameters.items():

        particle1 = parameters['particle1']
        particle2 = parameters['particle2']
        chargeProd = parameters['chargeProd']
        sigma = parameters['sigma']
        epsilon = parameters['epsilon']

        if (particle1 not in atoms_in) or (particle2 not in atoms_in):
            epsilon = 0.0 * unit.kilojoule_per_mole
            sigma = 0.0 * unit.nanometer
            if chargeProd != 0.0 * unit.elementary_charge**2:
                chargeProd = 1e-22 * unit.elementary_charge **2

        non_bonded_force.setExceptionParameters(ii, particle1, particle2, chargeProd,
                                                sigma, epsilon)

    non_bonded_force.updateParametersInContext(context)

    energy = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

    return energy


def _aux_openmm_crossed(atoms_in_1, atoms_in_2, non_bonded_force, non_bonded_forcegroup, context, original_particle_parameters,
                original_exception_parameters):

    aux_exc_pars_11 = []
    aux_exc_pars_22 = []
    aux_exc_pars_12 = []

    zero_charge = 0.0 * unit.elementary_charge
    zero_chargeProd = 0.0 * unit.elementary_charge**2
    zero_almost_chargeProd = 1e-22 * unit.elementary_charge**2
    zero_epsilon = 0.0 * unit.kilojoule_per_mole
    zero_sigma = 0.0 * unit.nanometer

    # All to zero

    for ii, parameters in original_particle_parameters.items():

        non_bonded_force.setParticleParameters(ii, zero_charge, zero_sigma, zero_epsilon)

    for ii, parameters in original_exception_parameters.items():

        particle1 = parameters['particle1']
        particle2 = parameters['particle2']
        chargeProd = parameters['chargeProd']
        sigma = parameters['sigma']
        epsilon = parameters['epsilon']

        if (particle1 in atoms_in_1) and (particle2 in atoms_in_1):
            aux_exc_pars_11.append([ii, particle1, particle2, chargeProd, sigma, epsilon])

        elif (particle1 in atoms_in_2) and (particle2 in atoms_in_2):
            aux_exc_pars_22.append([ii, particle1, particle2, chargeProd, sigma, epsilon])

        elif ((particle1 in atoms_in_1) and (particle2 in atoms_in_2)) or ((particle1 in
            atoms_in_2) and (particle2 in atoms_in_1)):
            aux_exc_pars_12.append([ii, particle1, particle2, chargeProd, sigma, epsilon])

        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2, zero_almost_chargeProd,
                                                zero_sigma, zero_epsilon)
        else:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2, zero_chargeProd,
                                                zero_sigma, zero_epsilon)

    non_bonded_force.updateParametersInContext(context)

    # subsystem1

    for ii in atoms_in_1:

        charge = original_particle_parameters[ii]['charge']
        sigma = original_particle_parameters[ii]['sigma']
        epsilon = original_particle_parameters[ii]['epsilon']

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_11:

        non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                chargeProd, sigma, epsilon)

    non_bonded_force.updateParametersInContext(context)

    energy_1 = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

    # subsystem1 union subsystem2


    for ii in atoms_in_2:

        charge = original_particle_parameters[ii]['charge']
        sigma = original_particle_parameters[ii]['sigma']
        epsilon = original_particle_parameters[ii]['epsilon']

        non_bonded_force.setParticleParameters(ii, charge, sigma, epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_22:

        non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                chargeProd, sigma, epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12:

        non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                chargeProd, sigma, epsilon)

    non_bonded_force.updateParametersInContext(context)

    energy_12 = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

    # subsystem2 (subsystem1 to zero)

    for ii in atoms_in_1:

        non_bonded_force.setParticleParameters(ii, zero_charge, zero_sigma, zero_epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_11:
        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                zero_almost_chargeProd, zero_sigma, zero_epsilon)
        else:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                zero_chargeProd, zero_sigma, zero_epsilon)

    for ii, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12:
        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                zero_almost_chargeProd, zero_sigma, zero_epsilon)
        else:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2,
                zero_chargeProd, zero_sigma, zero_epsilon)

    non_bonded_force.updateParametersInContext(context)

    energy_2 = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

    energy = energy_12-energy_1-energy_2

    return energy

def _aux_openmm_crossed_lists(atoms_in_1, atoms_in_2, non_bonded_force, non_bonded_forcegroup, context, original_particle_parameters,
                original_exception_parameters):

    if not is_iterable_of_iterables(atoms_in_1):
        atoms_in_1=[atoms_in_1]

    if not is_iterable_of_iterables(atoms_in_2):
        atoms_in_1=[atoms_in_2]

    n_atoms_lists_in_1 = len(atoms_in_1)
    n_atoms_lists_in_2 = len(atoms_in_2)

    aux_exc_pars_1 = [[] for ii in range(n_atoms_lists_in_1)]
    aux_exc_pars_2 = [[] for jj in range(n_atoms_lists_in_2)]
    aux_exc_pars_12 = [[[] for jj in range(n_atoms_lists_in_2)] for ii in range(n_atoms_lists_in_1)]

    output = np.zeros((n_atoms_lists_in_1, n_atoms_lists_in_2), dtype=float) * unit.kilojoule_per_mole
    E1 = np.zeros((n_atoms_lists_in_1), dtype=float) * unit.kilojoule_per_mole
    E2 = np.zeros((n_atoms_lists_in_2), dtype=float) * unit.kilojoule_per_mole

    zero_charge = 0.0 * unit.elementary_charge
    zero_chargeProd = 0.0 * unit.elementary_charge**2
    zero_almost_chargeProd = 1e-22 * unit.elementary_charge**2
    zero_epsilon = 0.0 * unit.kilojoule_per_mole
    zero_sigma = 0.0 * unit.nanometer

    # All to zero

    inv_aux_dict_1 = {}
    inv_aux_dict_2 = {}

    for jj, aux in enumerate(atoms_in_1):
        for ii in aux:
            inv_aux_dict_1[ii]=jj

    for jj, aux in enumerate(atoms_in_2):
        for ii in aux:
            inv_aux_dict_2[ii]=jj

    for ii, parameters in original_particle_parameters.items():

        non_bonded_force.setParticleParameters(ii, zero_charge, zero_sigma, zero_epsilon)

    for ii, parameters in original_exception_parameters.items():

        particle1 = parameters['particle1']
        particle2 = parameters['particle2']
        chargeProd = parameters['chargeProd']
        sigma = parameters['sigma']
        epsilon = parameters['epsilon']

        if particle1 in inv_aux_dict_1:

            aa = inv_aux_dict_1[particle1]

            if particle2 in inv_aux_dict_1:

                bb = inv_aux_dict_1[particle2]

                if aa==bb:

                    aux_exc_pars_1[aa].append([ii, particle1, particle2, chargeProd, sigma, epsilon])

            if particle2 in inv_aux_dict_2:

                bb = inv_aux_dict_2[particle2]

                aux_exc_pars_12[aa][bb].append([ii, particle1, particle2, chargeProd, sigma, epsilon])

        elif particle1 in inv_aux_dict_2:

            bb = inv_aux_dict_2[particle1]

            if particle2 in inv_aux_dict_2:

                aa = inv_aux_dict_2[particle2]

                if aa==bb:

                    aux_exc_pars_2[aa].append([ii, particle1, particle2, chargeProd, sigma, epsilon])

            if particle2 in inv_aux_dict_1:

                aa = inv_aux_dict_1[particle2]

                aux_exc_pars_12[aa][bb].append([ii, particle1, particle2, chargeProd, sigma, epsilon])

        if chargeProd != 0.0 * unit.elementary_charge**2:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2, zero_almost_chargeProd,
                                                zero_sigma, zero_epsilon)
        else:
            non_bonded_force.setExceptionParameters(ii, particle1, particle2, zero_chargeProd,
                                                zero_sigma, zero_epsilon)

    non_bonded_force.updateParametersInContext(context)

    # E1

    for ii, aux in enumerate(atoms_in_1):

        for jj in aux:

            charge = original_particle_parameters[jj]['charge']
            sigma = original_particle_parameters[jj]['sigma']
            epsilon = original_particle_parameters[jj]['epsilon']

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:

            non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                                                    chargeProd, sigma, epsilon)

        non_bonded_force.updateParametersInContext(context)

        E1[ii] = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()


        for jj in aux:

            non_bonded_force.setParticleParameters(jj, zero_charge, zero_sigma, zero_epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_almost_chargeProd, zero_sigma, zero_epsilon)
            else:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_chargeProd, zero_sigma, zero_epsilon)


    # E2

    for ii, aux in enumerate(atoms_in_2):

        for jj in aux:

            charge = original_particle_parameters[jj]['charge']
            sigma = original_particle_parameters[jj]['sigma']
            epsilon = original_particle_parameters[jj]['epsilon']

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ii]:

            non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                                                    chargeProd, sigma, epsilon)

        non_bonded_force.updateParametersInContext(context)

        E2[ii] = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()


        for jj in aux:

            non_bonded_force.setParticleParameters(jj, zero_charge, zero_sigma, zero_epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_almost_chargeProd, zero_sigma, zero_epsilon)
            else:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_chargeProd, zero_sigma, zero_epsilon)


    # E1 + E2 + E12

    for ii, aux1 in enumerate(atoms_in_1):

        for jj in aux1:

            charge = original_particle_parameters[jj]['charge']
            sigma = original_particle_parameters[jj]['sigma']
            epsilon = original_particle_parameters[jj]['epsilon']

            non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:

            non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                                                    chargeProd, sigma, epsilon)

        for ll, aux2 in enumerate(atoms_in_2):

            for jj in aux2:

                charge = original_particle_parameters[jj]['charge']
                sigma = original_particle_parameters[jj]['sigma']
                epsilon = original_particle_parameters[jj]['epsilon']

                non_bonded_force.setParticleParameters(jj, charge, sigma, epsilon)

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ll]:

                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                                                    chargeProd, sigma, epsilon)

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12[ii][ll]:

                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                                                    chargeProd, sigma, epsilon)

            non_bonded_force.updateParametersInContext(context)

            output[ii,ll] = context.getState(getEnergy=True, groups={non_bonded_forcegroup}).getPotentialEnergy()

            for jj in aux2:

                non_bonded_force.setParticleParameters(jj, zero_charge, zero_sigma, zero_epsilon)

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_2[ll]:
                if chargeProd != 0.0 * unit.elementary_charge**2:
                    non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                        zero_almost_chargeProd, zero_sigma, zero_epsilon)
                else:
                    non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                        zero_chargeProd, zero_sigma, zero_epsilon)

            for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_12[ii][ll]:
                if chargeProd != 0.0 * unit.elementary_charge**2:
                    non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                        zero_almost_chargeProd, zero_sigma, zero_epsilon)
                else:
                    non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                        zero_chargeProd, zero_sigma, zero_epsilon)

        for jj in aux1:

            non_bonded_force.setParticleParameters(jj, zero_charge, zero_sigma, zero_epsilon)

        for jj, particle1, particle2, chargeProd, sigma, epsilon in aux_exc_pars_1[ii]:
            if chargeProd != 0.0 * unit.elementary_charge**2:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_almost_chargeProd, zero_sigma, zero_epsilon)
            else:
                non_bonded_force.setExceptionParameters(jj, particle1, particle2,
                    zero_chargeProd, zero_sigma, zero_epsilon)

    for ii in range(n_atoms_lists_in_1):
        for jj in range(n_atoms_lists_in_2):
            output[ii,jj] = output[ii,jj]-E1[ii]-E2[jj]

    return output

