from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_cif_gz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from ..file_cif_gz import download
    from ..file_cif_gz.extract import extract

    from molsysmt.form.string_pdb_id import _extract_pdb_id
    tmp_item = download(_extract_pdb_id(item), output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item
