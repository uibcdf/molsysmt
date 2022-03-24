from .is_string_pdb_id import is_string_pdb_id
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all', check=True):

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

    from mmtf import fetch
    from ..mmtf_MMTFDecoder import extract as extract_mmtf_MMTFDecoder

    tmp_item = item.split(':')[-1]
    tmp_item = fetch(tmp_item)
    tmp_item = extract_mmtf_MMTFDecoder(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

