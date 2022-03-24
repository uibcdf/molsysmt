from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import WrongFormError, WrongIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.indices import digest_indices
from molsysmt._private.structure_indices import digest_structure_indices
from molsysmt._private.box import digest_box
from molsysmt import puw

## System

def set_box_to_system(item, structure_indices='all', value=None, check=True):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

        try:
            box = digest_box(value)
        except:
            raise WrongStructureIndicesError()

    raise NotImplementedMethodError()

def set_coordinates_to_system(item, structure_indices='all', value=None, check=True):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

        try:
            box = digest_box(value)
        except:
            raise WrongStructureIndicesError()

    raise NotImplementedMethodError()

