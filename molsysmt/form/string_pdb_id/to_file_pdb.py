from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    from ..file_pdb import download as download_file_pdb
    from ..file_pdb import extract as extract_file_pdb

    tmp_item = download_file_pdb(item.replace('pdb_id:', ''), output_filename)
    tmp_item = extract_file_pdb(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False)

    return tmp_item

def _to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None):

    return to_file_pdb(item, atom_indices=atom_indices,
                                     structure_indices=structure_indices,
                                     output_filename=output_filename)

