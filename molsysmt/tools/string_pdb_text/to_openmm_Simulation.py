from molsysmt.tools.string_pdb_text.is_string_pdb_text import is_string_pdb_text
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_structure_indices

def to_openmm_Simulation(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_pdb_text(item)
        except:
            raise WrongFormError('string:pdb_text')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.tools.string_pdb_text import to_openmm_Modeller as string_pdb_text_to_openmm_Modeller
    from molsysmt.tools.openmm_Modeller import to_openmm_Simulation as openmm_Modeller_to_openmm_Simulation

    tmp_item = string_pdb_text_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Modeller_to_openmm_Simulation(tmp_item, check=False)

    return tmp_item

#    tmp_item, tmp_molecular_system = openmm_Modeller_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system, forcefield=forcefield, non_bonded_method=non_bonded_method,
#                                                    non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
#                                                    remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
#                                                    switch_distance=switch_distance, flexible_constraints=flexible_constraints,
#                                                    integrator=integrator, temperature=temperature,
#                                                    collisions_rate=collisions_rate, integration_timestep=integration_timestep,
#                                                    platform=platform, **kwargs)
#


