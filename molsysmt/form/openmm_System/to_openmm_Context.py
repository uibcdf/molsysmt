from molsysmt._private.digestion import digest

@digest(form='openmm.System')
def to_openmm_Context(item, atom_indices='all', coordinates=None,
        integrator='Langevin', temperature='300 kelvin', friction='1.0/picoseconds', time_step='2 femtoseconds',
        platform='CUDA'):

    from molsysmt import pyunitwizard as puw
    from molsysmt.form.openmm_Context import set_coordinates_to_atom
    import openmm as mm

    temperature = puw.convert(temperature, to_form='openmm.unit')
    friction = puw.convert(friction, to_form='openmm.unit')
    time_step = puw.convert(time_step, to_form='openmm.unit')

    if integrator=='Langevin':
        integrator = mm.LangevinIntegrator(temperature, friction, time_step)

    if platform=='CUDA':
        platform    = mm.Platform.getPlatformByName('CUDA')
    elif platform=='CPU':
        platform    = mm.Platform.getPlatformByName('CPU')

    context = mm.Context(item, integrator, platform)

    if coordinates is not None:
        set_coordinates_to_atom(context, indices=atom_indices, value=coordinates)

    return context

