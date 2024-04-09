from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='nglview.NGLWidget')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.structures import Structures
    from ..string_pdb_text import get_box_from_system as get_box_from_string_pdb_text
    from ..string_pdb_text import get_time_from_system as get_time_from_string_pdb_text
    from ..string_pdb_text import get_structure_id_from_system as get_structure_id_from_string_pdb_text

    tmp_item = Structures()

    if is_all(structure_indices):
        n_structures = item.max_frame + 1
        structure_indices = np.arange(n_structures)

    coordinates = []
    for ii in structure_indices:
        if is_all(atom_indices):
            coordinates.append(item[0].get_coordinates(ii))
        else:
            coordinates.append(item[0].get_coordinates(ii)[atom_indices,:])
    coordinates = np.array(coordinates)
    coordinates = puw.quantity(coordinates, unit='angstroms')
    coordinates = puw.standardize(coordinates)

    aux_item = item[0].get_structure_string() # string pdb text
    aux_item = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']
    box = get_box_from_string_pdb_text(aux_item, structure_indices=0, skip_digestion=False)
    time = get_time_from_string_pdb_text(aux_item, structure_indices=structure_indices, skip_digestion=False)
    structure_id = get_structure_id_from_string_pdb_text(aux_item, structure_indices=structure_indices,
                                                         skip_digestion=False)

    tmp_item.append(coordinates=coordinates, box=box, structure_id=structure_id, time=time, skip_digestion=True)

    return tmp_item

