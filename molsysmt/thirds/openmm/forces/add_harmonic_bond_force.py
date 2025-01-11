from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_harmonic_bond_force(molecular_system=None, atom_pair=None,
                            force_constant='1000 kilojoules_per_mole/nm**2', bond_length=None,
                            pbc=False, return_force=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from molsysmt.structure import get_distances
    from openmm import HarmonicBondForce

    atom_pairs=atom_pair

    n_pairs = len(atom_pairs)

    if bond_length is None:
        bond_length = get_distances(molecular_system, element='atom',
                      selection=atom_pairs, pairs=True, pbc=pbc)[0]

    if len(bond_length) != n_pairs:
        bond_length = [bond_length[0] for ii in range(n_pairs)]

    if len(force_constant) != n_pairs:
        force_constant = [force_constant[0] for ii in range(n_pairs)]

    force = HarmonicBondForce()

    for ii, atom_pair in enumerate(atom_pairs):
        aux_force_constant = puw.convert(force_constant[ii], to_form='openmm.unit')
        aux_bond_length = puw.convert(bond_length[ii], to_form='openmm.unit')
        force.addBond(int(atom_pair[0]), int(atom_pair[1]), aux_bond_length, aux_force_constant)

    if not return_force:
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
        elif form_in == 'openmm.Simulation':
            simulation = molecular_system
            index_force = simulation.system.addForce(force)
            simulation.context.reinitialize(preserveState=True)
            return index_force        
    else:
        return force

