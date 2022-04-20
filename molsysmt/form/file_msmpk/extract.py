from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, check=True):

    if check:

        digest_item(item, 'file:msmpk')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if output_filename is None:
        output_filename = item

    if (atom_indices is 'all') and (structure_indices is 'all'):

        if copy_if_all or (output_filename!=item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item
    else:

        raise NotImplementedError()

    return tmp_item

