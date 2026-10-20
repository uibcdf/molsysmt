from ._supported import choice


def digest_from_viewer(from_viewer, caller=None):
    from molsysmt.supported.viewers import viewers

    return choice(from_viewer, "from_viewer", [None, *viewers], caller)
