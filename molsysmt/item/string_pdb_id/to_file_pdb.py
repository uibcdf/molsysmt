from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    if check:

        digest_item(item, 'string:pdb_id')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from ..file_pdb import download as download_file_pdb
    from ..file_pdb import extract as extract_file_pdb

    tmp_item = download_file_pdb(item.replace('pdb_id:', ''), output_filename)
    tmp_item = extract_file_pdb(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False)

    return tmp_item

