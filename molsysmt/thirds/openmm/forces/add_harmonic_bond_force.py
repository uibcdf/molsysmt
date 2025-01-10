from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest()
def add_harmonic_bond_force(molecular_system=None, atom_pair=None,
                            force_constant='1000 kilojoules_per_mole/nm**2', bond_length=None,
                            pbc=False, return_force=False, syntax='MolSysMT', skip_digestion=False):

    from molsysmt import select, get, get_form
    from molsysmt.structure import get_distances
    from openmm import HarmonicBondForce

    if bond_length is None:
        bond_length = get_distances(molecular_system, element='atom',
                      selection=atom_pairs, pairs=True, pbc=pbc)[0]

    force_constant = puw.convert(force_constant, to_form='openmm.unit')
    bond_length = puw.convert(bond_length, to_form='openmm.unit')

    force = HarmonicBondForce()

    n_pairs_in_distances_minima = bond_length.shape[0]

    for ii, atoms_pair in enumerate(atoms_pairs):
        force.addBond(int(atom_pair[0]), int(atom_pair[1]), bond_length[ii], force_constant[ii])

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

