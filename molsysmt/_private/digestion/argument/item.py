from molsysmt._private.exceptions import ArgumentError

def digest_item(item, form=None, caller=None):
    """ Checks if an object is an item. Optionally checks if the item has the expected form.

        Parameters
        ----------
        item : obj
            An instance of one of the forms supported by MolSysMT.
        form : str, optional
            Name of the expected form.
        caller: str, optional
            Name of the function or method that is being digested.

        Raises
        ------
        WrongItemError or WrongItemFormError
            A WrongItemError is raised if the item object is not in deed an item.
            A WrongItemFormError is raised if the item object has not the expected form.

        Examples
        --------
        >>> from Bio.Seq import Seq
        >>> sequence = Seq("ATA")
        >>> digest_item(item=sequence, form="biopython.Seq")

    """
    from molsysmt.basic import get_form

    try:
        in_form = get_form(item)
        output = True
    except:
        output = False

    if output:
        if form is not None:
            if in_form!=form:
                raise ArgumentError('item', caller=caller, message=None)
        return item

    raise ArgumentError('item', caller=caller, message=None)
