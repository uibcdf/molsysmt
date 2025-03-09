from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest()
def get_degrees_of_freedom(item):

    from molsysmt import get_form

    form_in = get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            from openmm.app import ForceField
            forcefield_openmm = _digest_forcefields(forcefield)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        return 3*system.getNumParticles() - system.getNumConstraints()

    else:
        raise NotImplementedError


