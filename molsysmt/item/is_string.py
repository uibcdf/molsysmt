from molsysmt._private.digestion import digest

@digest()
def is_string(form):

    from molsysmt.api_items import string_forms

    return (form in string_forms)

