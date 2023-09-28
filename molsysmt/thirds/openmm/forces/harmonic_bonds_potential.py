from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def harmonic_bonds_potential(molecular_system=None, atoms_pairs=None, force_constant='1000 kilojoules_per_mole/nm**2',
        distances_minima=None, pbc=False, adding_force=False, syntax='MolSysMT'):

    from molsysmt import select, get, get_form
    from molsysmt.structures import get_distances
    from openmm import HarmonicBondForce

    if distances_minima is None:
        if molecular_system is not None:
            distances_minima = get_distances(molecular_system, element='atom',
                    selection=atoms_pairs, pairs=True, pbc=pbc)

    force_constant = puw.convert(force_constant, to_form='openmm.unit')
    distances_minima = puw.convert(distances_minima[0], to_form='openmm.unit')

    force = HarmonicBondForce()

    n_atoms_in_distances_minima = distances_minima.shape[0]

    if n_atoms_in_coordinates_minimum == 1:
        for ii, atoms_pair in enumerate(atoms_pairs):
            force.addBond(int(atom_pair[0]), int(atom_pair[1]), distances_minima[0],
                    force_constant)
    else:
        for ii, atoms_pair in enumerate(atoms_pairs):
            force.addBond(int(atom_pair[0]), int(atom_pair[1]), distances_minima[ii],
                    force_constant)

    if adding_force:
        form_in = get_form(molecular_system)
        if form_in == 'openmm.Context':
            context = molecular_system
            index_force = context.getSystem().addForce(force)
            aux_positions = context.getState(getPositions=True).getPositions()
            aux_velocities = context.getState(getVelocities=True).getVelocities()
            context.reinitialize()
            context.setPositions(aux_positions)
            context.setVelocities(aux_velocities)
            return index_force
        elif form_in == 'openmm.System':
            system = molecular_system
            index_force = system.addForce(force)
            return index_force
    else:
        return force

