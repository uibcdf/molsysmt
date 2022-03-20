from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        if not is_mmtf_MMTFDecoder(item):
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            atom_indices = digest_indices(atom_indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.native.structures import Structures
    from .get import get_step_from_system, get_time_from_system
    from .get import get_coordinates_from_atom, get_box_from_system

    step = get_step_from_system(item, structure_indices=structure_indices, check=False)
    time = get_time_from_system(item, structure_indices=structure_indices, check=False)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    box = get_box_from_system(item, structure_indices=structure_indices, check=False)

    tmp_item = Structures()
    tmp_item.append_structures(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

