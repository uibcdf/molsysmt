from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:psf')
def to_file_psf(
    item,
    atom_indices='all',
    structure_indices='all',
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):

    from .extract import extract

    return extract(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        copy_if_all=copy_if_all,
        skip_digestion=True,
    )
