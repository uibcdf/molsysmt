from ._supported import choice


def digest_as_rows(as_rows, caller=None):
    return choice(as_rows, "as_rows", ["from", "to"], caller)
