from ..lists_and_tuples import is_list_or_tuple
from molsysmt.api_forms import _dict_forms_lowercase
from ..exceptions import WrongFormError, WrongToFormError

def digest_form(form, caller=None):
    """ Checks if the name of the form is supported.

    If the form name is correctly spelled but not capitalized, the method returns the right name.

    Parameters
    ----------
    form: str or list of str
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
        A WrongFormError is raised if the form name is not supported.

    """
    from molsysmt.item import is_file

    if is_list_or_tuple(form):
        return [digest_form(ii, caller=caller) for ii in form]
    else:
        if is_file(form):
            return form
        else:
            try:
                return _dict_forms_lowercase[form.lower()]
            except:
                pass

    raise WrongFormError(form, caller)

def digest_to_form(to_form, caller=None):
    """ Checks if the to_form value is supported.

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

    return digest_form(to_form, caller)
