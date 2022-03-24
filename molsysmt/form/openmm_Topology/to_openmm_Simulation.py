from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.coordinates import digest_coordinates

def to_openmm_Simulation(item, atom_indices='all', check=True):

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
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

    from . import to_openmm_System
    from ..openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item = to_openmm_System(item, atom_indices=atom_indices, check=False)
    tmp_item = openmm_System_to_openmm_Simulation(tmp_item, check=False)

    return tmp_item


