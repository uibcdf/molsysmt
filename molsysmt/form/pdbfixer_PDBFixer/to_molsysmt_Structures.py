from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import WrongAtomIndicesError
from molsysmt._private.atom_indices import digest_atom_indices

def to_molsysmt_Structures(item, atom_indices='all', check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from molsysmt.native.structures import Structures
    from molsysmt.tools.pdbfixer_PDBFixer import get_coordinates_from_atom, get_box_from_system

    tmp_item = Structures()
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, check=False)
    box = get_box_from_system(item, check=False)

    tmp_item.append_structures(coordinates=coordinates, box=box)

    return tmp_item

