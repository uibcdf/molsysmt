from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest

@arg_digest()
def get_degrees_of_freedom(item, forcefield=None, water_model=None, implicit_solvent=None, skip_digestion=False):

    from molsysmt import get_form
    from molsysmt.configure import default_attribute
    from molsysmt._private.forcefield import digest_forcefield

    form_in = get_form(item)

    if form_in in ["openmm.Modeller", "openmm.System", "pdbfixer.PDBFixer"]:

        if form_in in ["openmm.Modeller", "pdbfixer.PDBFixer"]:
            from openmm.app import ForceField
            if forcefield is None:
                forcefield = default_attribute['forcefield']
            if water_model is None:
                water_model = default_attribute['water_model']
            if implicit_solvent is None:
                implicit_solvent = default_attribute['implicit_solvent']

            forcefield_openmm = digest_forcefield(forcefield, 'OpenMM', implicit_solvent=implicit_solvent, water_model=water_model)
            system = ForceField(*forcefield_openmm).createSystem(item.topology)

        elif form_in == "openmm.System":
            system = item

        return 3*system.getNumParticles() - system.getNumConstraints()

    else:
        raise NotImplementedError


