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
                context = convert(molecular_system, to_form='openmm.Context')
            else:
                context = convert([molecular_system, molecular_mechanics], to_form='openmm.Context')

            state = output.context.getState(getEnergy=True)

        energy = state.getPotentialEnergy()
        energy = puw.standardize(energy)

        return energy

    else:

        raise NotImplementedError
