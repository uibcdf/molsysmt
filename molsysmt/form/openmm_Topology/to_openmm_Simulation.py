from molsysmt._private.exceptions import *
from molsysmt._private.digestion import  *
from .is_openmm_Topology import is_openmm_Topology
<<<<<<< HEAD
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
=======
>>>>>>> 5c6ee6a0366ddfe994d7fe0c3fc26225984869c7

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


