from ..exceptions import WrongFormError

def digest_item(item, form):

    from molsysmt.api_forms import dict_is_form

    try:
        dict_is_form[form](item)
    except:
        raise WrongFormError(form)

    pass

