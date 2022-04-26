from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'string:pdb_id')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_mmtf_MMTFDecoder
    from ..mmtf_MMTFDecoder import to_file_mmtf

    tmp_item = to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item = to_file_mmtf(tmp_item, output_filename=output_filename, check=False)

    return tmp_item

