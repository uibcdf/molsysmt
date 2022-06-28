from ..exceptions import WrongFormError


def digest_item(item, form):
    """ Check if an item hsa the expected form.

        Examples
        --------
        >>> from Bio.Seq import Seq
        >>> sequence = Seq("ATA")
        >>> digest_item(item=sequence, form="biopython.Seq")

        Parameters
        ----------
        item : obj
            An instance of one of the forms supported by MolSysMT.

        form : str
            Name of the form

        Raises
        ------
        WrongFormError
            If the item form is not the given form.

    """
    from molsysmt.api_forms import dict_is_form

    try:
        dict_is_form[form](item)
    except KeyError:
        raise WrongFormError(form)
