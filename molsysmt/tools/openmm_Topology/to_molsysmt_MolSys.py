from molsysmt.tools.openmm_Topology.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError, WrongBoxError
from molsysmt._private_tools.exceptions import NotImplementedMethodError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_coordinates, digest_box

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
    from molsysmt.tools.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology
    from molsysmt.tools.openmm_Topology import get_box_from_system

    tmp_item = MolSys()
    tmp_item.topology = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item.structures = Structures()
    if box is None:
        box = get_box_from_system(item)
    tmp_item.structures.append_structures(coordinates=coordinates, box=box)

    return tmp_item

