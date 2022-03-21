from .is_nglview_NGLWidget import is_nglview_NGLWidget
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_nglview_NGLWidget(item)
        except:
            raise WrongFormError('nglview.NGLWidget')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()


    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_box_from_system, get_step_from_system, get_time_from_system

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)
    step = get_step_from_system(item, structure_indices=structure_indices, check=False)
    time = get_time_from_system(item, structure_indices=structure_indices, check=False)
    tmp_item.append_structures(coordinates=coordinates, box=box, step=step, time=time)

    return tmp_item

