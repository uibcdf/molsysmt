from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from ..file_pdb import download
    from ..file_pdb import extract

    tmp_item = download(item.replace('pdb_id:', ''), output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item

