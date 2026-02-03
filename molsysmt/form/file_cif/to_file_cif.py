from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.files_and_directories import str_filename

@arg_digest(form='file:cif')
def to_file_cif(item, atom_indices='all', structure_indices='all', output_name=None, copy_if_all=True,
                skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, output_name=output_name,
                   copy_if_all=copy_if_all, skip_digestion=True)

