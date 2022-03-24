from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_openmm_System(item, atom_indices='all', structure_indices='all', check=True,
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff='1.0 nm', constraints=None,
                     rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_openmm_System(tmp_item, forcefield=forcefield,
                                                non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff,
                                                constraints=constraints, rigid_water=rigid_water, remove_cm_motion=remove_cm_motion,
                                                hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
                                                flexible_constraints=flexible_constraints,
                                                check=False, **kwargs)

    return tmp_item

