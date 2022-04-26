from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_openmm_Topology import is_openmm_Topology

def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, box=None, check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

        try:
            box = digest_box(box)
        except:
            raise WrongBoxError()

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

