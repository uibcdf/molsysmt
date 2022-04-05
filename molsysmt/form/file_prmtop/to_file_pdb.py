from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, atom_indices='all', coordinates=None, output_filename=None, check=True):

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

    if output_filename is None:
        raise ValueError

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, output_filename=output_filename, check=False)

    return tmp_item

