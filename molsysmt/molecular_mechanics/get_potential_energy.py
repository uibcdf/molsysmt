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

#@digest()
def get_potential_energy(molecular_system, selection='all', selection_2=None, platform='CUDA', engine='OpenMM'):

    from molsysmt import convert, get_form, has_attribute
    from molsysmt.config import default_attribute

    in_form = get_form(molecular_system)

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

        state = context.getState(getEnergy=True)
        energy = state.getPotentialEnergy()

        energy = puw.standardize(energy)

        return energy

    else:

        raise NotImplementedError

