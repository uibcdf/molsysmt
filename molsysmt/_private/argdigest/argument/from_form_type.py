from ._supported import choice


def digest_from_form_type(from_form_type, caller=None):
    return choice(
        from_form_type, "from_form_type", [None, "class", "file", "string"], caller
    )
