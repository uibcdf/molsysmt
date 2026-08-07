from molsysmt._private.smonitor import NotImplementedMethodError, ArgumentError
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:pir')
def copy(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.file_pir.copy',
                            message='output_filename is required to copy a file:pir item.')

    from shutil import copy as copy_file
    copy_file(item, output_filename)

    return output_filename
