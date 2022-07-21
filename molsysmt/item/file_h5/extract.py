from molsysmt._private.exceptions.not_implemented import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='file:h5')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True):

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item
    else:

        raise NotImplementedMethodError()

    return tmp_item

