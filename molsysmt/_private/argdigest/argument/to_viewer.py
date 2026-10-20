from ._supported import choice


def digest_to_viewer(to_viewer, caller=None):
    from molsysmt.supported.viewers import viewers

    return choice(to_viewer, "to_viewer", [None, *viewers], caller)
