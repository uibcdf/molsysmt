from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_id')
def to_file_bcif_gz(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):
    """
    Converting from string:pdb_id to file.bcif.gz.

    Parameters
    ----------
    item : string:pdb_id
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file.bcif.gz
        Converted molecular system representation.
    """

    from ..file_bcif_gz import download
    from ..file_bcif_gz.extract import extract

    tmp_item = download(item, output_filename=output_filename)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=tmp_item, copy_if_all=False, skip_digestion=True)

    return tmp_item
