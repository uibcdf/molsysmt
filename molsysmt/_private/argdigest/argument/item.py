from molsysmt._private.smonitor import ArgumentError, NotSupportedFormError


def digest_item(item, form=None, caller=None):
    """Checks if an object is an item. Optionally checks if the item has the expected form.

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
    ArgumentError
        If the input is genuinely unsupported or has the wrong required form.
    MolecularSystemVerificationError
        If a declared adapter or form detector cannot finish verification.
        Operational exceptions retain their original Python cause chain.

    Examples
    --------
    >>> from Bio.Seq import Seq
    >>> sequence = Seq("ATA")
    >>> digest_item(item=sequence, form="biopython.Seq")

    """

    from molsysmt.basic import get_form

    append_target = (
        isinstance(caller, str)
        and caller.startswith("molsysmt.form")
        and caller.endswith("append_structures")
    )
    if append_target and item is None:
        return None

    try:
        in_form = get_form(item)
    except NotSupportedFormError as error:
        raise ArgumentError(
            "item",
            value=item,
            caller=caller,
            message=f"Error in argument 'item': {error}",
            cause=error,
        ) from error
    if append_target:
        return item
    if form is not None and in_form != form:
        raise ArgumentError("item", value=item, caller=caller, message=None)
    return item
