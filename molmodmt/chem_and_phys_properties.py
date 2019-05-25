from .utils.exceptions import *
from simtk import unit

def get_charge(item, atom_indices, forcefield=None):

    # This code belongs to the file https://github.com/choderalab/yank/Yank/pipeline.py
    # J. Chodera Lab

    from molmodmt import get_form as _get_form
    from simtk.openmm.app import ForceField
    from simtk.openmm import NonbondedForce

    form_in = _get_form(item)
    charge=[]

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            if forcefield is None:
                forcefield="amber99sb.xml"
            system = ForceField(forcefield).createSystem(item.topology)

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


def get_net_charge(item, atom_indices, forcefield=None):

    from molmodmt import get_form as _get_form
    from simtk.openmm.app import ForceField
    from simtk.openmm import NonbondedForce

    form_in = _get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            if forcefield is None:
                forcefield="amber99sb.xml"
            system = ForceField(forcefield).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        # This code belongs to the file https://github.com/choderalab/yank/Yank/pipeline.py
        # J. Chodera Lab

        atom_indices = set(atom_indices)  # convert to set to speed up searching
        net_charge = 0.0 * unit.elementary_charge
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

