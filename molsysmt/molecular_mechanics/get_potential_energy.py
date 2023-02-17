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

@digest()
def get_potential_energy(molecular_system, molecular_mechanics={'forcefield':'AMBER99SB-ILDN'}, engine='OpenMM'):

    """get_potential_energy(molecular_system, ...)

    """

    from molsysmt import convert, get_form, has_attribute

    in_form = get_form(molecular_system)

    if engine=='OpenMM':

        if in_form=='openmm.Context':

            state = molecular_system.getState(getEnergy=True)

        elif in_form=='openmm.Simulation':

            state = molecular_system.context.getState(getEnergy=True)

        else:

            if has_attribute(molecular_system, 'mechanical'):
                simulation = msm.convert(molecular_system, to_form='openmm.Simulation')
            else:
                simulation = msm.convert([molecular_system, molecular_mechanics], to_form='openmm.Simulation')

            state_pre_min = output.context.getState(getEnergy=True)
            simulation.minimizeEnergy()
            state_post_min = output.context.getState(getEnergy=True)

            if inplace:
                from molsysmt.form.openmm_Simulation import get_coordinates_from_system
                coordinates = get_coordinates_from_system(output)
                set(molecular_system, coordinates=coordinates)

        if verbose:
            energy_pre_min = state_pre_min.getPotentialEnergy()
            energy_pre_min = puw.standardize(energy_pre_min)
            print("Potential Energy before minimization: {}".format(energy_pre_min))
            energy_post_min = state_post_min.getPotentialEnergy()
            energy_post_min = puw.standardize(energy_post_min)
            print("Potential Energy after minimization: {}".format(energy_post_min))

        if inplace:
            pass
        else:
            output = convert(output, to_form=to_form)
            return output

    else:

        raise NotImplementedError
