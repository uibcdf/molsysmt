from .is_string_pdb_id import is_string_pdb_id
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_string_pdb_id(item)
        except:
            raise WrongFormError('string:pdb_id')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import to_string_pdb_text
    from ..string_pdb_text import to_mdtraj_Topology as string_pdb_text_to_mdtraj_Topology

    tmp_item = to_string_pdb_text(item, check=False)
    tmp_item = string_pdb_text_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

