from .is_string_pdb_id import is_string_pdb_id
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        try:
            is_string_pdb_id(item)
        except:
            raise WrongFormError('string:pdb_id')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()


    from ..file_mmtf import download as download_file_mmtf
    from ..file_mmtf import extract as extract_file_mmtf

    download_file_mmtf(item, output_filename)
    tmp_item = extract_file_mmtf(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=output_filename, copy_if_all=False, check=False)

    return tmp_item

