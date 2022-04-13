from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_Structures(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'pdbfixer.PDBFixer')
        atom_indices = digest_atom_indices(atom_indices)

    from molsysmt.native.structures import Structures
    from . import get_coordinates_from_atom, get_box_from_system

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, check=False)
    box = get_box_from_system(item, check=False)

    tmp_item.append_structures(coordinates=coordinates, box=box)

    return tmp_item

