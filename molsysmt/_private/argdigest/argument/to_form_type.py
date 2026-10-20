from ._supported import choice


def digest_to_form_type(to_form_type, caller=None):
    return choice(
        to_form_type, "to_form_type", [None, "class", "file", "string"], caller
    )
