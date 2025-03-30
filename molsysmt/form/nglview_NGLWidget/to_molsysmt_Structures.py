from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='nglview.NGLWidget')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native.structures import Structures
    from ..string_pdb_text import to_molsysmt_Structures as string_pdb_text_to_molsysmt_Structures
    from molsysmt.basic import set

    tmp_item = Structures()

    if is_all(structure_indices):
        n_structures = item.max_frame + 1
        structure_indices = np.arange(n_structures)

    if hasattr(item[0], 'get_structure_string()'):
        string_pdb_text = item[0].get_structure_string() # string pdb text
    else:
        string_pdb_text = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']

    tmp_item = string_pdb_text_to_molsysmt_Structures(string_pdb_text, atom_indices=atom_indices,
                                                      structure_indices='all', skip_digestion=True)

    if hasattr(item[0], 'get_coordinates'):

        coordinates = []
        for ii in structure_indices:
            if is_all(atom_indices):
                coordinates.append(item[0].get_coordinates(ii))
            else:
                coordinates.append(item[0].get_coordinates(ii)[atom_indices,:])
        coordinates = np.array(coordinates)
        coordinates = puw.quantity(coordinates, unit='angstroms')
        coordinates = puw.standardize(coordinates)

        set(tmp_item, element='atom', coordinates=coordinates)

    return tmp_item

