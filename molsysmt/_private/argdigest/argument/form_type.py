from ._supported import choice


def digest_form_type(form_type, caller=None):
    return choice(
        form_type, "form_type", [None, "all", "class", "file", "string"], caller
    )
