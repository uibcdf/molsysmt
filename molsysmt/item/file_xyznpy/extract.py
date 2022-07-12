from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.variables import is_all

def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, check=True):

    if check:

        digest_item(item, 'file:xyznpy')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

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

        raise NotImplementedError()

    return tmp_item

