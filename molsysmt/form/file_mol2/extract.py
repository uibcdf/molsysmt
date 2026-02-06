from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='file:mol2')
@dep_digest('parmed')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            raise NotImplementedMethodError()

        else:

            raise NotImplementedMethodError()

    else:

        raise NotImplementedMethodError()

    return tmp_item

