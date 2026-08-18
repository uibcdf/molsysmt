from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:top')
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form file:top.

    Parameters
    ----------
    item : file:top
        Source item.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    file:top
        Copied item.
    """

    from shutil import copy as copy_file
    copy_file(item, output_filename)
    tmp_item = output_filename

    return tmp_item
