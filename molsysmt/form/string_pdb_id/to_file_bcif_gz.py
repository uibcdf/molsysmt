from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_file_bcif_gz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from ..file_bcif_gz import download
    from ..file_bcif_gz import extract

    if item.startswith('pdb_id:'):
        tmp_item = item.split(':')[-1]
    elif item.startswith('pdb_'):
        tmp_item = item[-4:]
    else:
        tmp_item = item

    tmp_item = download(tmp_item, output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item
