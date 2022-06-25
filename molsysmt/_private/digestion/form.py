from ..lists_and_tuples import is_list_or_tuple
from ..exceptions import WrongFormError


def digest_form(form):
    """ Checks that the name of the form is correct and
        returns its name capitalized. For example, if
        form is mdanalysis.universe it returns mdanalysis.Universe.

        Parameters
        ----------
        form: str or list[str]
            The name or names of the forms

        Returns
        -------
         str or list[str]
            The name or names of the forms.

    """
    from molsysmt.api_forms import _dict_forms_lowercase
    from molsysmt.item import is_file

    if is_list_or_tuple(form):
        return [digest_form(ii) for ii in form]
    else:
        if is_file(form):
            return form
        else:
            try:
                return _dict_forms_lowercase[form.lower()]
            except KeyError:
                raise WrongFormError(form)


def digest_to_form(to_form):

    if to_form is None:
        return None
    return digest_form(to_form)
