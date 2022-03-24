from .is_openmm_Topology import is_openmm_Topology
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.coordinates import digest_coordinates

def to_openmm_Modeller(item, atom_indices='all', coordinates=None, check=True):

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

    from . import extract
    from molsysmt import puw
    from openmm.app import Modeller

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, check=False)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(tmp_item, positions)

    return tmp_item

