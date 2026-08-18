
def is_form(item):
    """
    Checking whether an item is an instance of form biopython.SeqRecord.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form biopython.SeqRecord, False otherwise.
    """

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'biopython.SeqRecord')

    return output

