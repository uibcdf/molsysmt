from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:smi')
def copy(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ValueError("output_filename is required to copy a file:smi item.")

    from shutil import copy as copy_file
    copy_file(item, output_filename)

    return output_filename
