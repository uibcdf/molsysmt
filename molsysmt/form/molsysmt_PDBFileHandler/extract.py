from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.PDBFileHandler')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if output_filename is not None and output_filename != item:
            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename
        else:
            if copy_if_all and output_filename is not None:
                 from shutil import copy as copy_file
                 copy_file(item, output_filename)
                 tmp_item = output_filename
            else:
                 tmp_item = item
    else:

        raise NotImplementedMethodError(caller='molsysmt.form.molsysmt_PDBFileHandler.extract')

    return tmp_item

