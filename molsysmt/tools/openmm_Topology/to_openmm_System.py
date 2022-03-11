from molsysmt.tools.openmm_Topology.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices
from molsysmt._private_tools.exceptions import NotImplementedMethodError

def to_openmm_System(item, atom_indices='all', forcefield=None, parameters=None, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            forcefield = digest_forcefield(forcefield)
        except:
            raise WrongForceFieldError()

    #forcefield = molecular_mechanics.to_openmm_ForceField()
    #system_parameters = molecular_mechanics.get_openmm_System_parameters()
    #tmp_item = forcefield.createSystem(item, **parameters)

    #if molecular_mechanics.use_dispersion_correction or molecular_mechanics.ewald_error_tolerance:
    #    forces = {ii.__class__.__name__ : ii for ii in tmp_item.getForces()}
    #if molecular_mechanics.use_dispersion_correction:
    #    forces['NonbondedForce'].setUseDispersionCorrection(True)
    #if molecular_mechanics.ewald_error_tolerance:
    #    forces['NonbondedForce'].setEwaldErrorTolerance(molecular_mechanics.ewald_error_tolerance)

    #return tmp_item

    raise NotImplementedMethodError
    pass
