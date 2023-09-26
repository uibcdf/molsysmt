from molsysmt import pyunitwizard as puw
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest()
def get_forces(molecular_system, selection='all', norm=False, platform='CUDA',
        engine='OpenMM', syntax='MolSysMT'):

    from molsysmt import convert, select, get_form, has_attribute
    from molsysmt.config import default_attribute

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if engine=='OpenMM':

        import openmm as mm

        form_in = get_form(molecular_system)

        if form_in == 'openmm.Context':

            if is_all(selection):

                context=molecular_system

            else:

                from molsysmt.form.openmm_Context import extract

                context=extract(molecular_system, selection=selection, syntax=syntax)

        elif form_in == 'openmm.Simulation':

            if is_all(selection):

                context = item.context

            else:

                from molsysmt.form.openmm_Simulation import extract

                context=extract(molecular_system, selection=selection, syntax=syntax)

        else:

            extra_conversion_arguments={}

            possible_missing_attributes=['forcefield', 'water_model', 'implicit_solvent', 'constraints',
                    'non_bonded_method', 'switch_distance', 'dispersion_correction', 'ewald_error_tolerance',
                    'integrator', 'temperature', 'friction', 'time_step']

            for att in possible_missing_attributes:
                if not has_attribute(molecular_system, att):
                    extra_conversion_arguments[att]=default_attribute[att]

            context = convert(molecular_system, to_form='openmm.Context', selection=selection,
                    syntax=syntax, **extra_conversion_arguments, platform=platform)

        state = context.getState(getForces=True)
        output = state.getForces(asNumpy=True)
        output = output[atom_indices]
        output = puw.standardize(output)

        if norm:
            output_value, output_unit = puw.get_value_and_unit(output)
            output_value = np.linalg.norm(output_value, axis=1)
            output = puw.quantity(output_value, output_unit)

        return output

    else:

        raise NotImplementedError

