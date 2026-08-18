
def is_form(item):
    """
    Checking whether an item is an instance of form biopython.Seq.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form biopython.Seq, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    return item_fullname == 'biopython.Seq'
