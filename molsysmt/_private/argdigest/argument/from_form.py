from ._supported import form_filter


def digest_from_form(from_form, caller=None):
    return form_filter(from_form, "from_form", caller)
