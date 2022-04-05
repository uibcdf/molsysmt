from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_nglview_NGLWidget(item, atom_indices='all', coordinates=None, check=True):

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

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, check=False)
    tmp_item = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item, check=False)

    return tmp_item


