from .utils.exceptions import *
from .utils.forcefields import digest_forcefields as _digest_forcefields
from .utils.engines import digest_engines as _digest_engines
from simtk import unit as _unit

def get_charge(item, atom_indices, forcefield=['AMBER99SB-ILDN','TIP3P']):

    # This code belongs to the file https://github.com/choderalab/yank/Yank/pipeline.py
    # J. Chodera Lab

    from molmodmt import get_form
    from simtk.openmm.app import ForceField
    from simtk.openmm import NonbondedForce

    form_in = get_form(item)
    charge=[]

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        for force_index in range(system.getNumForces()):
            force = system.getForce(force_index)
            if isinstance(force, NonbondedForce):
                for index in atom_indices:
                    charge.append(force.getParticleParameters(index)[0])
        return charge

    else:
        raise NotImplementedError


def get_net_charge(item, atom_indices, forcefield=['AMBER99SB-ILDN','TIP3P']):

    from molmodmt import get_form as get_form
    from simtk.openmm.app import ForceField
    from simtk.openmm import NonbondedForce

    form_in = _get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        # This code belongs to the file https://github.com/choderalab/yank/Yank/pipeline.py
        # J. Chodera Lab

        atom_indices = set(atom_indices)  # convert to set to speed up searching
        net_charge = 0.0 * _unit.elementary_charge
        for force_index in range(system.getNumForces()):
            force = system.getForce(force_index)
            if isinstance(force, NonbondedForce):
                for particle_index in range(force.getNumParticles()):
                    if particle_index in atom_indices:
                        net_charge += force.getParticleParameters(particle_index)[0]
                        atom_indices.remove(particle_index)
        assert len(atom_indices) == 0
        net_charge = int(round(net_charge / unit.elementary_charge))
        return net_charge

    else:
        raise NotImplementedError


def get_mass(item, atom_indices, forcefield=['AMBER99SB-ILDN','TIP3P']):

    from molmodmt import get_form

    form_in = get_form(item)
    mass=[]

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            from simtk.openmm.app import ForceField
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        atom_indices = set(atom_indices)
        for particle_index in range(system.getNumParticles()):
            if particle_index in atom_indices:
                mass.append(system.getParticleMass(particle_index))
        return mass

    else:
        raise NotImplementedError


def get_net_mass(item, atom_indices, forcefield=['AMBER99SB-ILDN','TIP3P']):

    from molmodmt import get_form

    form_in = get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            from simtk.openmm.app import ForceField
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        atom_indices = set(atom_indices)
        net_mass = 0.0 * _unit.amu
        for particle_index in range(system.getNumParticles()):
            if particle_index in atom_indices:
                net_mass += system.getParticleMass(particle_index)
        return net_mass.in_units_of(unit.gram/unit.mole)/unit.AVOGADRO_CONSTANT_NA

    else:
        raise NotImplementedError

def get_degrees_of_freedom(item, forcefield=['AMBER99SB-ILDN','TIP3P']):

    from molmodmt import get_form

    form_in = get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            from simtk.openmm.app import ForceField
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        return 3*system.getNumParticles() - system.getNumConstraints()

    else:
        raise NotImplementedError


