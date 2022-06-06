from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, box=None, check=True):

    if check:

        digest_item(item, 'openmm.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    from molsysmt.native.molsys import MolSys
    from molsysmt.native.structures import Structures
    from . import to_molsysmt_Topology as to_molsysmt_Topology
    from . import get_box_from_system

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append_structures(coordinates=coordinates, box=box)

    return tmp_item

