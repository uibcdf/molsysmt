from molsysmt._private.smonitor import ArgumentError

# Tolerance aliases for common user mistakes (singular/variant spellings).
# These are NOT official form names — do not document or advertise them.
_FORM_TOLERANCE_ALIASES = {
    "molsysmt.structure": "molsysmt.Structures",
    "molsysmt.topology": "molsysmt.Topology",
    "molsysmt.molsys": "molsysmt.MolSys",
    "molsysmt.molsysdict": "molsysmt.MolSysDict",
    "molsysmt.topologydict": "molsysmt.TopologyDict",
    "molsysmt.structuresdict": "molsysmt.StructuresDict",
}


def digest_to_form(to_form, caller=None):
    """Checks if the to_form value is supported.

    If the to_form value is a string correctly spelled but not capitalized, the method returns the right name.

    Parameters
    ----------
    to_form: str or list of str
        The name or names of the forms.

    caller: str, optional
        Name of the function or method that is being digested.

    Returns
    -------
     str or list of str
        The name or names of the forms.

    Raises
    ------
    WrongFormError
        A WrongToFormError is raised if the form name is not supported.

    """
    if to_form is None:
        return None

    from molsysmt.form import _dict_forms_lowercase, is_file

    if isinstance(to_form, (list, tuple)):
        return [digest_to_form(ii, caller=caller) for ii in to_form]
    else:
        # Known names and tolerated spellings do not need item detection.
        if isinstance(to_form, str):
            canonical = _dict_forms_lowercase.get(to_form.lower())
            if canonical is not None:
                return canonical
            canonical = _FORM_TOLERANCE_ALIASES.get(to_form.lower())
            if canonical is not None:
                return canonical
        if is_file(to_form):
            return to_form

    raise ArgumentError("to_form", value=to_form, caller=caller, message=None)
