from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Modeller(item, atom_indices='all', coordinates=None, check=True):

    if check:

        try:
            is_file_prmtop(item)
        except:
            raise WrongFormError('file:prmtop')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

    from . import to_openmm_Topology
    from ..openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices)

    return tmp_item


