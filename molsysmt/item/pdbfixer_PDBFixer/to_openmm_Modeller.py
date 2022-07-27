from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_openmm_Modeller(item, atom_indices='all'):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt import puw
    from . import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices)
    coordinates = puw.convert(coordinates, to_units='nanometer', to_form='openmm.unit')
    tmp_item = openmm_Modeller(tmp_item, coordinates)

    return tmp_item

