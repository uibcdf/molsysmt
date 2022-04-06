from .is_file_prmtop import is_file_prmtop
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_molsysmt_MolSys(item, atom_indices='all', coordinates=None, check=True):

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
            raise WrongAtomIndicesError()

    from molsysmt.native import MolSys, Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology
    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)
    tmp_item.structures = Structures()
    tmp_item.structures.append_structures(coordinates=coordinates)

    return tmp_item

