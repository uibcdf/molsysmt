from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest()
def add_constant_force(molecular_system, selection='all',
                       force='[500,0,0] kilojoules/(mole*nanometer)', return_force=False,
                       syntax='MolSysMT', skip_digestion=False):
    """
    Adding a constant directional force vector to selected particles in OpenMM.

    Parameters
    ----------
    system : openmm.System
        Target OpenMM system to modify.
    atom_indices : list of int
        Atom indices to apply constant force to.
    force_vector : quantity or list of float
        3D force vector in `kJ/(mol*nm)`.

    Returns
    -------
    openmm.CustomExternalForce
        The added constant force instance.

    .. versionadded:: 1.0.0
    """

    from molsysmt import select, get, get_form
    from openmm import CustomExternalForce

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    potential = "-(px*x+py*y+pz*z)"
    force = puw.convert(force, to_unit='kJ/(mole*nm)', to_form='openmm.unit')
    force_values = puw.get_value(force)

    ommforce = CustomExternalForce(potential)
    ommforce.addGlobalParameter('px', float(force_values[0]))
    ommforce.addGlobalParameter('py', float(force_values[1]))
    ommforce.addGlobalParameter('pz', float(force_values[2]))

    for ii in atom_indices:
        ommforce.addParticle(int(ii))

    if not return_force:
        form_in = get_form(molecular_system)
        if form_in == 'openmm.Context':
            context = molecular_system
            index_force = context.getSystem().addForce(ommforce)
            context.reinitialize(preserveState=True)
            return index_force
        elif form_in == 'openmm.System':
            system = molecular_system
            index_force = system.addForce(ommforce)
            return index_force
        elif form_in == 'openmm.Simulation':
            simulation = molecular_system
            index_force = simulation.system.addForce(ommforce)
            simulation.context.reinitialize(preserveState=True)
            return index_force
    else:
        return ommforce
