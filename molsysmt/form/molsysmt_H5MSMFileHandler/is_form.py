
def is_form(item):
    """
    Checking whether an item is an instance of form molsysmt.H5MSMFileHandler.


    Parameters
    ----------
    item : molecular system
        Argument item.

    Returns
    -------
    bool
        True if condition is satisfied, False otherwise.


    .. versionadded:: 1.0.0
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'molsysmt.native.h5msm_file_handler.H5MSMFileHandler')

    return output

